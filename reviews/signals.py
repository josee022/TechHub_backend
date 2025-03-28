from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Review
from device.models import Device

@receiver(post_save, sender=Review)
def update_device_ratings_on_review_save(sender, instance, created, **kwargs):
    """Actualiza la puntuación promedio y el número de reseñas cuando se crea o actualiza una reseña"""
    Review.update_device_ratings(instance.device_id)

@receiver(post_delete, sender=Review)
def update_device_ratings_on_review_delete(sender, instance, **kwargs):
    """Actualiza la puntuación promedio y el número de reseñas cuando se elimina una reseña"""
    Review.update_device_ratings(instance.device_id)