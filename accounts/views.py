from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render
from django.utils.http import urlsafe_base64_encode
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer, MyUserSerializer, ChangePasswordSerializer, UpdateUserSerializer
from .models import MyUser
from .serializers import RegisterUserSerializer
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_decode


class RegisterUserAPIView(generics.CreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = RegisterUserSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UsersList(generics.ListAPIView):
    serializer_class = MyUserSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = MyUser.objects.all()
        return queryset



class UserDetailsView(generics.RetrieveAPIView):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'national_code'


class UpdateUserView(generics.UpdateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UpdateUserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'national_code'
    parser_classes = [MultiPartParser, FormParser]

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class DeleteUserView(generics.DestroyAPIView):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'national_code'


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserPasswordResetView(APIView):
    def post(self, request):
        email = request.data.get("email")
        try:
            user = MyUser.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            reset_link = f"http://localhost:8000/accounts/reset/{uid}/{token}/"
            send_mail(
                subject="Reset Your Password",
                message=f"Click the link to reset your password: {reset_link}",
                from_email="noreply@example.com",
                recipient_list=[email],
            )

            return Response({"detail": "Password reset email sent."}, status=status.HTTP_200_OK)
        except MyUser.DoesNotExist:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)


class UserPasswordResetConfirmView(APIView):
    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = MyUser.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                new_password = request.data.get("password")
                user.set_password(new_password)
                user.save()
                return Response({"detail": "Password has been reset."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()
            return Response({'detail': 'رمز عبور با موفقیت تغییر کرد.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
