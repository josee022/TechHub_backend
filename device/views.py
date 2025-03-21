from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Device
from .serializers import DeviceSerializer

class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden usar estos endpoints

    def perform_create(self, serializer):
        """Asigna automáticamente el usuario autenticado al crear un dispositivo"""
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        """Actualiza el dispositivo sin sobrescribir `user` ni requerir otros campos"""
        serializer.save()
