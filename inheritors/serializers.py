from rest_framework import serializers
from .models import Inheritors


class InheritorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inheritors
        fields = '__all__'
        read_only_fields = ['user']