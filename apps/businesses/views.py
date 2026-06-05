"""
apps/businesses/views.py

ViewSets for Business intelligence models.
Includes support for IntelligenceSnapshot (primary read model) and comparisons.
"""

from rest_framework import viewsets, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from django.db.models import Avg, Count, F, Q
from decimal import Decimal

from apps.core.pagination import StandardPagination
from apps.core.permissions import IsAdminOrReadOnly
from .models import (
    Business, BusinessScale, CapitalItem, OperatingCost, RevenueProjection,
    FinancialMetric, Risk, FeasibilityFactor, OperationsChecklist,
    BusinessProfile, BusinessProfileFeature, BusinessProfileTestimonial,
    IntelligenceSnapshot, TimeSeriesMetric
)
from .serializers import (
    BusinessSerializer, BusinessListSerializer, BusinessDetailSerializer,
    BusinessScaleSerializer, CapitalItemSerializer, OperatingCostSerializer,
    RevenueProjectionSerializer, FinancialMetricSerializer, RiskSerializer,
    FeasibilityFactorSerializer, OperationsChecklistSerializer,
    BusinessProfileSerializer, BusinessProfileListSerializer,
    BusinessProfileDetailSerializer, PartnerDirectorySerializer,
    BusinessProfileFeatureSerializer, BusinessProfileTestimonialSerializer,
    IntelligenceSnapshotSerializer, IntelligenceSnapshotListSerializer,
    TimeSeriesMetricSerializer, BusinessComparisonSerializer,
    SectorDashboardSerializer, YearOverYearTrendSerializer
)


# ============================================
# BUSINESS VIEWSET
# ============================================

class BusinessViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Business model.
    
    Provides CRUD operations for business profiles.
    Supports lookup by ID or slug.
    Public: Read-only access to published businesses
    Admin: Full CRUD access
    """
    
    queryset = Business.objects.filter(is_deleted=False).select_related('sector')
    serializer_class = BusinessSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'short_description', 'overview', 'opportunity_thesis']
    filterset_fields = ['sector', 'status', 'is_featured', 'has_scales']
    ordering_fields = ['name', 'view_count', 'created_at', 'updated_at']
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
        
        try:
            import uuid
            uuid.UUID(str(lookup_value))
            obj = get_object_or_404(Business, pk=lookup_value, is_deleted=False)
        except (ValueError, TypeError):
            obj = get_object_or_404(Business, slug=lookup_value, is_deleted=False)
        
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
    def with_snapshots(self, request):
        """Get businesses that have published snapshots"""
        business_ids = IntelligenceSnapshot.objects.filter(
            status='published', is_latest=True
        ).values_list('business_id', flat=True).distinct()
        
        businesses = self.get_queryset().filter(id__in=business_ids)
        serializer = BusinessListSerializer(businesses, many=True)
        return Response(serializer.data)


# ============================================
# BUSINESS SCALE VIEWSET
# ============================================

class BusinessScaleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for BusinessScale model.
    Read-only for public users.
    NOTE: BusinessScale does NOT have is_deleted field (doesn't inherit BaseModel)
    """
    
    queryset = BusinessScale.objects.select_related('business', 'primary_source')
    serializer_class = BusinessScaleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['business', 'scale_type', 'year']
    ordering_fields = ['year', 'scale_type']
    ordering = ['-year', 'scale_type']


# ============================================
# INTELLIGENCE SNAPSHOT VIEWSET (PRIMARY READ MODEL)
# ============================================

class IntelligenceSnapshotViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for IntelligenceSnapshot - the primary read model.
    
    This is what frontend and API clients should use for business intelligence data.
    Supports filtering, comparison, and year-over-year trends.
    
    Permission levels:
    - Free: Small scale only
    - Premium: Small + Medium scale
    - Pro: All scales
    - Enterprise: All scales + API access
    """
    
    queryset = IntelligenceSnapshot.objects.filter(
        status='published', is_latest=True
    ).select_related('business', 'primary_source')
    serializer_class = IntelligenceSnapshotSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['business_name', 'business_slug']
    ordering_fields = ['year', 'startup_cost', 'gross_margin_pct', 'payback_months']
    ordering = ['-year', 'business_name']
    
    def get_queryset(self):
        """Apply access control based on user tier"""
        queryset = super().get_queryset()
        user = self.request.user
        
        # Apply scale filtering based on subscription tier
        if not user.is_authenticated or user.tier == 'free':
            # Free tier: small scale only
            queryset = queryset.filter(Q(scale_type='small') | Q(scale_type__isnull=True))
        elif user.tier == 'premium':
            # Premium: small and medium scales
            queryset = queryset.filter(Q(scale_type__in=['small', 'medium']) | Q(scale_type__isnull=True))
        # Pro and Enterprise: all scales
        
        # Filter by query parameters
        sector = self.request.query_params.get('sector')
        if sector:
            queryset = queryset.filter(sector_id=sector)
        
        year = self.request.query_params.get('year')
        if year:
            queryset = queryset.filter(year=year)
        
        scale = self.request.query_params.get('scale')
        if scale:
            queryset = queryset.filter(scale_type=scale)
        
        # Min/max filters for comparison tool
        min_margin = self.request.query_params.get('min_margin')
        if min_margin:
            queryset = queryset.filter(gross_margin_pct__gte=Decimal(min_margin))
        
        max_startup = self.request.query_params.get('max_startup')
        if max_startup:
            queryset = queryset.filter(startup_cost__lte=int(max_startup))
        
        max_payback = self.request.query_params.get('max_payback')
        if max_payback:
            queryset = queryset.filter(payback_months__lte=Decimal(max_payback))
        
        return queryset
    
    def get_serializer_class(self):
        """Use list serializer for list action for better performance"""
        if self.action == 'list':
            return IntelligenceSnapshotListSerializer
        return IntelligenceSnapshotSerializer
    
    @action(detail=False, methods=['get'], url_path='compare')
    def compare(self, request):
        """
        Compare multiple businesses side-by-side.
        Report Type B & E: Compare Two Businesses / Investor Comparison Matrix
        
        Query params:
        - ids: comma-separated list of snapshot IDs
        - businesses: comma-separated list of business IDs (gets latest snapshot for each)
        - year: year to compare (default: latest)
        - scale: scale to compare (default: medium)
        """
        snapshot_ids = request.query_params.get('ids', '').split(',')
        business_ids = request.query_params.get('businesses', '').split(',')
        year = request.query_params.get('year')
        scale = request.query_params.get('scale', 'medium')
        
        queryset = self.get_queryset()
        
        # Filter by snapshot IDs
        if snapshot_ids and snapshot_ids[0]:
            queryset = queryset.filter(id__in=snapshot_ids)
        
        # Filter by business IDs (get latest for each)
        elif business_ids and business_ids[0]:
            business_filters = Q()
            for biz_id in business_ids:
                business_filters |= Q(business_id=biz_id)
            
            if year:
                queryset = queryset.filter(business_filters, year=year, scale_type=scale)
            else:
                # Get latest year for each business
                latest_snapshots = []
                for biz_id in business_ids:
                    latest = queryset.filter(business_id=biz_id).order_by('-year').first()
                    if latest:
                        latest_snapshots.append(latest)
                queryset = latest_snapshots
        
        # Build comparison data
        comparison_data = []
        for snapshot in queryset:
            comparison_data.append({
                'business_id': snapshot.business_id,
                'business_name': snapshot.business_name,
                'business_slug': snapshot.business_slug,
                'sector_name': snapshot.business.sector.name if snapshot.business.sector else None,
                'scale_type': snapshot.scale_type,
                'year': snapshot.year,
                'startup_cost': snapshot.startup_cost,
                'gross_margin_pct': snapshot.gross_margin_pct,
                'payback_months': snapshot.payback_months,
                'feasibility_score': snapshot.feasibility_score,
                'risk_score': snapshot.risk_score,
                'min_investment': snapshot.min_investment,
                'max_investment': snapshot.max_investment,
            })
        
        serializer = BusinessComparisonSerializer(comparison_data, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='sector-dashboard/(?P<sector_id>[^/.]+)')
    def sector_dashboard(self, request, sector_id=None):
        """
        Get sector dashboard with aggregated metrics.
        Report Type C: Sector Dashboard
        
        Query params:
        - year: year to analyze (default: current year)
        """
        year = request.query_params.get('year', '2024')
        
        snapshots = self.get_queryset().filter(
            sector_id=sector_id,
            year=year
        )
        
        if not snapshots.exists():
            return Response({
                'sector_id': sector_id,
                'year': year,
                'total_businesses': 0,
                'message': 'No data available for this sector and year'
            })
        
        # Get sector name from first snapshot
        sector_name = snapshots.first().business.sector.name if snapshots.first().business.sector else None
        
        # Aggregated metrics
        aggregated = snapshots.aggregate(
            total_businesses=Count('id', distinct=True),
            avg_startup_cost=Avg('startup_cost'),
            avg_gross_margin=Avg('gross_margin_pct'),
            avg_payback_months=Avg('payback_months'),
            avg_feasibility=Avg('feasibility_score'),
            avg_risk_score=Avg('risk_score'),
        )
        
        # Count by scale
        scale_counts = {
            'small': snapshots.filter(scale_type='small').count(),
            'medium': snapshots.filter(scale_type='medium').count(),
            'large': snapshots.filter(scale_type='large').count(),
        }
        
        # Get top opportunities from snapshot data (extract from JSON)
        opportunities = []
        for snapshot in snapshots[:10]:
            if snapshot.data and 'opportunities' in snapshot.data:
                for opp in snapshot.data['opportunities'][:3]:
                    opportunities.append({
                        'business': snapshot.business_name,
                        'name': opp.get('name'),
                        'description': opp.get('description'),
                        'investment_range': opp.get('investment_range'),
                    })
        
        dashboard_data = {
            'sector_id': sector_id,
            'sector_name': sector_name,
            'year': int(year),
            'total_businesses': aggregated['total_businesses'] or 0,
            'avg_startup_cost': aggregated['avg_startup_cost'],
            'avg_gross_margin': aggregated['avg_gross_margin'],
            'avg_payback_months': aggregated['avg_payback_months'],
            'avg_feasibility': aggregated['avg_feasibility'],
            'avg_risk_score': aggregated['avg_risk_score'],
            'by_scale': scale_counts,
            'top_opportunities': opportunities[:10],
        }
        
        serializer = SectorDashboardSerializer(dashboard_data)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='trend/(?P<business_id>[^/.]+)')
    def year_over_year_trend(self, request, business_id=None):
        """
        Get year-over-year trend for a specific business.
        Report Type D: Year-Over-Year Trend
        
        Query params:
        - scale: scale to analyze (default: medium)
        - metrics: comma-separated list of metrics (default: all)
        """
        scale = request.query_params.get('scale', 'medium')
        metrics_param = request.query_params.get('metrics', '')
        
        # Default metrics to track
        default_metrics = ['startup_cost', 'gross_margin_pct', 'payback_months', 'feasibility_score', 'risk_score']
        
        if metrics_param:
            metrics = metrics_param.split(',')
        else:
            metrics = default_metrics
        
        # Get all snapshots for this business
        snapshots = IntelligenceSnapshot.objects.filter(
            business_id=business_id,
            scale_type=scale,
            status='published',
            is_latest=True
        ).order_by('year')
        
        if not snapshots.exists():
            return Response({
                'business_id': business_id,
                'scale_type': scale,
                'message': 'No trend data available'
            })
        
        # Build trend data
        trends = {}
        for metric in metrics:
            trends[metric] = []
            for snapshot in snapshots:
                value = getattr(snapshot, metric, None)
                trends[metric].append({
                    'year': snapshot.year,
                    'value': float(value) if value is not None else None
                })
        
        business_name = snapshots.first().business_name
        
        trend_data = {
            'business_id': business_id,
            'business_name': business_name,
            'scale_type': scale,
            'trends': trends,
        }
        
        serializer = YearOverYearTrendSerializer(trend_data)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='by-business/(?P<slug>[^/.]+)')

    def get_by_business_slug(self, request, slug=None):
        """
        Get intelligence snapshot by business slug.
        Usage: /api/v1/intelligence/by-business/poultry-farming-broilers/?scale=medium&year=2024
        """
        from .models import Business
        
        # Get the business
        business = get_object_or_404(Business, slug=slug, is_deleted=False)
        
        # Get query parameters
        scale = request.query_params.get('scale', 'medium')
        year = request.query_params.get('year', '2024')
        
        # Check user tier access
        user = request.user
        if not user.is_authenticated or getattr(user, 'tier', 'free') == 'free':
            if scale not in ['small', None]:
                return Response(
                    {'error': f'Upgrade to Premium to access {scale} scale data', 'premium_locked': True},
                    status=status.HTTP_403_FORBIDDEN
                )
        elif getattr(user, 'tier', 'free') == 'premium':
            if scale == 'large':
                return Response(
                    {'error': 'Upgrade to Pro to access large scale data', 'premium_locked': True},
                    status=status.HTTP_403_FORBIDDEN
                )
        
        # Get the snapshot
        snapshot = IntelligenceSnapshot.objects.filter(
            business=business,
            scale_type=scale,
            year=int(year),
            status='published',
            is_latest=True
        ).first()
        
        if not snapshot:
            return Response(
                {'detail': f'No intelligence data found for {business.name} at {scale} scale for {year}'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.get_serializer(snapshot)
        return Response(serializer.data)


        @action(detail=False, methods=['get'], url_path='available-years')
        def available_years(self, request):
            """Get all available years for snapshots"""
            years = self.get_queryset().values_list('year', flat=True).distinct().order_by('-year')
            return Response(list(years))
        
        @action(detail=False, methods=['get'], url_path='investment-filter')
        def investment_filter(self, request):
            """
            Filter businesses by investment amount.
            Useful for diaspora investors with specific budgets.
            """
            min_investment = request.query_params.get('min', 0)
            max_investment = request.query_params.get('max')
            
            queryset = self.get_queryset()
            
            if min_investment:
                queryset = queryset.filter(
                    Q(min_investment__gte=min_investment) | Q(startup_cost__gte=min_investment)
                )
            
            if max_investment:
                queryset = queryset.filter(
                    Q(max_investment__lte=max_investment) | Q(startup_cost__lte=max_investment)
                )
            
            # Return simplified list for quick scanning
            results = queryset.values(
                'id', 'business_name', 'business_slug', 'scale_type', 'year',
                'startup_cost', 'gross_margin_pct', 'payback_months', 'feasibility_score'
            )
            
            return Response(results)


# ============================================
# TIME SERIES METRIC VIEWSET
# ============================================

class TimeSeriesMetricViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for TimeSeriesMetric.
    Provides fast access to year-over-year metric changes.
    """
    
    queryset = TimeSeriesMetric.objects.select_related('business', 'source')
    serializer_class = TimeSeriesMetricSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['business', 'metric_name', 'year', 'scale_type']
    ordering_fields = ['year', 'value_numeric']
    ordering = ['business', '-year']
    
    @action(detail=False, methods=['get'], url_path='trend')
    def metric_trend(self, request):
        """
        Get trend for a specific metric across years.
        Query params: business_id, metric_name, scale_type (optional)
        """
        business_id = request.query_params.get('business_id')
        metric_name = request.query_params.get('metric_name')
        scale_type = request.query_params.get('scale_type')
        
        if not business_id or not metric_name:
            return Response({'error': 'business_id and metric_name required'}, status=400)
        
        queryset = self.get_queryset().filter(
            business_id=business_id,
            metric_name=metric_name
        )
        
        if scale_type:
            queryset = queryset.filter(scale_type=scale_type)
        
        data = [
            {'year': item.year, 'value': float(item.value_numeric)}
            for item in queryset.order_by('year')
        ]
        
        return Response({
            'business_id': business_id,
            'metric_name': metric_name,
            'scale_type': scale_type,
            'values': data
        })


