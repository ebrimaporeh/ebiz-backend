# apps/sectors/admin.py

from django.contrib import admin
from .models import Sector, SectorTag, SectorStat


@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ['name', 'country_display', 'region', 'business_count', 'status', 'order']
    list_filter = ['status', 'country', 'region']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'parent')
        }),
        ('Geographic Scope', {
            'fields': ('country', 'region', 'currency')
        }),
        ('Visual', {
            'fields': ('icon', 'color', 'featured_image'),
            'classes': ('collapse',)
        }),
        ('Market Data', {
            'fields': ('business_count', 'estimated_market_size', 'estimated_market_size_display'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('status', 'order', 'summary_for_ai')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_prepopulated_fields(self, _request, obj=None):
        return {} if obj else self.prepopulated_fields

    def country_display(self, obj):
        """Display country name"""
        from apps.core.constants import Country as CountryChoice
        return dict(CountryChoice.choices).get(obj.country, obj.country)
    country_display.short_description = "Country"


@admin.register(SectorTag)
class SectorTagAdmin(admin.ModelAdmin):
    list_display = ['label', 'slug']
    search_fields = ['label', 'description']
    prepopulated_fields = {'slug': ['label']}


@admin.register(SectorStat)
class SectorStatAdmin(admin.ModelAdmin):
    list_display = ['label', 'sector', 'value', 'unit', 'year']
    list_filter = ['sector', 'year', 'unit', 'country', 'region']
    search_fields = ['label']