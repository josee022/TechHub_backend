from rest_framework import serializers  # Serializadores de DRF
from django.contrib.auth.hashers import make_password  # Encripta contraseñas
from .models import CustomUser  # Modelo de usuario personalizado
from .models import Profile  # Modelo de profile personalizado

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

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    username = serializers.CharField(write_only=True, required=False)
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['user', 'avatar', 'bio', 'location', 'username', 'avatar_url']

    def get_avatar_url(self, obj):
        """Obtiene la URL completa del avatar."""
        try:
            if obj.avatar:
                url = obj.avatar_url()
                if url:
                    return url
                # Fallback: intentar obtener la URL directamente del campo CloudinaryField
                if hasattr(obj.avatar, 'url'):
                    return obj.avatar.url
        except Exception as e:
            print(f"Error en get_avatar_url: {e}")
        return None

    def update(self, instance, validated_data):
        # Actualizar el username si se proporciona
        if 'username' in validated_data:
            user = instance.user
            user.username = validated_data.pop('username')
            user.save()

        # Actualizar los demás campos del perfil
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
