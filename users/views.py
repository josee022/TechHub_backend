from rest_framework import generics, permissions, status  # Vistas basadas en clases y control de permisos
from rest_framework_simplejwt.views import TokenObtainPairView  # Login con JWT (access y refresh tokens)
from rest_framework.views import APIView  # Vistas personalizadas
from rest_framework.response import Response  # Respuestas JSON
from rest_framework.permissions import IsAuthenticated  # Restringe acceso a usuarios autenticados
from .models import CustomUser, Profile  # Modelo de usuario personalizado
from .serializers import UserSerializer, RegisterSerializer, ProfileSerializer  # Serializadores para manejar usuarios
from rest_framework_simplejwt.tokens import RefreshToken  # Para invalidar tokens en el logout

class RegisterView(generics.CreateAPIView):
    """ Registra nuevos usuarios (sin autenticación previa). """
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]  # Accesible para cualquier usuario

class LoginView(TokenObtainPairView):
    """ Autenticación con JWT (manejado automáticamente por Simple JWT). """
    pass

class ProtectedView(APIView):
    """ Ruta protegida: solo accesible con un token válido. """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """ Devuelve info del usuario autenticado. """
        user_data = {
            "username": request.user.username,
            "email": request.user.email,
            "role": request.user.role,
        }
        return Response({"message": "Acceso permitido", "user": user_data})

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
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder

    def get(self, request):
        """Obtener los datos del perfil del usuario autenticado."""
        profile = request.user.profile  # Accede al perfil del usuario autenticado
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        """Actualizar los datos del perfil del usuario autenticado."""
        profile = request.user.profile
        serializer = ProfileSerializer(profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
