from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DeviceViewSet

# Crear el router y registrar el viewset
router = DefaultRouter()
router.register(r'devices', DeviceViewSet)

urlpatterns = [
    path('api/', include(router.urls)),  # Incluir las URLs generadas automáticamente
]
