from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Sector
from apps.core.constants import Status


@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
        'business_count_display',
        'order',
        'status_badge',
        'created_at',
    ]
    
    list_filter = ['status', 'created_at', 'updated_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'status')
        }),
        ('Visuals', {
            'fields': ('icon', 'color', 'featured_image'),
            'classes': ('collapse',)
        }),
        ('Display Settings', {
            'fields': ('order',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('business_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'business_count']
    
    actions = ['publish_sectors', 'unpublish_sectors']
    
    def status_badge(self, obj):
        colors = {
            'draft': 'gray',
            'published': 'green',
            'archived': 'red',
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">{}</span>',
            'gray' if color == 'gray' else ('#10b981' if color == 'green' else '#ef4444'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def business_count_display(self, obj):
        url = reverse('admin:businesses_business_changelist') + f'?sector__id__exact={obj.id}'
        return format_html('<a href="{}">{} businesses</a>', url, obj.business_count)
    business_count_display.short_description = 'Businesses'
    
    def publish_sectors(self, request, queryset):
        queryset.update(status=Status.PUBLISHED)
    publish_sectors.short_description = 'Publish selected sectors'
    
    def unpublish_sectors(self, request, queryset):
        queryset.update(status=Status.DRAFT)
    unpublish_sectors.short_description = 'Unpublish selected sectors'