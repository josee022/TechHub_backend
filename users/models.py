from django.contrib.auth.models import AbstractUser  # Modelo base de usuario en Django
from django.db import models  # Para definir los modelos de base de datos

class CustomUser(AbstractUser):
    """ Modelo de usuario personalizado con un campo de rol adicional. """

    ROLE_CHOICES = (
        ('admin', 'Admin'),  # Usuario administrador
        ('user', 'User'),  # Usuario normal
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')  # Rol del usuario

    def __str__(self):
        """ Retorna el email como representación del usuario. """
        return self.email
