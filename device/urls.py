from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DeviceViewSet, get_dashboard_stats

# Crear el router y registrar el viewset
router = DefaultRouter()
router.register('devices', DeviceViewSet, basename='device')

app_name = 'devices'

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard-stats/', get_dashboard_stats, name='dashboard-stats'),
    path('<int:device_id>/reviews/', include('reviews.urls')),
]