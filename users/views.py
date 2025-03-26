from rest_framework import generics, permissions, status  # Vistas basadas en clases y control de permisos
from rest_framework_simplejwt.views import TokenObtainPairView  # Login con JWT (access y refresh tokens)
from rest_framework.views import APIView  # Vistas personalizadas
from rest_framework.response import Response  # Respuestas JSON
from rest_framework.permissions import IsAuthenticated  # Restringe acceso a usuarios autenticados
from rest_framework_simplejwt.tokens import RefreshToken  # Para invalidar tokens en el logout
from rest_framework.exceptions import PermissionDenied  # Importar excepción para denegar permisos
from django.contrib.auth import authenticate
from .models import CustomUser, Profile  # Modelo de usuario personalizado
from .serializers import UserSerializer, RegisterSerializer, ProfileSerializer  # Serializadores para manejar usuarios
from .permissions import IsOwnerOrAdmin # Permisos personalizados
from rest_framework.parsers import MultiPartParser, FormParser
import logging
logger = logging.getLogger(__name__)

class RegisterView(generics.CreateAPIView):
    """ Registra nuevos usuarios (sin autenticación previa). """
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]  # Accesible para cualquier usuario

class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        try:
            logger.info(f"DEBUG - Login attempt for user: {request.data.get('username')}")
            response = super().post(request, *args, **kwargs)
            user = CustomUser.objects.get(username=request.data['username'])
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role
            }
            response.data['user'] = user_data
            logger.info(f"DEBUG - Login response data: {response.data}")
            return response
        except Exception as e:
            logger.error(f"DEBUG - Login error: {str(e)}")
            raise

class ProtectedView(APIView):
    """ Ruta protegida: solo accesible con un token válido. """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """ Devuelve info del usuario autenticado. """
        try:
            logger.info(f"DEBUG - Protected endpoint accessed by user: {request.user.username}")
            user_data = {
                "id": request.user.id,
                "username": request.user.username,
                "email": request.user.email,
                "role": request.user.role,
            }
            logger.info(f"DEBUG - Protected endpoint response: {user_data}")
            return Response({"message": "Acceso permitido", "user": user_data})
        except Exception as e:
            logger.error(f"DEBUG - Protected endpoint error: {str(e)}")
            return Response(
                {"error": "Error al obtener datos del usuario"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class LogoutView(APIView):
    """ Cierra sesión invalidando el refresh token. """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # Invalida el token de refresco
            return Response({"message": "Logout exitoso"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

class ProfileView(APIView):
    """Vista para que un usuario autenticado pueda ver y actualizar su perfil."""
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]  # Solo autenticados, permisos aplicados

    # Añadir los parsers para manejar archivos
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self, request, user_id=None):
        """Obtiene el perfil del usuario:"""
        if user_id:  # Si se pasa un ID en la URL...
            if request.user.role == "admin":  # Solo los admins pueden acceder a perfiles de otros usuarios
                return Profile.objects.get(user__id=user_id)
            elif request.user.id == user_id:  # El usuario puede ver su propio perfil
                return request.user.profile
            else:
                raise PermissionDenied("No tienes permisos para acceder a este perfil.")  # Bloquear acceso a otros perfiles

        return request.user.profile  # Si no se especifica ID, se accede al propio perfil

    def get(self, request, user_id=None):
        """Obtener los datos del perfil del usuario autenticado o de otro usuario (si es admin)."""
        profile = self.get_object(request, user_id)  # Obtiene el perfil correcto
        self.check_object_permissions(request, profile)  # Aplica los permisos
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, user_id=None):
        """Actualizar los datos del perfil del usuario autenticado o de otro usuario (si es admin)."""
        profile = self.get_object(request, user_id)  # Obtiene el perfil correcto
        self.check_object_permissions(request, profile)  # Aplica los permisos

        # Aseguramos que los datos de perfil (incluyendo imagen) lleguen correctamente
        serializer = ProfileSerializer(profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()  # Guardar los datos, incluyendo la imagen si está presente
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
