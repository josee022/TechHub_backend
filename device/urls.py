from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DeviceViewSet

# Crear el router y registrar el viewset
router = DefaultRouter()
router.register(r'devices', DeviceViewSet, basename='device')

app_name = 'devices'

urlpatterns = [
    *router.urls,
    path('<int:device_id>/reviews/', include('reviews.urls')),
]