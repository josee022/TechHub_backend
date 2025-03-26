from rest_framework.routers import DefaultRouter
from .views import DeviceViewSet

# Crear el router y registrar el viewset
router = DefaultRouter()
router.register(r'devices', DeviceViewSet, basename='device')

# Las URLs se incluirán directamente en la ruta /api/ desde el urls.py principal
urlpatterns = router.urls
