from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import (
    Business, BusinessScale, CapitalItem, OperatingCost, RevenueProjection,
    FinancialMetric, Risk, FeasibilityFactor, OperationsChecklist,
    BusinessProfile, BusinessProfileFeature, BusinessProfileTestimonial,
    IntelligenceSnapshot, TimeSeriesMetric
)


class CapitalItemInline(admin.TabularInline):
    model = CapitalItem
    extra = 1
    fields = ['category', 'item_name', 'quantity', 'unit_cost', 'total_cost', 'priority', 'source', 'notes']
    readonly_fields = ['total_cost']


class OperatingCostInline(admin.TabularInline):
    model = OperatingCost
    extra = 1
    fields = ['period_number', 'period_type', 'cost_category', 'amount_dalasi', 'source', 'notes']
    readonly_fields = []


class RevenueProjectionInline(admin.TabularInline):
    model = RevenueProjection
    extra = 1
    fields = ['period_number', 'period_type', 'unit_sales', 'price_per_unit', 
              'total_revenue', 'cost_of_goods', 'gross_profit', 
              'operating_expenses', 'net_profit', 'cumulative_cash_flow', 'source']
    readonly_fields = ['total_revenue', 'gross_profit', 'net_profit']


class FinancialMetricInline(admin.TabularInline):
    model = FinancialMetric
    extra = 1
    fields = ['breakeven_cycles', 'gross_margin_pct', 'net_margin_pct', 
              'roi_pct', 'payback_months', 'is_primary', 'source']


class RiskInline(admin.TabularInline):
    model = Risk
    extra = 1
    fields = ['category', 'specific_risk', 'likelihood', 'impact', 'risk_score', 
              'mitigation_strategy', 'source']
    readonly_fields = ['risk_score']


class FeasibilityFactorInline(admin.TabularInline):
    model = FeasibilityFactor
    extra = 1
    fields = ['category', 'sub_category', 'rating', 'source', 'notes']


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ['name', 'sector', 'status', 'is_featured', 'view_count', 'has_scales']
    list_filter = ['status', 'is_featured', 'sector', 'has_scales']
    search_fields = ['name', 'short_description', 'overview']
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ('Basic Information', {
            'fields': ('sector', 'name', 'slug', 'short_description', 'overview', 'opportunity_thesis')
        }),
        ('Media', {
            'fields': ('featured_image',),
            'classes': ('collapse',)
        }),
        ('Settings', {
            'fields': ('has_scales', 'status', 'is_featured', 'summary_for_ai')
        }),
        ('Statistics', {
            'fields': ('view_count',),
            'classes': ('collapse',)
        }),
    )

    def get_prepopulated_fields(self, _request, obj=None):
        # slug is readonly for existing objects — disable prepopulate JS to avoid KeyError
        if obj:
            return {}
        return self.prepopulated_fields

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['slug', 'view_count', 'created_at', 'updated_at']
        return []


@admin.register(BusinessScale)
class BusinessScaleAdmin(admin.ModelAdmin):
    list_display = ['business_link', 'scale_type', 'year', 'capacity_definition', 'overall_feasibility_score']
    list_filter = ['scale_type', 'year', 'business__sector']
    search_fields = ['business__name', 'capacity_definition', 'target_market']
    
    inlines = [
        CapitalItemInline,
        OperatingCostInline,
        RevenueProjectionInline,
        FinancialMetricInline,
        RiskInline,
        FeasibilityFactorInline,
    ]
    
    def business_link(self, obj):
        url = reverse('admin:businesses_business_change', args=[obj.business.id])
        return format_html('<a href="{}">{}</a>', url, obj.business.name)
    business_link.short_description = 'Business'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('business', 'scale_type', 'year', 'capacity_definition', 
                      'target_market', 'location_type', 'labor_needed')
        }),
        ('Feasibility', {
            'fields': ('overall_feasibility_score', 'primary_source')
        }),
    )


@admin.register(CapitalItem)
class CapitalItemAdmin(admin.ModelAdmin):
    list_display = ['item_name', 'scale_link', 'category', 'quantity', 'unit_cost', 'total_cost', 'priority']
    list_filter = ['category', 'priority', 'scale__scale_type', 'scale__year']
    search_fields = ['item_name', 'notes']
    readonly_fields = ['total_cost']
    
    def scale_link(self, obj):
        url = reverse('admin:businesses_businessscale_change', args=[obj.scale.id])
        return format_html('<a href="{}">{}</a>', url, obj.scale)
    scale_link.short_description = 'Scale'


@admin.register(OperatingCost)
class OperatingCostAdmin(admin.ModelAdmin):
    list_display = ['scale_link', 'period_label', 'cost_category', 'amount_dalasi', 'period_type']
    list_filter = ['cost_category', 'period_type', 'scale__scale_type', 'scale__year']
    search_fields = ['scale__business__name', 'notes']
    
    def scale_link(self, obj):
        url = reverse('admin:businesses_businessscale_change', args=[obj.scale.id])
        return format_html('<a href="{}">{}</a>', url, obj.scale)
    scale_link.short_description = 'Scale'
    
    def period_label(self, obj):
        return obj.period_label
    period_label.short_description = 'Period'


@admin.register(RevenueProjection)
class RevenueProjectionAdmin(admin.ModelAdmin):
    list_display = ['scale_link', 'period_label', 'unit_sales', 'total_revenue', 'net_profit', 'cumulative_cash_flow']
    list_filter = ['period_type', 'scale__scale_type', 'scale__year']
    readonly_fields = ['total_revenue', 'gross_profit', 'net_profit']
    
    def scale_link(self, obj):
        url = reverse('admin:businesses_businessscale_change', args=[obj.scale.id])
        return format_html('<a href="{}">{}</a>', url, obj.scale)
    scale_link.short_description = 'Scale'
    
    def period_label(self, obj):
        return obj.period_label
    period_label.short_description = 'Period'


