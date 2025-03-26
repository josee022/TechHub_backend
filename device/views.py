from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Device
from .serializers import DeviceSerializer

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
