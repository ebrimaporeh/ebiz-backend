"""
apps/sectors/views.py

ViewSets for Sector taxonomy models with country/region support for West African expansion.
"""

from rest_framework import viewsets, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count, Sum

from apps.core.pagination import StandardPagination
from apps.core.permissions import IsAdminOrReadOnly
from .models import Sector, SectorTag, SectorStat
from .serializers import (
    SectorSerializer, SectorListSerializer, SectorDetailSerializer,
    SectorTagSerializer, SectorStatSerializer
)


class SectorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Sector model with country/region filtering.
    
    Provides CRUD operations for business sectors/categories.
    Public: Read-only access
    Admin: Full CRUD access
    Supports lookup by ID or slug.
    Supports filtering by country and region for West African expansion.
    """
    
    queryset = Sector.objects.filter(is_deleted=False)
    serializer_class = SectorSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'summary_for_ai']
    filterset_fields = ['status', 'parent', 'country', 'region']
    ordering_fields = ['order', 'name', 'business_count', 'created_at', 'country']
    ordering = ['country', 'order', 'name']
    lookup_field = 'slug'
    lookup_value_regex = '[^/]+'
    
    def get_serializer_class(self):
        """Return different serializers based on action"""
        if self.action == 'list':
            return SectorListSerializer
        elif self.action == 'retrieve':
            return SectorDetailSerializer
        return SectorSerializer
    
    def get_queryset(self):
        """Filter by status for non-admin users and apply country/region filters"""
        queryset = super().get_queryset()
        
        # Non-admin users only see published sectors
        if not self.request.user.is_staff:
            queryset = queryset.filter(status='published')
        
        # Country filter from query param
        country = self.request.query_params.get('country')
        if country:
            queryset = queryset.filter(country=country)
        
        # Region filter
        region = self.request.query_params.get('region')
        if region:
            queryset = queryset.filter(region=region)
        
        return queryset
    
    def get_object(self):
        """
        Override get_object to support lookup by either ID or slug.
        """
        lookup_value = self.kwargs.get(self.lookup_field)
        
        # Try to find by ID first (UUID format)
        try:
            import uuid
            uuid.UUID(str(lookup_value))
            obj = get_object_or_404(Sector, pk=lookup_value, is_deleted=False)
        except (ValueError, TypeError):
            # Otherwise try by slug
            obj = get_object_or_404(Sector, slug=lookup_value, is_deleted=False)
        
        # Check permissions
        self.check_object_permissions(self.request, obj)
        
        return obj
    
    @action(detail=False, methods=['get'])
    def by_country(self, request):
        """Get sectors filtered by country code"""
        country_code = request.query_params.get('country_code', 'gm')
        sectors = self.get_queryset().filter(country=country_code)
        page = self.paginate_queryset(sectors)
        if page is not None:
            serializer = SectorListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = SectorListSerializer(sectors, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_region(self, request):
        """Get sectors filtered by region"""
        region = request.query_params.get('region', 'west_africa')
        sectors = self.get_queryset().filter(region=region)
        page = self.paginate_queryset(sectors)
        if page is not None:
            serializer = SectorListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = SectorListSerializer(sectors, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def top_level(self, request):
        """Get only top-level sectors (no parent)"""
        sectors = self.get_queryset().filter(parent__isnull=True)
        page = self.paginate_queryset(sectors)
        if page is not None:
            serializer = SectorListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = SectorListSerializer(sectors, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def children(self, request, slug=None):
        """Get child sectors of a parent sector"""
        sector = self.get_object()
        children = sector.children.filter(is_deleted=False)
        
        if not request.user.is_staff:
            children = children.filter(status='published')
        
        serializer = SectorListSerializer(children, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def stats(self, request, slug=None):
        """Get sector statistics"""
        sector = self.get_object()
        stats = sector.stats.all()
        serializer = SectorStatSerializer(stats, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def tags(self, request, slug=None):
        """Get tags assigned to this sector"""
        sector = self.get_object()
        tags = sector.tag_assignments.select_related('tag').all()
        data = [{'id': t.tag.id, 'label': t.tag.label, 'slug': t.tag.slug} for t in tags]
        return Response(data)
    
    @action(detail=False, methods=['get'])
    def available_countries(self, request):
        """Get list of countries that have sectors"""
        from apps.core.constants import Country as CountryChoice, COUNTRY_FLAGS
        
        countries = self.get_queryset().values_list('country', flat=True).distinct()
        country_data = []
        for code in countries:
            country_name = dict(CountryChoice.choices).get(code, code)
            country_data.append({
                'code': code,
                'name': country_name,
                'flag': COUNTRY_FLAGS.get(code, "")
            })
        return Response(country_data)


class SectorTagViewSet(viewsets.ModelViewSet):
    """
    ViewSet for SectorTag model.
    Admin only for write operations.
    """
    
    queryset = SectorTag.objects.all()
    serializer_class = SectorTagSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['label', 'description']
    ordering_fields = ['label', 'created_at']
    ordering = ['label']


class SectorStatViewSet(viewsets.ModelViewSet):
    """
    ViewSet for SectorStat model with country/region support.
    Admin only for write operations.
    """
    
    queryset = SectorStat.objects.all().select_related('sector', 'source')
    serializer_class = SectorStatSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['sector', 'year', 'is_headline', 'country', 'region']
    ordering_fields = ['display_order', 'year']
    ordering = ['sector', 'display_order']
    
    def get_queryset(self):
        """Filter by year and country/region if provided"""
        queryset = super().get_queryset()
        
        year = self.request.query_params.get('year')
        if year:
            queryset = queryset.filter(year=year)
        
        country = self.request.query_params.get('country')
        if country:
            queryset = queryset.filter(country=country)
        
        region = self.request.query_params.get('region')
        if region:
            queryset = queryset.filter(region=region)
        
        return queryset