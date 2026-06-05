"""
apps/core/admin.py

Admin configuration for core models.
"""

from django.contrib import admin
from .models import Source, RatingValue, APIKey, Country, Region


# ============================================
# SOURCE ADMIN
# ============================================

@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'year', 'source_type', 'confidence_rating', 'is_primary_source']
    list_filter = ['source_type', 'year', 'is_primary_source']
    search_fields = ['name', 'reference', 'notes']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'reference', 'url', 'publication_date', 'year')
        }),
        ('Classification', {
            'fields': ('source_type', 'confidence_rating', 'is_primary_source')
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


# ============================================
# RATING VALUE ADMIN
# ============================================

@admin.register(RatingValue)
class RatingValueAdmin(admin.ModelAdmin):
    list_display = ['value', 'year', 'source', 'confidence_score']
    list_filter = ['year', 'source__source_type']
    search_fields = ['notes']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Rating', {
            'fields': ('value', 'year', 'source', 'confidence_score')
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# ============================================
# API KEY ADMIN
# ============================================

@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ['organization', 'tier', 'is_active', 'last_used', 'expires_at']
    list_filter = ['tier', 'is_active']
    search_fields = ['organization', 'contact_email', 'key']
    readonly_fields = ['key', 'created_at', 'last_used']
    
    fieldsets = (
        ('Organization', {
            'fields': ('organization', 'contact_name', 'contact_email')
        }),
        ('Access', {
            'fields': ('key', 'tier', 'rate_limit_per_minute')
        }),
        ('Status', {
            'fields': ('is_active', 'expires_at', 'last_used')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing existing
            return ['key', 'created_at', 'last_used', 'organization']
        return ['key', 'created_at', 'last_used']
    
    actions = ['revoke_keys', 'activate_keys']
    
    def revoke_keys(self, request, queryset):
        """Revoke selected API keys"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} API key(s) revoked.')
    revoke_keys.short_description = "Revoke selected API keys"
    
    def activate_keys(self, request, queryset):
        """Activate selected API keys"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} API key(s) activated.')
    activate_keys.short_description = "Activate selected API keys"


# ============================================
# COUNTRY ADMIN
# ============================================

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['flag_display', 'code', 'name', 'currency_symbol', 'is_active', 'order']
    list_filter = ['is_active', 'currency']
    search_fields = ['name', 'code']
    list_editable = ['order', 'is_active']
    ordering = ['order', 'name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('code', 'name', 'flag_emoji', 'is_active', 'order')
        }),
        ('Currency', {
            'fields': ('currency', 'currency_symbol')
        }),
        ('Market Data', {
            'fields': ('population', 'gdp_per_capita_usd'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def flag_display(self, obj):
        """Display flag emoji in list"""
        return obj.flag_emoji or "🏳️"
    flag_display.short_description = "Flag"
    flag_display.admin_order_field = 'name'


# ============================================
# REGION ADMIN
# ============================================

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'country_count']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ['name']}
    readonly_fields = ['created_at', 'updated_at', 'country_count']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Countries', {
            'fields': ('countries',),
            'description': 'Select countries that belong to this region'
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'country_count'),
            'classes': ('collapse',)
        }),
    )
    
    filter_horizontal = ['countries']
    
    def country_count(self, obj):
        """Display number of countries in region"""
        return obj.countries.count()
    country_count.short_description = "Countries"