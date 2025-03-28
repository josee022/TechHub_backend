from django.contrib.auth.models import AbstractUser  # Modelo base de usuario en Django
from django.db import models  # Modelos de base de datos
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save

class CustomUser(AbstractUser):
    """ Usuario personalizado con un campo de rol adicional. """

    ROLE_CHOICES = (
        ('admin', 'Admin'),  # Administrador
        ('user', 'User'),  # Usuario normal
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')  # Rol del usuario

    def __str__(self):
        """ Retorna el username como representación del usuario. """
        return str(self.username)

User = get_user_model()

class Profile(models.Model):
    """ Perfil de usuario con información adicional. Relación 1 a 1 con CustomUser. """
    objects = models.Manager()  # Definir el manager explícitamente (opcional)

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)  # Imagen opcional
    bio = models.TextField(blank=True, null=True)  # Biografía
    location = models.CharField(max_length=100, blank=True, null=True)  # Ubicación
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación

    def __str__(self):
        """ Retorna la relación con el usuario. """
        return f"Perfil de {self.user}"

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """ Crea automáticamente un perfil cuando se registra un usuario. """
    if created:
        Profile.objects.create(user=instance)
