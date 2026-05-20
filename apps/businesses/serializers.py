from rest_framework import serializers
from .models import *
from apps.sectors.serializers import SectorListSerializer


# ============================================
# NESTED SERIALIZERS
# ============================================

class CapitalItemSerializer(serializers.ModelSerializer):
    """Serializer for CapitalItem"""
    
    total_cost_display = serializers.SerializerMethodField()
    category_display = serializers.SerializerMethodField()
    
    class Meta:
        model = CapitalItem
        fields = [
            'id', 'category', 'category_display', 'item_name',
            'quantity', 'unit_cost', 'total_cost', 'total_cost_display',
            'priority', 'notes'
        ]
    
    def get_total_cost_display(self, obj):
        return f"D{obj.total_cost:,}"
    
    def get_category_display(self, obj):
        categories = {
            'registration': 'Registration & Legal',
            'premises': 'Premises & Housing',
            'equipment': 'Equipment & Tools',
            'inventory': 'Initial Inventory',
        }
        return categories.get(obj.category, obj.category)


class OperatingCostSerializer(serializers.ModelSerializer):
    """Serializer for OperatingCost"""
    
    total_display = serializers.SerializerMethodField()
    
    class Meta:
        model = OperatingCost
        fields = [
            'id', 'week_range', 'feed_starter', 'feed_grower',
            'feed_finisher', 'utilities', 'water', 'medication',
            'labor', 'transport_misc', 'total', 'total_display'
        ]
    
    def get_total_display(self, obj):
        return f"D{obj.total:,}"


class RevenueProjectionSerializer(serializers.ModelSerializer):
    """Serializer for RevenueProjection"""
    
    total_revenue_display = serializers.SerializerMethodField()
    gross_profit_display = serializers.SerializerMethodField()
    net_profit_display = serializers.SerializerMethodField()
    cumulative_cash_flow_display = serializers.SerializerMethodField()
    
    class Meta:
        model = RevenueProjection
        fields = [
            'id', 'cycle_number', 'unit_sales', 'price_per_unit',
            'total_revenue', 'total_revenue_display', 'cost_of_goods',
            'gross_profit', 'gross_profit_display', 'operating_expenses',
            'net_profit', 'net_profit_display', 'cumulative_cash_flow',
            'cumulative_cash_flow_display'
        ]
    
    def get_total_revenue_display(self, obj):
        return f"D{obj.total_revenue:,}"
    
    def get_gross_profit_display(self, obj):
        return f"D{obj.gross_profit:,}"
    
    def get_net_profit_display(self, obj):
        return f"D{obj.net_profit:,}"
    
    def get_cumulative_cash_flow_display(self, obj):
        return f"D{obj.cumulative_cash_flow:,}"


class FinancialMetricSerializer(serializers.ModelSerializer):
    """Serializer for FinancialMetric"""
    
    class Meta:
        model = FinancialMetric
        fields = [
            'id', 'breakeven_cycles', 'gross_margin_percent',
            'net_margin_percent', 'roi_percent', 'payback_months',
            'data_source', 'last_updated'
        ]


class RiskSerializer(serializers.ModelSerializer):
    """Serializer for Risk"""
    
    category_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Risk
        fields = [
            'id', 'category', 'category_display', 'specific_risk',
            'likelihood', 'impact', 'risk_score', 'mitigation_strategy'
        ]
    
    def get_category_display(self, obj):
        return obj.get_category_display()


class FeasibilityFactorSerializer(serializers.ModelSerializer):
    """Serializer for FeasibilityFactor"""
    
    category_display = serializers.SerializerMethodField()
    
    class Meta:
        model = FeasibilityFactor
        fields = [
            'id', 'category', 'category_display', 'sub_category',
            'rating', 'notes', 'data_source', 'last_updated'
        ]
    
    def get_category_display(self, obj):
        return obj.get_category_display()


