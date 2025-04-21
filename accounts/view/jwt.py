from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims to the token
        token['full_name'] = user.full_name
        token['is_admin'] = user.is_admin
        token['email'] = user.email
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['full_name'] = self.user.full_name
        data['national_code'] = self.user.national_code
        data['is_admin'] = self.user.is_admin
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
