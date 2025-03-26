from rest_framework import serializers
from .models import Device
from users.serializers import UserSerializer

class DeviceSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Devuelve toda la info del usuario

    class Meta:
        model = Device
        fields = '__all__'  # Incluye todos los campos del modelo
