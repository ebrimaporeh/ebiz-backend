"""
apps/businesses/serializers.py

Serializers for Business intelligence models.
"""

from rest_framework import serializers

from .models import (
    Business, BusinessScale, CapitalItem, OperatingCost, OperatingCostCategory,
    RevenueProjection, FinancialMetric, Risk, FeasibilityFactor,
    OperationsChecklist, BusinessProfile, BusinessProfileFeature,
    BusinessProfileTestimonial, IntelligenceSnapshot, TimeSeriesMetric
)
from apps.sectors.serializers import SectorListSerializer
from apps.core.serializers import SourceSerializer  # We'll create this


# ============================================
# CAPITAL ITEM SERIALIZER
# ============================================

class CapitalItemSerializer(serializers.ModelSerializer):
    """Serializer for CapitalItem (startup costs)"""
    
    total_cost_display = serializers.SerializerMethodField()
    category_display = serializers.SerializerMethodField()
    priority_display = serializers.SerializerMethodField()
    source_name = serializers.ReadOnlyField(source='source.name', default=None)
    
    class Meta:
        model = CapitalItem
        fields = [
            'id', 'category', 'category_display', 'item_name',
            'quantity', 'unit_cost', 'total_cost', 'total_cost_display',
            'priority', 'priority_display', 'notes', 'source_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'total_cost', 'created_at', 'updated_at']
    
    def get_total_cost_display(self, obj):
        return f"D{obj.total_cost:,}"
    
    def get_category_display(self, obj):
        return obj.get_category_display()
    
    def get_priority_display(self, obj):
        return obj.get_priority_display()


# ============================================
# OPERATING COST SERIALIZER
# ============================================

class OperatingCostSerializer(serializers.ModelSerializer):
    """Serializer for OperatingCost (flexible period costs)"""
    
    amount_display = serializers.SerializerMethodField()
    period_label = serializers.ReadOnlyField()
    cost_category_display = serializers.SerializerMethodField()
    period_type_display = serializers.SerializerMethodField()
    source_name = serializers.ReadOnlyField(source='source.name', default=None)
    
    class Meta:
        model = OperatingCost
        fields = [
            'id', 'period_number', 'period_type', 'period_type_display',
            'period_label', 'cost_category', 'cost_category_display',
            'amount_dalasi', 'amount_display', 'notes', 'source_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_amount_display(self, obj):
        return f"D{obj.amount_dalasi:,}"
    
    def get_cost_category_display(self, obj):
        return obj.get_cost_category_display()
    
    def get_period_type_display(self, obj):
        return obj.get_period_type_display()


# ============================================
# REVENUE PROJECTION SERIALIZER
# ============================================

class RevenueProjectionSerializer(serializers.ModelSerializer):
    """Serializer for RevenueProjection"""
    
    total_revenue_display = serializers.SerializerMethodField()
    gross_profit_display = serializers.SerializerMethodField()
    net_profit_display = serializers.SerializerMethodField()
    cumulative_cash_flow_display = serializers.SerializerMethodField()
    period_label = serializers.ReadOnlyField()
    period_type_display = serializers.SerializerMethodField()
    source_name = serializers.ReadOnlyField(source='source.name', default=None)
    
    class Meta:
        model = RevenueProjection
        fields = [
            'id', 'period_number', 'period_type', 'period_type_display',
            'period_label', 'unit_sales', 'price_per_unit',
            'total_revenue', 'total_revenue_display', 'cost_of_goods',
            'gross_profit', 'gross_profit_display', 'operating_expenses',
            'net_profit', 'net_profit_display', 'cumulative_cash_flow',
            'cumulative_cash_flow_display', 'source_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'total_revenue', 'gross_profit', 'net_profit',
            'cumulative_cash_flow', 'created_at', 'updated_at'
        ]
    
    def get_total_revenue_display(self, obj):
        return f"D{obj.total_revenue:,}"
    
    def get_gross_profit_display(self, obj):
        return f"D{obj.gross_profit:,}"
    
    def get_net_profit_display(self, obj):
        return f"D{obj.net_profit:,}"
    
    def get_cumulative_cash_flow_display(self, obj):
        return f"D{obj.cumulative_cash_flow:,}"
    
    def get_period_type_display(self, obj):
        return obj.get_period_type_display()


# ============================================
# FINANCIAL METRIC SERIALIZER
# ============================================

class FinancialMetricSerializer(serializers.ModelSerializer):
    """Serializer for FinancialMetric (summary KPIs)"""
    
    source_name = serializers.ReadOnlyField(source='source.name', default=None)
    
    class Meta:
        model = FinancialMetric
        fields = [
            'id', 'breakeven_cycles', 'gross_margin_pct', 'net_margin_pct',
            'roi_pct', 'payback_months', 'is_primary', 'source_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


# ============================================
# RISK SERIALIZER
# ============================================

class RiskSerializer(serializers.ModelSerializer):
    """Serializer for Risk assessment"""
    
    category_display = serializers.SerializerMethodField()
    severity_label = serializers.ReadOnlyField()
    source_name = serializers.ReadOnlyField(source='source.name', default=None)
    
    class Meta:
        model = Risk
        fields = [
            'id', 'category', 'category_display', 'specific_risk',
            'likelihood', 'impact', 'risk_score', 'severity_label',
            'mitigation_strategy', 'source_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'risk_score', 'created_at', 'updated_at']
    
    def get_category_display(self, obj):
        return obj.get_category_display()


# ============================================
# FEASIBILITY FACTOR SERIALIZER
# ============================================

class FeasibilityFactorSerializer(serializers.ModelSerializer):
    """Serializer for FeasibilityFactor ratings"""
    
    category_display = serializers.SerializerMethodField()
    source_name = serializers.ReadOnlyField(source='source.name', default=None)
    
    class Meta:
        model = FeasibilityFactor
        fields = [
            'id', 'category', 'category_display', 'sub_category',
            'rating', 'notes', 'source_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_category_display(self, obj):
        return obj.get_category_display()


# ============================================
# OPERATIONS CHECKLIST SERIALIZER
# ============================================

class OperationsChecklistSerializer(serializers.ModelSerializer):
    """Serializer for OperationsChecklist (daily/weekly tasks)"""
    
    scale_type_display = serializers.SerializerMethodField()
    task_type_display = serializers.SerializerMethodField()
    
    class Meta:
        model = OperationsChecklist
        fields = [
            'id', 'scale_type', 'scale_type_display', 'task_type',
            'task_type_display', 'task_name', 'description',
            'time_of_day', 'responsible', 'duration_minutes', 'order'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_scale_type_display(self, obj):
        if not obj.scale_type:
            return 'All Scales'
        return obj.get_scale_type_display()
    
    def get_task_type_display(self, obj):
        return obj.get_task_type_display()


# ============================================
# BUSINESS SCALE SERIALIZER
# ============================================

class BusinessScaleSerializer(serializers.ModelSerializer):
    """Complete serializer for BusinessScale with all nested data"""
    
    scale_type_display = serializers.SerializerMethodField()
    capital_items = CapitalItemSerializer(many=True, read_only=True)
    operating_costs = OperatingCostSerializer(many=True, read_only=True)
    revenue_projections = RevenueProjectionSerializer(many=True, read_only=True)
    financial_metrics = FinancialMetricSerializer(many=True, read_only=True)
    risks = RiskSerializer(many=True, read_only=True)
    feasibility_factors = FeasibilityFactorSerializer(many=True, read_only=True)
    total_startup_cost = serializers.SerializerMethodField()
    total_startup_cost_display = serializers.SerializerMethodField()
    
    class Meta:
        model = BusinessScale
        fields = [
            'id', 'scale_type', 'scale_type_display', 'year',
            'capacity_definition', 'target_market', 'location_type',
            'labor_needed', 'overall_feasibility_score',
            'total_startup_cost', 'total_startup_cost_display',
            'capital_items', 'operating_costs', 'revenue_projections',
            'financial_metrics', 'risks', 'feasibility_factors'
        ]
    
    def get_scale_type_display(self, obj):
        return obj.get_scale_type_display()
    
    def get_total_startup_cost(self, obj):
        return obj.total_startup_cost
    
    def get_total_startup_cost_display(self, obj):
        return f"D{obj.total_startup_cost:,}"


# ============================================
# BUSINESS SERIALIZERS
# ============================================

class BusinessListSerializer(serializers.ModelSerializer):
    """Minimal serializer for business list views"""
    
    sector_name = serializers.ReadOnlyField(source='sector.name')
    sector_slug = serializers.ReadOnlyField(source='sector.slug')
    sector_icon = serializers.ReadOnlyField(source='sector.icon')
    has_scales_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Business
        fields = [
            'id', 'name', 'slug', 'short_description', 'sector',
            'sector_name', 'sector_slug', 'sector_icon',
            'featured_image', 'has_scales', 'has_scales_display',
            'is_featured', 'view_count', 'status'
        ]
    
    def get_has_scales_display(self, obj):
        return "Yes" if obj.has_scales else "No"


class BusinessDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for single business view"""
    
    sector = SectorListSerializer(read_only=True)
    scales = serializers.SerializerMethodField()
    checklists = serializers.SerializerMethodField()
    status_display = serializers.ReadOnlyField(source='get_status_display')
    latest_snapshot = serializers.SerializerMethodField()
    
    class Meta:
        model = Business
        fields = [
            'id', 'name', 'slug', 'sector', 'short_description',
            'overview', 'opportunity_thesis', 'featured_image',
            'has_scales', 'status', 'status_display', 'is_featured',
            'summary_for_ai', 'view_count', 'scales', 'checklists',
            'latest_snapshot', 'created_at', 'updated_at'
        ]
    
    def get_scales(self, obj):
        """Return all published scales for this business"""
        scales = obj.scales.all().order_by('-year', 'scale_type')
        return BusinessScaleSerializer(scales, many=True).data
    
    def get_checklists(self, obj):
        """Return operations checklists for this business"""
        checklists = obj.checklists.all()
        return OperationsChecklistSerializer(checklists, many=True).data
    
    def get_latest_snapshot(self, obj):
        """Return the latest published intelligence snapshot"""
        snapshot = obj.snapshots.filter(
            status='published', is_latest=True
        ).order_by('-year').first()
        if snapshot:
            return IntelligenceSnapshotSerializer(snapshot, context=self.context).data
        return None


class BusinessSerializer(serializers.ModelSerializer):
    """Base serializer for CRUD operations"""
    
    class Meta:
        model = Business
        fields = '__all__'
        read_only_fields = ['id', 'slug', 'view_count', 'created_at', 'updated_at']


# ============================================
# INTELLIGENCE SNAPSHOT SERIALIZER (FRONTEND)
# ============================================

class IntelligenceSnapshotSerializer(serializers.ModelSerializer):
    """
    Serializer for IntelligenceSnapshot - the primary read model.
    Returns the complete denormalized data structure for frontend.
    """
    
    class Meta:
        model = IntelligenceSnapshot
        fields = [
            'id', 'business', 'scale_type', 'year', 'version',
            'is_latest', 'status', 'published_at', 'data',
            'startup_cost', 'gross_margin_pct', 'payback_months',
            'feasibility_score', 'risk_score', 'summary_text',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'version', 'is_latest', 'startup_cost',
            'gross_margin_pct', 'payback_months', 'feasibility_score',
            'risk_score', 'created_at', 'updated_at'
        ]
    
    def to_representation(self, instance):
        """Return the display_data (with computed display values)"""
        data = super().to_representation(instance)
        # Replace raw data with display-ready data
        data['display_data'] = instance.display_data
        return data


class IntelligenceSnapshotListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing snapshots (comparisons, filtering).
    """
    
    business_name = serializers.ReadOnlyField()
    business_slug = serializers.ReadOnlyField()
    sector_id = serializers.ReadOnlyField()
    
    class Meta:
        model = IntelligenceSnapshot
        fields = [
            'id', 'business', 'business_name', 'business_slug',
            'sector_id', 'scale_type', 'year', 'version',
            'is_latest', 'status', 'startup_cost', 'gross_margin_pct',
            'payback_months', 'feasibility_score', 'risk_score',
            'min_investment', 'max_investment'
        ]


# ============================================
# TIME SERIES METRIC SERIALIZER
# ============================================

class TimeSeriesMetricSerializer(serializers.ModelSerializer):
    """Serializer for TimeSeriesMetric (year-over-year trends)"""
    
    metric_name_display = serializers.SerializerMethodField()
    scale_type_display = serializers.SerializerMethodField()
    source_name = serializers.ReadOnlyField(source='source.name', default=None)
    
    class Meta:
        model = TimeSeriesMetric
        fields = [
            'id', 'business', 'scale_type', 'scale_type_display',
            'metric_name', 'metric_name_display', 'year',
            'value_numeric', 'source_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_metric_name_display(self, obj):
        return obj.get_metric_name_display()
    
    def get_scale_type_display(self, obj):
        return obj.get_scale_type_display() if obj.scale_type else None


# ============================================
# BUSINESS PROFILE SERIALIZERS
# ============================================

class BusinessProfileFeatureSerializer(serializers.ModelSerializer):
    """Serializer for BusinessProfileFeature"""
    
    class Meta:
        model = BusinessProfileFeature
        fields = ['id', 'title', 'description', 'icon', 'order']
        read_only_fields = ['id']


class BusinessProfileTestimonialSerializer(serializers.ModelSerializer):
    """Serializer for BusinessProfileTestimonial"""
    
    class Meta:
        model = BusinessProfileTestimonial
        fields = ['id', 'quote', 'author_name', 'author_position', 'is_featured', 'order']
        read_only_fields = ['id']


class BusinessProfileListSerializer(serializers.ModelSerializer):
    """Minimal serializer for business profile list views"""
    
    sector_name = serializers.ReadOnlyField(source='sector.name')
    sector_slug = serializers.ReadOnlyField(source='sector.slug')
    business_type_name = serializers.ReadOnlyField(source='business_type.name', default=None)
    
    class Meta:
        model = BusinessProfile
        fields = [
            'id', 'name', 'slug', 'owner_name', 'short_description',
            'logo', 'cover_image', 'location', 'sector', 'sector_name',
            'sector_slug', 'business_type', 'business_type_name',
            'is_partner', 'is_verified', 'is_featured',
            'partner_type', 'view_count'
        ]


class BusinessProfileDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for single business profile view"""
    
    sector_name = serializers.ReadOnlyField(source='sector.name')
    sector_slug = serializers.ReadOnlyField(source='sector.slug')
    business_type_name = serializers.ReadOnlyField(source='business_type.name', default=None)
    business_type_slug = serializers.ReadOnlyField(source='business_type.slug', default=None)
    features = BusinessProfileFeatureSerializer(many=True, read_only=True)
    testimonials = BusinessProfileTestimonialSerializer(many=True, read_only=True)
    status_display = serializers.ReadOnlyField(source='get_status_display')
    partner_type_display = serializers.ReadOnlyField()
    
    class Meta:
        model = BusinessProfile
        fields = [
            'id', 'name', 'slug', 'owner_name', 'owner_position',
            'description', 'short_description', 'logo', 'cover_image',
            'email', 'phone', 'website', 'address', 'location',
            'facebook', 'instagram', 'linkedin', 'twitter', 'tiktok', 'whatsapp',
            'founded_year', 'employee_count', 'business_type_legal',
            'sector', 'sector_name', 'sector_slug',
            'business_type', 'business_type_name', 'business_type_slug',
            'user', 'is_partner', 'is_verified', 'is_featured', 'partner_type',
            'partner_type_display', 'interview_date', 'interviewed_by',
            'interview_notes', 'status', 'status_display', 'view_count',
            'features', 'testimonials', 'created_at', 'updated_at'
        ]


class BusinessProfileSerializer(serializers.ModelSerializer):
    """Base serializer for CRUD operations"""
    
    class Meta:
        model = BusinessProfile
        fields = '__all__'
        read_only_fields = ['id', 'slug', 'view_count', 'created_at', 'updated_at']


# ============================================
# PARTNER DIRECTORY SERIALIZER
# ============================================

class PartnerDirectorySerializer(serializers.ModelSerializer):
    """Serializer for partner directory listing"""
    
    sector_name = serializers.ReadOnlyField(source='sector.name')
    sector_slug = serializers.ReadOnlyField(source='sector.slug')
    business_type_name = serializers.ReadOnlyField(source='business_type.name', default=None)
    partner_type_display = serializers.ReadOnlyField()
    
    class Meta:
        model = BusinessProfile
        fields = [
            'id', 'name', 'slug', 'owner_name', 'short_description',
            'logo', 'location', 'sector', 'sector_name', 'sector_slug',
            'business_type', 'business_type_name', 'partner_type',
            'partner_type_display', 'phone', 'email', 'website',
            'is_verified', 'view_count'
        ]


# ============================================
# COMPARISON SERIALIZER (Report Type B & E)
# ============================================

class BusinessComparisonSerializer(serializers.Serializer):
    """
    Serializer for comparing multiple businesses side-by-side.
    Used for Report Type B (Compare Two Businesses) and Report Type E (Investor Comparison Matrix).
    """
    
    business_id = serializers.UUIDField()
    business_name = serializers.CharField()
    business_slug = serializers.CharField()
    sector_name = serializers.CharField()
    scale_type = serializers.CharField()
    year = serializers.IntegerField()
    
    # Key comparison metrics
    startup_cost = serializers.IntegerField()
    startup_cost_display = serializers.SerializerMethodField()
    gross_margin_pct = serializers.DecimalField(max_digits=5, decimal_places=2)
    payback_months = serializers.DecimalField(max_digits=10, decimal_places=2)
    feasibility_score = serializers.DecimalField(max_digits=3, decimal_places=1)
    risk_score = serializers.IntegerField()
    min_investment = serializers.IntegerField()
    max_investment = serializers.IntegerField()
    
    def get_startup_cost_display(self, obj):
        return f"D{obj.get('startup_cost', 0):,}"
    
    class Meta:
        fields = [
            'business_id', 'business_name', 'business_slug', 'sector_name',
            'scale_type', 'year', 'startup_cost', 'startup_cost_display',
            'gross_margin_pct', 'payback_months', 'feasibility_score',
            'risk_score', 'min_investment', 'max_investment'
        ]


# ============================================
# SECTOR DASHBOARD SERIALIZER (Report Type C)
# ============================================

class SectorDashboardSerializer(serializers.Serializer):
    """Serializer for sector dashboard aggregation"""
    
    sector_id = serializers.UUIDField()
    sector_name = serializers.CharField()
    year = serializers.IntegerField()
    total_businesses = serializers.IntegerField()
    
    # Aggregated metrics
    avg_startup_cost = serializers.DecimalField(max_digits=20, decimal_places=2, allow_null=True)
    avg_gross_margin = serializers.DecimalField(max_digits=5, decimal_places=2, allow_null=True)
    avg_payback_months = serializers.DecimalField(max_digits=10, decimal_places=2, allow_null=True)
    avg_feasibility = serializers.DecimalField(max_digits=3, decimal_places=1, allow_null=True)
    avg_risk_score = serializers.DecimalField(max_digits=5, decimal_places=2, allow_null=True)
    
    # Breakdown by scale
    small_scale_count = serializers.IntegerField()
    medium_scale_count = serializers.IntegerField()
    large_scale_count = serializers.IntegerField()
    
    # Top opportunities
    top_opportunities = serializers.ListField(child=serializers.DictField(), required=False)


# ============================================
# YEAR-OVER-YEAR TREND SERIALIZER (Report Type D)
# ============================================

class YearOverYearTrendSerializer(serializers.Serializer):
    """Serializer for year-over-year trend analysis"""
    
    business_id = serializers.UUIDField()
    business_name = serializers.CharField()
    scale_type = serializers.CharField(allow_null=True)
    
    trends = serializers.DictField(child=serializers.ListField())
    
    def to_representation(self, instance):
        """Format trends for frontend chart consumption"""
        data = super().to_representation(instance)
        
        # Convert trend data to chart-friendly format
        if 'trends' in data:
            formatted_trends = {}
            for metric, values in data['trends'].items():
                formatted_trends[metric] = [
                    {'year': v.get('year'), 'value': float(v.get('value')) if v.get('value') else None}
                    for v in values
                ]
            data['trends'] = formatted_trends
        
        return data