from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Report, ReportPurchase, ReportBundle, ReportReview


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'report_type', 'format', 'price_display', 
        'is_featured', 'is_bestseller', 'status_badge', 
        'download_count', 'rating_display'
    ]
    list_filter = [
        'report_type', 'format', 'status', 'is_featured', 
        'is_bestseller', 'sector', 'created_at'
    ]
    search_fields = ['title', 'subtitle', 'description', 'author']
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'subtitle', 'slug', 'description', 'short_description')
        }),
        ('File & Media', {
            'fields': ('cover_image', 'file', 'file_size')
        }),
        ('Report Details', {
            'fields': ('report_type', 'format', 'sector', 'business')
        }),
        ('Content', {
            'fields': ('table_of_contents', 'key_highlights'),
            'classes': ('collapse',)
        }),
        ('Pricing', {
            'fields': ('price', 'is_free')
        }),
        ('Metadata', {
            'fields': ('page_count', 'version', 'author')
        }),
        ('Status', {
            'fields': ('status', 'is_featured', 'is_bestseller', 'published_at')
        }),
        ('Stats', {
            'fields': ('download_count', 'view_count', 'rating', 'review_count'),
            'classes': ('collapse',)
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['file_size', 'download_count', 'view_count', 'rating', 'review_count']
    
    def price_display(self, obj):
        return obj.price_display
    price_display.short_description = 'Price'
    
    def rating_display(self, obj):
        if obj.rating == 0:
            return "No reviews"
        stars = '★' * int(obj.rating) + '☆' * (5 - int(obj.rating))
        return format_html('<span title="{} stars">{}</span>', obj.rating, stars)
    rating_display.short_description = 'Rating'
    
    def status_badge(self, obj):
        colors = {'draft': 'gray', 'published': 'green', 'archived': 'red'}
        color = colors.get(obj.status, 'gray')
        bg = 'gray' if color == 'gray' else ('#10b981' if color == 'green' else '#ef4444')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">{}</span>',
            bg, obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    actions = ['publish_reports', 'make_featured', 'make_bestseller']
    
    def publish_reports(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='published', published_at=timezone.now())
    publish_reports.short_description = 'Publish selected reports'
    
    def make_featured(self, request, queryset):
        queryset.update(is_featured=True)
    make_featured.short_description = 'Mark as featured'
    
    def make_bestseller(self, request, queryset):
        queryset.update(is_bestseller=True)
    make_bestseller.short_description = 'Mark as bestseller'


@admin.register(ReportPurchase)
class ReportPurchaseAdmin(admin.ModelAdmin):
    list_display = [
        'user_link', 'report_link', 'amount_paid', 'is_paid', 
        'has_downloaded', 'download_count', 'paid_at'
    ]
    list_filter = ['is_paid', 'has_downloaded', 'paid_at']
    search_fields = ['user__email', 'report__title', 'transaction_reference']
    readonly_fields = ['paid_at']
    
    def user_link(self, obj):
        url = reverse('admin:users_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.email)
    user_link.short_description = 'User'
    
    def report_link(self, obj):
        url = reverse('admin:reports_report_change', args=[obj.report.id])
        return format_html('<a href="{}">{}</a>', url, obj.report.title)
    report_link.short_description = 'Report'


@admin.register(ReportBundle)
class ReportBundleAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'price_display', 'original_price_display', 
        'discount_percent', 'purchase_count', 'is_featured', 'status'
    ]
    list_filter = ['status', 'is_featured', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    
    filter_horizontal = ['reports']
    
    def price_display(self, obj):
        return obj.price_display
    price_display.short_description = 'Price'
    
    def original_price_display(self, obj):
        return obj.original_price_display
    original_price_display.short_description = 'Original Price'


@admin.register(ReportReview)
class ReportReviewAdmin(admin.ModelAdmin):
    list_display = ['report', 'user', 'rating', 'title', 'is_verified_purchase', 'is_approved']
    list_filter = ['rating', 'is_approved', 'is_verified_purchase', 'created_at']
    search_fields = ['user__email', 'report__title', 'title', 'content']
    
    actions = ['approve_reviews']
    
    def approve_reviews(self, request, queryset):
        for review in queryset:
            review.approve()
    approve_reviews.short_description = 'Approve selected reviews'