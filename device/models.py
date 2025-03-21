from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()  # Esto obtendrá el modelo de usuario personalizado

class Device(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ubicacion = models.CharField(max_length=200, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    modelo_firmware = models.CharField(max_length=100, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con CustomUser

    def __str__(self):
        return str(self.nombre)
