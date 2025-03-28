from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    device = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ('id', 'user', 'device', 'rating', 'comment', 'created_at', 'updated_at')
        read_only_fields = ('user', 'device', 'created_at', 'updated_at')

    def get_user(self, obj):
        try:
            profile = getattr(obj.user, 'profile', None)
            avatar_url = profile.avatar.url if profile and hasattr(profile, 'avatar') else None
            return {
                'id': obj.user.id,
                'username': obj.user.username,
                'avatar': avatar_url
            }
        except AttributeError:
            return {
                'id': obj.user.id,
                'username': obj.user.username,
                'avatar': None
            }

    def get_device(self, obj):
        return {
            'id': obj.device.id,
            'nombre': obj.device.nombre
        }

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value

    def validate_comment(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Comment must be at least 10 characters long")
        return value

    def validate(self, data):
        request = self.context.get('request')
        device_id = request.data.get('device_id') if request else None
        user = request.user if request else None

        if device_id and user and Review.objects.filter(device_id=device_id, user=user, is_active=True).exists():
            raise serializers.ValidationError("You have already reviewed this device.")
        
        return data
