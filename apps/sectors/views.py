# apps/sectors/views.py
from rest_framework import viewsets, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404

from apps.core.pagination import StandardPagination
from apps.core.permissions import IsAdminOrReadOnly
from .models import Sector
from .serializers import SectorSerializer, SectorListSerializer, SectorDetailSerializer


class SectorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Sector model.
    
    Provides CRUD operations for business sectors/categories.
    Public: Read-only access
    Admin: Full CRUD access
    """
    
    queryset = Sector.objects.filter(is_deleted=False)
    serializer_class = SectorSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    filterset_fields = ['status']
    ordering_fields = ['order', 'name', 'business_count', 'created_at']
    ordering = ['order', 'name']
    
    def get_serializer_class(self):
        """Return different serializers based on action"""
        if self.action == 'list':
            return SectorListSerializer
        elif self.action == 'retrieve':
            return SectorDetailSerializer
        return SectorSerializer
    
    def get_queryset(self):
        """Filter by status for non-admin users"""
        queryset = super().get_queryset()
        
        # Non-admin users only see published sectors
        if not self.request.user.is_staff:
            queryset = queryset.filter(status='published')
        
        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a sector by either ID or slug.
        """
        lookup_value = kwargs.get('pk')
        
        # Try to find by ID first (if numeric)
        if lookup_value.isdigit():
            sector = get_object_or_404(Sector, pk=lookup_value, is_deleted=False)
        else:
            # Otherwise try by slug
            sector = get_object_or_404(Sector, slug=lookup_value, is_deleted=False)
        
        # Check status for non-admin users
        if not request.user.is_staff and sector.status != 'published':
            return Response(
                {'detail': 'Not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.get_serializer(sector)
        return Response(serializer.data)