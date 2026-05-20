# apps/businesses/views.py
from rest_framework import viewsets, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404

from apps.core.pagination import StandardPagination
from apps.core.permissions import IsAdminOrReadOnly
from .models import Business, BusinessScale, BusinessProfile, BusinessProfileFeature, BusinessProfileTestimonial
from .serializers import (
    BusinessSerializer, BusinessListSerializer, BusinessDetailSerializer,
    BusinessScaleSerializer, BusinessProfileSerializer, BusinessProfileListSerializer,
    BusinessProfileDetailSerializer, PartnerDirectorySerializer,
    BusinessProfileFeatureSerializer, BusinessProfileTestimonialSerializer
)


class BusinessViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Business model.
    
    Provides CRUD operations for business profiles.
    Supports lookup by ID or slug.
    Public: Read-only access
    Admin: Full CRUD access
    """
    
    queryset = Business.objects.filter(is_deleted=False).select_related('sector')
    serializer_class = BusinessSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'short_description', 'overview']
    filterset_fields = ['sector', 'status', 'is_featured']
    ordering_fields = ['name', 'view_count', 'created_at']
    ordering = ['-is_featured', 'name']
    lookup_field = 'slug'
    lookup_value_regex = '[^/]+'
    
    def get_serializer_class(self):
        """Return different serializers based on action"""
        if self.action == 'list':
            return BusinessListSerializer
        elif self.action == 'retrieve':
            return BusinessDetailSerializer
        return BusinessSerializer
    
    def get_queryset(self):
        """Filter by status for non-admin users"""
        queryset = super().get_queryset()
        
        # Non-admin users only see published businesses
        if not self.request.user.is_staff:
            queryset = queryset.filter(status='published')
        
        return queryset
    
    def get_object(self):
        """
        Override get_object to support lookup by either ID or slug.
        """
        lookup_value = self.kwargs.get(self.lookup_field)
        
        # Try to find by ID first (if numeric)
        if lookup_value and lookup_value.isdigit():
            obj = get_object_or_404(Business, pk=lookup_value, is_deleted=False)
        else:
            # Otherwise try by slug
            obj = get_object_or_404(Business, slug=lookup_value, is_deleted=False)
        
        # Check permissions
        self.check_object_permissions(self.request, obj)
        
        return obj
    
    @action(detail=False, methods=['post'], url_path='increment-view/(?P<slug>[^/.]+)')
    def increment_view_by_slug(self, request, slug=None):
        """Increment view count for a business using slug"""
        business = get_object_or_404(Business, slug=slug, is_deleted=False)
        business.increment_view_count()
        return Response({'view_count': business.view_count})
    
    @action(detail=True, methods=['post'])
    def increment_view(self, request, pk=None):
        """Increment view count for a business using ID"""
        business = self.get_object()
        business.increment_view_count()
        return Response({'view_count': business.view_count})
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured businesses"""
        featured_businesses = self.get_queryset().filter(is_featured=True)[:6]
        serializer = BusinessListSerializer(featured_businesses, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_sector(self, request):
        """Get businesses filtered by sector slug"""
        sector_slug = request.query_params.get('sector')
        if sector_slug:
            businesses = self.get_queryset().filter(sector__slug=sector_slug)
            serializer = BusinessListSerializer(businesses, many=True)
            return Response(serializer.data)
        return Response({'error': 'sector parameter required'}, status=400)
    
    @action(detail=False, methods=['get'])
    def by_slug(self, request):
        """Get a single business by slug (alternative endpoint)"""
        slug = request.query_params.get('slug')
        if slug:
            business = get_object_or_404(Business, slug=slug, is_deleted=False)
            serializer = BusinessDetailSerializer(business)
            return Response(serializer.data)
        return Response({'error': 'slug parameter required'}, status=400)


class BusinessScaleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for BusinessScale model.
    Read-only for public users.
    """
    
    queryset = BusinessScale.objects.all().select_related('business')
    serializer_class = BusinessScaleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['business', 'scale_type']


# ============================================
# BUSINESS PROFILE VIEWSETS (with slug support)
# ============================================

class BusinessProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for BusinessProfile model.
    
    Manages profiles of interviewed businesses and partners.
    Supports lookup by ID or slug.
    Public: Read-only access to published profiles
    Admin: Full CRUD access
    """
    
    queryset = BusinessProfile.objects.filter(is_deleted=False).select_related('sector')
    serializer_class = BusinessProfileSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'owner_name', 'description', 'location']
    filterset_fields = [
        'sector', 'status', 'is_partner', 'is_verified', 
        'is_featured', 'location', 'partner_type'
    ]
    ordering_fields = ['name', 'view_count', 'created_at', 'founded_year']
    ordering = ['-is_featured', '-is_verified', 'name']
    lookup_field = 'slug'
    lookup_value_regex = '[^/]+'
    
    def get_serializer_class(self):
        if self.action == 'list':
            return BusinessProfileListSerializer
        elif self.action == 'retrieve':
            return BusinessProfileDetailSerializer
        return BusinessProfileSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Non-admin users only see published profiles
        if not self.request.user.is_staff:
            queryset = queryset.filter(status='published')
        
        return queryset
    
    def get_object(self):
        """
        Override get_object to support lookup by either ID or slug.
        """
        lookup_value = self.kwargs.get(self.lookup_field)
        
        # Try to find by ID first (if numeric)
        if lookup_value and lookup_value.isdigit():
            obj = get_object_or_404(BusinessProfile, pk=lookup_value, is_deleted=False)
        else:
            # Otherwise try by slug
            obj = get_object_or_404(BusinessProfile, slug=lookup_value, is_deleted=False)
        
        # Check permissions
        self.check_object_permissions(self.request, obj)
        
        return obj
    
    def retrieve(self, request, *args, **kwargs):
        """Get business profile with view count increment"""
        instance = self.get_object()
        instance.increment_view_count()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured business profiles"""
        featured = self.get_queryset().filter(is_featured=True)[:6]
        serializer = BusinessProfileListSerializer(featured, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def partners(self, request):
        """Get partner directory listings"""
        partners = self.get_queryset().filter(is_partner=True, is_verified=True)[:20]
        serializer = PartnerDirectorySerializer(partners, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_sector(self, request):
        """Get business profiles filtered by sector slug"""
        sector_slug = request.query_params.get('sector')
        if sector_slug:
            profiles = self.get_queryset().filter(sector__slug=sector_slug)
            serializer = BusinessProfileListSerializer(profiles, many=True)
            return Response(serializer.data)
        return Response({'error': 'sector parameter required'}, status=400)
    
    @action(detail=False, methods=['get'])
    def verified(self, request):
        """Get only verified business profiles"""
        verified = self.get_queryset().filter(is_verified=True)[:50]
        serializer = BusinessProfileListSerializer(verified, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def increment_view(self, request, pk=None):
        """Increment view count for a business profile"""
        profile = self.get_object()
        profile.increment_view_count()
        return Response({'view_count': profile.view_count})


# ============================================
# BUSINESS PROFILE FEATURE VIEWSET
# ============================================

class BusinessProfileFeatureViewSet(viewsets.ModelViewSet):
    """
    ViewSet for BusinessProfileFeature model.
    Admin only for write operations.
    """
    
    queryset = BusinessProfileFeature.objects.all()
    serializer_class = BusinessProfileFeatureSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['business_profile']
    ordering_fields = ['order']
    ordering = ['order']


# ============================================
# BUSINESS PROFILE TESTIMONIAL VIEWSET
# ============================================

class BusinessProfileTestimonialViewSet(viewsets.ModelViewSet):
    """
    ViewSet for BusinessProfileTestimonial model.
    Admin only for write operations.
    """
    
    queryset = BusinessProfileTestimonial.objects.all()
    serializer_class = BusinessProfileTestimonialSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['business_profile', 'is_featured']
    ordering_fields = ['order']
    ordering = ['order']
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured testimonials for homepage"""
        featured = self.get_queryset().filter(is_featured=True)[:6]
        serializer = BusinessProfileTestimonialSerializer(featured, many=True)
        return Response(serializer.data)