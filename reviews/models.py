from django.db import models
from django.conf import settings
from django.db.models import Avg, Count
from device.models import Device

class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    objects: models.Manager = models.Manager()

    class Meta:
        unique_together = ('device', 'user')
        ordering = ['-created_at']

    def __str__(self):
        try:
            user_name = self.user.username if self.user else 'Anonymous'
            device_name = self.device.nombre if self.device else 'Unknown Device'
            return f"Review {self.rating} stars by {user_name} for {device_name}"
        except AttributeError:
            return f"Review {self.rating} stars for Unknown Device"

    @classmethod
    def update_device_ratings(cls, device_id):
        """Actualiza la puntuación promedio y el número de reseñas de un dispositivo"""
        try:
            # Obtener el promedio y conteo en una sola consulta
            stats = cls.objects.filter(
                device_id=device_id,
                is_active=True
            ).aggregate(
                avg_rating=Avg('rating'),
                review_count=Count('id')
            )
            
            avg_rating = stats['avg_rating']
            review_count = stats['review_count']
            
            # Actualizar el dispositivo en una sola operación
            Device.objects.filter(id=device_id).update(
                average_rating=round(avg_rating, 1) if avg_rating else 0,
                review_count=review_count or 0
            )
            
        except Exception as e:
            print(f"Error updating device ratings: {str(e)}")