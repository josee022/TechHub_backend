from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Device
from .serializers import DeviceSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Count, Avg, Sum
from django.db.models.functions import TruncMonth, TruncDay
from datetime import datetime, timedelta

class DevicePagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = 'page_size'
    max_page_size = 100

class DeviceFilter(filters.FilterSet):
    estado = filters.BooleanFilter()
    fecha_creacion_after = filters.DateTimeFilter(field_name='fecha_creacion', lookup_expr='gte')
    fecha_creacion_before = filters.DateTimeFilter(field_name='fecha_creacion', lookup_expr='lte')

    class Meta:
        model = Device
        fields = ['estado', 'fecha_creacion_after', 'fecha_creacion_before']

class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all().order_by('-fecha_creacion')
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = DevicePagination
    filter_backends = [filters.DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = DeviceFilter
    search_fields = ['nombre', 'tipo', 'descripcion']
    ordering_fields = ['fecha_creacion', 'nombre', 'estado']

    def perform_create(self, serializer):
        """Asigna automáticamente el usuario autenticado al crear un dispositivo"""
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        """Actualiza el dispositivo manteniendo el usuario original"""
        serializer.save()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dashboard_stats(request):
    """
    Endpoint para obtener estadísticas para el dashboard
    """
    # Obtener todos los dispositivos del usuario actual
    user_devices = Device.objects.filter(user=request.user)
    
    # Estadísticas básicas
    total_devices = user_devices.count()
    active_devices = user_devices.filter(estado=True).count()
    inactive_devices = user_devices.filter(estado=False).count()
    avg_rating = user_devices.aggregate(avg=Avg('average_rating'))['avg'] or 0
    
    # Dispositivos por tipo
    devices_by_type = user_devices.values('tipo').annotate(count=Count('id'))
    
    # Dispositivos creados por mes (últimos 6 meses)
    six_months_ago = datetime.now() - timedelta(days=180)
    devices_by_month = user_devices.filter(
        fecha_creacion__gte=six_months_ago
    ).annotate(
        month=TruncMonth('fecha_creacion')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')
    
    # Formatear los datos para el frontend
    devices_by_month_formatted = [
        {
            'month': item['month'].strftime('%b %Y'),
            'count': item['count']
        } for item in devices_by_month
    ]
    
    # Actividad reciente (últimos 30 días)
    thirty_days_ago = datetime.now() - timedelta(days=30)
    recent_activity = user_devices.filter(
        last_updated__gte=thirty_days_ago
    ).annotate(
        day=TruncDay('last_updated')
    ).values('day').annotate(
        count=Count('id')
    ).order_by('day')
    
    # Formatear los datos para el frontend
    recent_activity_formatted = [
        {
            'date': item['day'].strftime('%d %b'),
            'count': item['count']
        } for item in recent_activity
    ]
    
    # Obtener las ubicaciones más comunes
    top_locations = user_devices.exclude(ubicacion__isnull=True).exclude(ubicacion='').values(
        'ubicacion'
    ).annotate(
        count=Count('id')
    ).order_by('-count')[:5]
    
    return Response({
        'basic_stats': {
            'total_devices': total_devices,
            'active_devices': active_devices,
            'inactive_devices': inactive_devices,
            'avg_rating': round(avg_rating, 1)
        },
        'devices_by_type': list(devices_by_type),
        'devices_by_month': devices_by_month_formatted,
        'recent_activity': recent_activity_formatted,
        'top_locations': list(top_locations)
    })
