from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Manager  # Add this import for type hinting
from cloudinary.models import CloudinaryField  # Importar CloudinaryField
import cloudinary

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
    imagen = CloudinaryField('image', folder='devices', null=True, blank=True)  # Usar CloudinaryField en lugar de ImageField
    average_rating = models.FloatField(default=0.0)
    review_count = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con CustomUser

    def __str__(self):
        return str(self.nombre)
        
    def imagen_url(self):
        """Devuelve la URL completa de la imagen de Cloudinary."""
        try:
            if self.imagen and hasattr(self.imagen, 'public_id') and self.imagen.public_id:
                return cloudinary.CloudinaryImage(self.imagen.public_id).build_url(secure=True)
        except Exception as e:
            print(f"Error al generar URL de imagen: {e}")
        return None
