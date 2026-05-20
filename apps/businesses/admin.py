# apps/businesses/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import *


# ============================================
# INLINE CLASSES (Define BEFORE using them)
# ============================================

class BusinessScaleInline(admin.TabularInline):
    model = BusinessScale
    extra = 0
    fields = ['scale_type', 'capacity_definition', 'target_market', 'overall_feasibility_score']
    show_change_link = True


class CapitalItemInline(admin.TabularInline):
    model = CapitalItem
    extra = 0
    fields = ['category', 'item_name', 'quantity', 'unit_cost', 'total_cost', 'priority']
    readonly_fields = ['total_cost']


class OperatingCostInline(admin.TabularInline):
    model = OperatingCost
    extra = 0
    fields = ['week_range', 'total']
    readonly_fields = ['total']


class RiskInline(admin.TabularInline):
    model = Risk
    extra = 0
    fields = ['category', 'specific_risk', 'likelihood', 'impact', 'risk_score']
    readonly_fields = ['risk_score']


class OperationsChecklistInline(admin.TabularInline):
    """Operations checklist inline for Business admin"""
    model = OperationsChecklist
    extra = 0
    fields = ['scale_type', 'task_type', 'task_name', 'order']


# ============================================
# BUSINESS ADMIN
# ============================================

@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'sector', 'status_badge', 'is_featured', 
        'view_count', 'created_at'
    ]
    list_filter = ['sector', 'status', 'is_featured']
    search_fields = ['name', 'overview']
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('sector', 'name', 'slug', 'short_description')
        }),
        ('Content', {
            'fields': ('overview', 'opportunity_thesis')
        }),
        ('Media', {
            'fields': ('featured_image',),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('status', 'is_featured')
        }),
        ('Metadata', {
            'fields': ('view_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['view_count', 'created_at', 'updated_at']
    
    # Now OperationsChecklistInline is defined before being used
    inlines = [BusinessScaleInline, OperationsChecklistInline]
    
    actions = ['publish_businesses', 'feature_businesses']
    
    def status_badge(self, obj):
        colors = {'draft': 'gray', 'published': 'green', 'archived': 'red'}
        color = colors.get(obj.status, 'gray')
        bg = 'gray' if color == 'gray' else ('#10b981' if color == 'green' else '#ef4444')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">{}</span>',
            bg, obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def publish_businesses(self, request, queryset):
        queryset.update(status='published')
    publish_businesses.short_description = 'Publish selected businesses'
    
    def feature_businesses(self, request, queryset):
        queryset.update(is_featured=True)
    feature_businesses.short_description = 'Feature selected businesses'


# ============================================
# BUSINESS SCALE ADMIN
# ============================================

@admin.register(BusinessScale)
class BusinessScaleAdmin(admin.ModelAdmin):
    list_display = ['business', 'scale_type', 'capacity_definition', 'overall_feasibility_score']
    list_filter = ['scale_type', 'business__sector']
    search_fields = ['business__name']
    
    fieldsets = (
        ('Business', {
            'fields': ('business', 'scale_type')
        }),
        ('Definition', {
            'fields': ('capacity_definition', 'target_market', 'location_type', 'labor_needed')
        }),
        ('Feasibility', {
            'fields': ('overall_feasibility_score',)
        }),
    )
    
    inlines = [CapitalItemInline, OperatingCostInline, RiskInline]
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('business')


# ============================================
# OTHER MODEL ADMINS
# ============================================

@admin.register(CapitalItem)
class CapitalItemAdmin(admin.ModelAdmin):
    list_display = ['item_name', 'scale', 'category', 'quantity', 'unit_cost', 'total_cost', 'priority']
    list_filter = ['category', 'priority', 'scale__scale_type']
    search_fields = ['item_name']


@admin.register(OperatingCost)
class OperatingCostAdmin(admin.ModelAdmin):
    list_display = ['scale', 'week_range', 'total']
    list_filter = ['scale__scale_type']
    readonly_fields = ['total']


@admin.register(Risk)
class RiskAdmin(admin.ModelAdmin):
    list_display = ['specific_risk', 'scale', 'category', 'likelihood', 'impact', 'risk_score']
    list_filter = ['category', 'scale__scale_type']
    readonly_fields = ['risk_score']


@admin.register(FeasibilityFactor)
class FeasibilityFactorAdmin(admin.ModelAdmin):
    list_display = ['sub_category', 'scale', 'category', 'rating', 'data_source']
    list_filter = ['category', 'scale__scale_type']
    search_fields = ['sub_category']


@admin.register(OperationsChecklist)
class OperationsChecklistAdmin(admin.ModelAdmin):
    list_display = ['task_name', 'business', 'scale_type', 'task_type', 'order']
    list_filter = ['scale_type', 'task_type']
    search_fields = ['task_name', 'business__name']


# Add to existing admin.py

class BusinessProfileFeatureInline(admin.TabularInline):
    model = BusinessProfileFeature
    extra = 0
    fields = ['title', 'description', 'icon', 'order']


class BusinessProfileTestimonialInline(admin.TabularInline):
    model = BusinessProfileTestimonial
    extra = 0
    fields = ['quote', 'author_name', 'author_position', 'is_featured', 'order']


@admin.register(BusinessProfile)
class BusinessProfileAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'owner_name', 'sector', 'location', 
        'is_partner', 'is_verified', 'is_featured', 'status_badge'
    ]
    list_filter = ['is_partner', 'is_verified', 'is_featured', 'status', 'sector', 'location']
    search_fields = ['name', 'owner_name', 'email', 'phone', 'description']
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'owner_name', 'owner_position', 'description', 'short_description')
        }),
        ('Media', {
            'fields': ('logo', 'cover_image')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'website', 'address', 'location')
        }),
        ('Social Media', {
            'fields': ('facebook', 'instagram', 'linkedin', 'twitter', 'tiktok', 'whatsapp'),
            'classes': ('collapse',)
        }),
        ('Business Details', {
            'fields': ('founded_year', 'employee_count', 'business_type', 'sector')
        }),
        ('Partnership', {
            'fields': ('is_partner', 'is_verified', 'is_featured', 'partner_type'),
            'classes': ('collapse',)
        }),
        ('Interview Details', {
            'fields': ('interview_date', 'interviewed_by', 'interview_notes'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Stats', {
            'fields': ('view_count',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['view_count']
    inlines = [BusinessProfileFeatureInline, BusinessProfileTestimonialInline]
    
    def status_badge(self, obj):
        colors = {'draft': 'gray', 'published': 'green', 'archived': 'red'}
        color = colors.get(obj.status, 'gray')
        bg = 'gray' if color == 'gray' else ('#10b981' if color == 'green' else '#ef4444')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">{}</span>',
            bg, obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    actions = ['verify_businesses', 'make_partners', 'publish_profiles']
    
    def verify_businesses(self, request, queryset):
        queryset.update(is_verified=True)
    verify_businesses.short_description = 'Mark as verified'
    
    def make_partners(self, request, queryset):
        queryset.update(is_partner=True)
    make_partners.short_description = 'Mark as partners'
    
    def publish_profiles(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='published')
    publish_profiles.short_description = 'Publish selected profiles'