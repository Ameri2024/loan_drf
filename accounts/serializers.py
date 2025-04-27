from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import MyUser


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = [
            'national_code',
            'password',
            'email',
            'phone_num',
            'full_name',
            'father_name',
            'date_of_birth',
            'address',
            'work_address',
            'profile_image',
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return MyUser.objects.create_user(**validated_data)


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = [
            'email', 'phone_num', 'full_name', 'father_name',
            'date_of_birth', 'address', 'work_address',
            'profile_image','is_active'
        ]


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims if you want
        token['full_name'] = user.full_name
        return token

    def validate(self, attrs):
        # replace 'username' with 'national_code'
        self.fields['national_code'] = self.fields.pop('username')
        return super().validate(attrs)


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data.pop('password'))
        return super().update(instance, validated_data)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("رمز عبور فعلی اشتباه است.")
        return value