class OperationsChecklistSerializer(serializers.ModelSerializer):
    """Serializer for OperationsChecklist"""
    
    scale_type_display = serializers.SerializerMethodField()
    task_type_display = serializers.SerializerMethodField()
    
    class Meta:
        model = OperationsChecklist
        fields = [
            'id', 'scale_type', 'scale_type_display', 'task_type',
            'task_type_display', 'task_name', 'description',
            'time_of_day', 'responsible', 'duration_minutes', 'order'
        ]
    
    def get_scale_type_display(self, obj):
        if obj.scale_type == 'all':
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
    
    class Meta:
        model = BusinessScale
        fields = [
            'id', 'scale_type', 'scale_type_display', 'capacity_definition',
            'target_market', 'location_type', 'labor_needed',
            'overall_feasibility_score', 'last_updated',
            'capital_items', 'operating_costs', 'revenue_projections',
            'financial_metrics', 'risks', 'feasibility_factors'
        ]
    
    def get_scale_type_display(self, obj):
        return obj.get_scale_type_display()


# ============================================
# BUSINESS SERIALIZERS
# ============================================

class BusinessListSerializer(serializers.ModelSerializer):
    """Minimal serializer for business list views"""
    
    sector_name = serializers.ReadOnlyField(source='sector.name')
    sector_slug = serializers.ReadOnlyField(source='sector.slug')
    
    class Meta:
        model = Business
        fields = [
            'id', 'name', 'slug', 'short_description',
            'sector', 'sector_name', 'sector_slug',
            'featured_image', 'is_featured', 'view_count'
        ]


class BusinessDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for single business view"""
    
    sector = SectorListSerializer(read_only=True)
    scales = BusinessScaleSerializer(many=True, read_only=True)
    checklists = OperationsChecklistSerializer(many=True, read_only=True)
    status_display = serializers.ReadOnlyField(source='get_status_display')
    
    class Meta:
        model = Business
        fields = [
            'id', 'name', 'slug', 'sector', 'short_description',
            'overview', 'opportunity_thesis', 'featured_image',
            'status', 'status_display', 'is_featured',
            'view_count', 'scales', 'checklists',
            'created_at', 'updated_at'
        ]


class BusinessSerializer(serializers.ModelSerializer):
    """Base serializer for CRUD operations"""
    
    class Meta:
        model = Business
        fields = '__all__'


# ============================================
# BUSINESS PROFILE SERIALIZERS
# ============================================

class BusinessProfileFeatureSerializer(serializers.ModelSerializer):
    """Serializer for BusinessProfileFeature"""
    
    class Meta:
        model = BusinessProfileFeature
        fields = [
            'id', 'title', 'description', 'icon', 'order'
        ]


class BusinessProfileTestimonialSerializer(serializers.ModelSerializer):
    """Serializer for BusinessProfileTestimonial"""
    
    class Meta:
        model = BusinessProfileTestimonial
        fields = [
            'id', 'quote', 'author_name', 'author_position', 
            'is_featured', 'order'
        ]


class BusinessProfileListSerializer(serializers.ModelSerializer):
    """Minimal serializer for business profile list views"""
    
    sector_name = serializers.ReadOnlyField(source='sector.name')
    sector_slug = serializers.ReadOnlyField(source='sector.slug')
    
    class Meta:
        model = BusinessProfile
        fields = [
            'id', 'name', 'slug', 'owner_name', 'short_description',
            'logo', 'cover_image', 'location', 'sector', 'sector_name',
            'sector_slug', 'is_partner', 'is_verified', 'is_featured',
            'partner_type', 'view_count'
        ]


class BusinessProfileDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for single business profile view"""
    
    sector_name = serializers.ReadOnlyField(source='sector.name')
    sector_slug = serializers.ReadOnlyField(source='sector.slug')
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
            'founded_year', 'employee_count', 'business_type',
            'sector', 'sector_name', 'sector_slug',
            'is_partner', 'is_verified', 'is_featured', 'partner_type',
            'partner_type_display', 'interview_date', 'interviewed_by',
            'status', 'status_display', 'view_count',
            'features', 'testimonials',
            'created_at', 'updated_at'
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
    
    class Meta:
        model = BusinessProfile
        fields = [
            'id', 'name', 'slug', 'owner_name', 'short_description',
            'logo', 'location', 'sector', 'sector_name',
            'partner_type', 'phone', 'email', 'website',
            'is_verified', 'view_count'
        ]