from rest_framework import serializers
from .models import Device

class DeviceSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # Devuelve solo el ID del usuario

    class Meta:
        model = Device
        fields = '__all__'  # Incluye todos los campos del modelo
