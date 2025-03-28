from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet, AverageRatingView

router = DefaultRouter()
router.register(r'', ReviewViewSet, basename='review')

app_name = 'reviews'

urlpatterns = [
    path('average-rating/<int:device_id>/', AverageRatingView.as_view(), name='average_rating'),
    *router.urls
]