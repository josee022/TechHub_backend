from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

from device.models import Device
from .models import Review
from .serializers import ReviewSerializer

class ReviewPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ReviewPagination

    def get_queryset(self):
        device_id = self.kwargs.get('device_id')
        if device_id:
            return Review.objects.filter(device_id=device_id)
        return Review.objects.all()

    def perform_create(self, serializer):
        device_id = self.kwargs.get('device_id')
        if not device_id:
            raise PermissionDenied("Device ID is required")
            
        if Review.objects.filter(device_id=device_id, user=self.request.user, is_active=True).exists():
            raise PermissionDenied("You have already reviewed this device")
            
        serializer.save(
            user=self.request.user,
            device_id=device_id
        )
        Review.update_device_ratings(device_id)

    def perform_update(self, serializer):
        review = self.get_object()
        if review.user != self.request.user:
            raise PermissionDenied("You can only update your own reviews")
        serializer.save()
        Review.update_device_ratings(review.device_id)

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You can only delete your own reviews")
        device_id = instance.device.id
        instance.delete()
        Review.update_device_ratings(device_id)

class AverageRatingView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, device_id):
        device = get_object_or_404(Device, id=device_id)
        return Response({
            'average_rating': device.average_rating,
            'review_count': device.review_count
        })
