from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'device', 'user', 'rating', 'is_active', 'created_at')
    list_filter = ('rating', 'is_active')
    search_fields = ('user__username', 'device__nombre', 'comment')