@admin.register(FinancialMetric)
class FinancialMetricAdmin(admin.ModelAdmin):
    list_display = ['scale_link', 'gross_margin_pct', 'net_margin_pct', 'roi_pct', 'payback_months', 'is_primary']
    list_filter = ['is_primary', 'scale__scale_type', 'scale__year']
    search_fields = ['scale__business__name']
    
    def scale_link(self, obj):
        url = reverse('admin:businesses_businessscale_change', args=[obj.scale.id])
        return format_html('<a href="{}">{}</a>', url, obj.scale)
    scale_link.short_description = 'Scale'


@admin.register(Risk)
class RiskAdmin(admin.ModelAdmin):
    list_display = ['specific_risk', 'scale_link', 'category', 'likelihood', 'impact', 'risk_score']
    list_filter = ['category', 'scale__scale_type', 'scale__year']  # REMOVED severity_label
    search_fields = ['specific_risk', 'mitigation_strategy']
    readonly_fields = ['risk_score']
    
    def scale_link(self, obj):
        url = reverse('admin:businesses_businessscale_change', args=[obj.scale.id])
        return format_html('<a href="{}">{}</a>', url, obj.scale)
    scale_link.short_description = 'Scale'


@admin.register(FeasibilityFactor)
class FeasibilityFactorAdmin(admin.ModelAdmin):
    list_display = ['sub_category', 'scale_link', 'category', 'rating', 'source']
    list_filter = ['category', 'scale__scale_type', 'scale__year', 'rating']
    search_fields = ['sub_category', 'notes']
    
    def scale_link(self, obj):
        url = reverse('admin:businesses_businessscale_change', args=[obj.scale.id])
        return format_html('<a href="{}">{}</a>', url, obj.scale)
    scale_link.short_description = 'Scale'


@admin.register(OperationsChecklist)
class OperationsChecklistAdmin(admin.ModelAdmin):
    list_display = ['task_name', 'business_link', 'scale_type', 'task_type', 'duration_minutes']
    list_filter = ['task_type', 'scale_type', 'business__sector']
    search_fields = ['task_name', 'description']
    
    def business_link(self, obj):
        url = reverse('admin:businesses_business_change', args=[obj.business.id])
        return format_html('<a href="{}">{}</a>', url, obj.business.name)
    business_link.short_description = 'Business'


@admin.register(BusinessProfile)
class BusinessProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner_name', 'sector', 'business_type', 'is_verified', 'is_partner', 'status']
    list_filter = ['is_verified', 'is_partner', 'is_featured', 'status', 'sector', 'location']
    search_fields = ['name', 'owner_name', 'email', 'phone']
    prepopulated_fields = {'slug': ['name']}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'owner_name', 'owner_position', 'description', 'short_description')
        }),
        ('Media', {
            'fields': ('logo', 'cover_image'),
            'classes': ('collapse',)
        }),
        ('Contact', {
            'fields': ('email', 'phone', 'website', 'address', 'location'),
            'classes': ('collapse',)
        }),
        ('Social Media', {
            'fields': ('facebook', 'instagram', 'linkedin', 'twitter', 'tiktok', 'whatsapp'),
            'classes': ('collapse',)
        }),
        ('Business Details', {
            'fields': ('founded_year', 'employee_count', 'business_type_legal', 'sector', 'business_type', 'user')
        }),
        ('Classification', {
            'fields': ('is_partner', 'is_featured', 'is_verified', 'partner_type')
        }),
        ('Interview Metadata', {
            'fields': ('interview_date', 'interviewed_by', 'interview_notes'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('status', 'view_count')
        }),
    )


class BusinessProfileFeatureInline(admin.TabularInline):
    model = BusinessProfileFeature
    extra = 1
    fields = ['title', 'description', 'icon', 'order']


class BusinessProfileTestimonialInline(admin.TabularInline):
    model = BusinessProfileTestimonial
    extra = 1
    fields = ['quote', 'author_name', 'author_position', 'is_featured', 'order']


@admin.register(IntelligenceSnapshot)
class IntelligenceSnapshotAdmin(admin.ModelAdmin):
    list_display = ['business_name', 'year', 'scale_type', 'version', 'is_latest', 'status', 'startup_cost']
    list_filter = ['status', 'is_latest', 'year', 'scale_type']
    search_fields = ['business_name', 'business_slug']
    readonly_fields = ['business_name', 'business_slug', 'sector_id', 'startup_cost', 
                       'gross_margin_pct', 'payback_months', 'feasibility_score', 'risk_score']
    
    fieldsets = (
        ('Identity', {
            'fields': ('business', 'scale_type', 'year', 'version', 'is_latest')
        }),
        ('Status', {
            'fields': ('status', 'published_at', 'primary_source')
        }),
        ('Denormalized Data (Read Only)', {
            'fields': ('business_name', 'business_slug', 'sector_id', 'startup_cost',
                      'gross_margin_pct', 'payback_months', 'feasibility_score', 'risk_score'),
            'classes': ('collapse',)
        }),
        ('Full Data (JSON)', {
            'fields': ('data',),
            'classes': ('collapse',)
        }),
        ('AI', {
            'fields': ('summary_text', 'embedding'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TimeSeriesMetric)
class TimeSeriesMetricAdmin(admin.ModelAdmin):
    list_display = ['business', 'metric_name', 'year', 'scale_type', 'value_numeric']
    list_filter = ['metric_name', 'year', 'scale_type']
    search_fields = ['business__name']
    readonly_fields = ['created_at', 'updated_at']