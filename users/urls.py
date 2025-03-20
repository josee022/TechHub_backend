from django.urls import path  # Importamos path para definir las rutas
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView  # Vistas de Simple JWT para login y refresh
from .views import RegisterView, ProtectedView, LogoutView, ProfileView  # Importamos las vistas de autenticación

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),  # Registro de usuarios
    path('login/', TokenObtainPairView.as_view(), name='login'),  # Obtiene el access_token y refresh_token
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Renueva el access_token con el refresh_token
    path('protected/', ProtectedView.as_view(), name='protected'),  # Ruta protegida para probar autenticación
    path('logout/', LogoutView.as_view(), name='logout'),  # Ruta para cerrar sesión
    path('profile/', ProfileView.as_view(), name='profile'),

]
