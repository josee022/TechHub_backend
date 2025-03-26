from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Manager  # Add this import for type hinting

User = get_user_model()  # Esto obtendrá el modelo de usuario personalizado

class Device(models.Model):
    objects: Manager = models.Manager()  # Add type hint for objects
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ubicacion = models.CharField(max_length=200, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    modelo_firmware = models.CharField(max_length=100, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    imagen = models.ImageField(upload_to='devices/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con CustomUser

    def __str__(self):
        return str(self.nombre)
