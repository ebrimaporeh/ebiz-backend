"""
apps/core/views.py

ViewSets for core models (Source, RatingValue, APIKey, Country, Region).
"""

from rest_framework import viewsets, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from apps.core.pagination import StandardPagination
from apps.core.permissions import IsAdminOrReadOnly, IsAuthenticatedOrReadOnly
from .models import Source, RatingValue, APIKey, Country, Region
from .serializers import (
    SourceSerializer, RatingValueSerializer, 
    APIKeySerializer, APIKeyCreateSerializer,
    CountrySerializer, CountryListSerializer, RegionSerializer
)
import secrets


# ============================================
# SOURCE VIEWSET
# ============================================

class SourceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Source model.
    Admin only for write operations.
    """
    
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'reference', 'notes']
    filterset_fields = ['source_type', 'year', 'is_primary_source']
    ordering_fields = ['year', 'confidence_rating', 'created_at']
    ordering = ['-year', '-confidence_rating']


# ============================================
# RATING VALUE VIEWSET
# ============================================

class RatingValueViewSet(viewsets.ModelViewSet):
    """
    ViewSet for RatingValue model.
    Admin only for write operations.
    """
    
    queryset = RatingValue.objects.select_related('source')
    serializer_class = RatingValueSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['year', 'source']
    ordering_fields = ['value', 'year']
    ordering = ['-year']


# ============================================
# API KEY VIEWSET
# ============================================

class APIKeyViewSet(viewsets.ModelViewSet):
    """
    ViewSet for APIKey model.
    Admin only for full access. Users can view their own keys.
    """
    
    queryset = APIKey.objects.all()
    serializer_class = APIKeySerializer
    permission_classes = [IsAdminUser]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['organization', 'contact_name', 'contact_email']
    filterset_fields = ['tier', 'is_active']
    ordering_fields = ['created_at', 'expires_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return APIKeyCreateSerializer
        return APIKeySerializer
    
    @action(detail=True, methods=['post'])
    def revoke(self, request, pk=None):
        """Revoke an API key (soft delete)"""
        api_key = self.get_object()
        api_key.is_active = False
        api_key.save()
        return Response({'status': 'revoked'})
    
    @action(detail=True, methods=['post'])
    def regenerate(self, request, pk=None):
        """Regenerate an API key"""
        api_key = self.get_object()
        from .models import APIKey as APIKeyModel
        api_key.key = f"gb_{secrets.token_urlsafe(32)}"
        api_key.save()
        return Response({'new_key': api_key.key})


# ============================================
# COUNTRY VIEWSET
# ============================================

class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Country model.
    Public read-only access.
    """
    
    queryset = Country.objects.filter(is_active=True)
    serializer_class = CountrySerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code']
    filterset_fields = ['is_active']
    ordering_fields = ['order', 'name']
    ordering = ['order', 'name']
    lookup_field = 'code'
    lookup_value_regex = '[a-z]{2}'
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CountryListSerializer
        return CountrySerializer
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get only active countries"""
        countries = self.get_queryset().filter(is_active=True)
        serializer = CountryListSerializer(countries, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def market_overview(self, request, code=None):
        """
        Get market overview for a specific country.
        Includes sector counts and business statistics.
        """
        from apps.sectors.models import Sector
        from django.db.models import Sum
        
        country = self.get_object()
        
        # Get sectors for this country
        sectors = Sector.objects.filter(
            country=country.code,
            is_deleted=False,
            status='published'
        )
        
        # Aggregate market data
        total_sectors = sectors.count()
        total_businesses = sectors.aggregate(total=Sum('business_count'))['total'] or 0
        
        # Get top sectors by business count
        top_sectors = sectors.order_by('-business_count')[:5].values('name', 'business_count', 'icon', 'slug')
        
        return Response({
            'country': {
                'code': country.code,
                'name': country.name,
                'flag': country.flag_emoji,
                'currency': country.currency,
                'currency_symbol': country.currency_symbol,
                'population': country.population,
                'gdp_per_capita_usd': country.gdp_per_capita_usd,
            },
            'statistics': {
                'total_sectors': total_sectors,
                'total_businesses': total_businesses,
                'average_businesses_per_sector': round(total_businesses / total_sectors, 1) if total_sectors > 0 else 0,
            },
            'top_sectors': list(top_sectors),
        })


# ============================================
# REGION VIEWSET
# ============================================

class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Region model.
    Public read-only access.
    """
    
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']
    
    @action(detail=True, methods=['get'])
    def countries(self, request, pk=None):
        """Get all countries in this region"""
        region = self.get_object()
        countries = region.countries.filter(is_active=True)
        serializer = CountryListSerializer(countries, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_country(self, request):
        """Find region that contains a specific country"""
        country_code = request.query_params.get('country_code')
        if not country_code:
            return Response({'error': 'country_code parameter required'}, status=400)
        
        region = Region.objects.filter(countries__code=country_code).first()
        if region:
            serializer = RegionSerializer(region)
            return Response(serializer.data)
        return Response({'detail': 'Region not found'}, status=404)