# ============================================
# CAPITAL ITEM VIEWSET
# ============================================

class CapitalItemViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only ViewSet for CapitalItem"""
    
    queryset = CapitalItem.objects.select_related('scale__business', 'source')
    serializer_class = CapitalItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['scale', 'category', 'priority']


# ============================================
# OPERATING COST VIEWSET
# ============================================

class OperatingCostViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only ViewSet for OperatingCost"""
    
    queryset = OperatingCost.objects.select_related('scale__business', 'source')
    serializer_class = OperatingCostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['scale', 'cost_category', 'period_type']


# ============================================
# REVENUE PROJECTION VIEWSET
# ============================================

class RevenueProjectionViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only ViewSet for RevenueProjection"""
    
    queryset = RevenueProjection.objects.select_related('scale__business', 'source')
    serializer_class = RevenueProjectionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['scale', 'period_type']


# ============================================
# FINANCIAL METRIC VIEWSET
# ============================================

class FinancialMetricViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only ViewSet for FinancialMetric"""
    
    queryset = FinancialMetric.objects.select_related('scale__business', 'source')
    serializer_class = FinancialMetricSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['scale', 'is_primary']


# ============================================
# RISK VIEWSET
# ============================================

class RiskViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only ViewSet for Risk"""
    
    queryset = Risk.objects.select_related('scale__business', 'source')
    serializer_class = RiskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['scale', 'category']


# ============================================
# FEASIBILITY FACTOR VIEWSET
# ============================================

class FeasibilityFactorViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only ViewSet for FeasibilityFactor"""
    
    queryset = FeasibilityFactor.objects.select_related('scale__business', 'source')
    serializer_class = FeasibilityFactorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['scale', 'category']


# ============================================
# OPERATIONS CHECKLIST VIEWSET
# ============================================

class OperationsChecklistViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only ViewSet for OperationsChecklist"""
    
    queryset = OperationsChecklist.objects.select_related('business')
    serializer_class = OperationsChecklistSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['business', 'scale_type', 'task_type']
    ordering_fields = ['order']
    ordering = ['order']


# ============================================
# BUSINESS PROFILE VIEWSETS
# ============================================

class BusinessProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for BusinessProfile model.
    
    Manages profiles of interviewed businesses and partners.
    Supports lookup by ID or slug.
    Public: Read-only access to published profiles
    Admin: Full CRUD access
    """
    
    queryset = BusinessProfile.objects.filter(is_deleted=False).select_related('sector', 'business_type')
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
        
        try:
            import uuid
            uuid.UUID(str(lookup_value))
            obj = get_object_or_404(BusinessProfile, pk=lookup_value, is_deleted=False)
        except (ValueError, TypeError):
            obj = get_object_or_404(BusinessProfile, slug=lookup_value, is_deleted=False)
        
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