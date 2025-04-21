from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Inheritors
from .serializers import InheritorSerializer
from rest_framework.permissions import IsAuthenticated


class ManageInheritors(generics.ListCreateAPIView):
    serializer_class = InheritorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Inheritors.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        if not self.request.user:
            raise ValueError("User is not authenticated")
        serializer.save(user=self.request.user)


class CreateInheritor(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = InheritorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)  # اینجا user مستقیم در save پاس داده میشه
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class UpdateInheritorsView(generics.RetrieveUpdateAPIView):
    queryset = Inheritors.objects.all()
    serializer_class = InheritorSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'


class DeleteInheritorsView(generics.DestroyAPIView):
    queryset = Inheritors.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
