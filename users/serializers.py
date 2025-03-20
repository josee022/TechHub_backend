from rest_framework import serializers  # Serializadores de DRF
from django.contrib.auth.hashers import make_password  # Encripta contraseñas
from .models import CustomUser  # Modelo de usuario personalizado

class UserSerializer(serializers.ModelSerializer):
    """ Serializador para mostrar información del usuario (sin contraseña). """
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role']  # Campos visibles en la API

class RegisterSerializer(serializers.ModelSerializer):
    """ Serializador para registrar usuarios (maneja la contraseña de forma segura). """
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}  # Oculta la contraseña en respuestas JSON

    def create(self, validated_data):
        """ Encripta la contraseña antes de guardar el usuario. """
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)  # Guarda el usuario con la contraseña encriptada
