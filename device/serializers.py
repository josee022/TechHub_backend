from rest_framework import serializers
from .models import Device
from users.serializers import UserSerializer

class DeviceSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Devuelve toda la info del usuario
    imagen_url = serializers.SerializerMethodField()

    class Meta:
        model = Device
        fields = '__all__'  # Incluye todos los campos del modelo
        
    def get_imagen_url(self, obj):
        """Obtiene la URL completa de la imagen."""
        if obj.imagen:
            return obj.imagen_url()
        return None
