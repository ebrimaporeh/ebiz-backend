from django.contrib import admin
from django.utils.html import format_html
from .models import Article, Video, CaseStudy, Tag, Comment


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'author', 'sector', 'is_premium', 'is_featured',
        'status_badge', 'view_count', 'published_at'
    ]
    list_filter = ['status', 'is_premium', 'is_featured', 'sector', 'created_at']
    search_fields = ['title', 'excerpt', 'content', 'author']
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'excerpt', 'content', 'premium_content')
        }),
        ('Media', {
            'fields': ('featured_image',),
            'classes': ('collapse',)
        }),
        ('Relationships', {
            'fields': ('sector', 'business')
        }),
        ('Metadata', {
            'fields': ('author', 'read_time')
        }),
        ('Status', {
            'fields': ('status', 'is_premium', 'is_featured', 'published_at')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Stats', {
            'fields': ('view_count', 'like_count'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['view_count', 'like_count']
    
    def status_badge(self, obj):
        colors = {'draft': 'gray', 'published': 'green', 'archived': 'red'}
        color = colors.get(obj.status, 'gray')
        bg = 'gray' if color == 'gray' else ('#10b981' if color == 'green' else '#ef4444')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">{}</span>',
            bg, obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    actions = ['publish_articles', 'make_premium', 'make_free']
    
    def publish_articles(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='published', published_at=timezone.now())
    publish_articles.short_description = 'Publish selected articles'
    
    def make_premium(self, request, queryset):
        queryset.update(is_premium=True)
    make_premium.short_description = 'Mark as premium'
    
    def make_free(self, request, queryset):
        queryset.update(is_premium=False)
    make_free.short_description = 'Mark as free'


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'platform', 'sector', 'is_premium', 'is_featured',
        'status_badge', 'view_count', 'published_at'
    ]
    list_filter = ['status', 'platform', 'is_premium', 'is_featured', 'sector']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description')
        }),
        ('Video Source', {
            'fields': ('platform', 'platform_video_id', 'video_url', 'thumbnail_url', 'duration')
        }),
        ('Relationships', {
            'fields': ('sector', 'business')
        }),
        ('Status', {
            'fields': ('status', 'is_premium', 'is_featured', 'published_at')
        }),
        ('Stats', {
            'fields': ('view_count', 'like_count', 'comment_count'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['video_url']
    
    def status_badge(self, obj):
        colors = {'draft': 'gray', 'published': 'green', 'archived': 'red'}
        color = colors.get(obj.status, 'gray')
        bg = 'gray' if color == 'gray' else ('#10b981' if color == 'green' else '#ef4444')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">{}</span>',
            bg, obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    actions = ['publish_videos']
    
    def publish_videos(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='published', published_at=timezone.now())
    publish_videos.short_description = 'Publish selected videos'


@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'business_name', 'sector', 'is_success',
        'is_featured', 'status_badge', 'view_count'
    ]
    list_filter = ['status', 'is_success', 'is_featured', 'sector']
    search_fields = ['title', 'business_name', 'content']
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'excerpt', 'content')
        }),
        ('Business Details', {
            'fields': ('business_name', 'business_type', 'sector')
        }),
        ('Financial Metrics', {
            'fields': ('initial_investment', 'revenue_generated', 'roi_percent', 'timeline_months')
        }),
        ('Outcome', {
            'fields': ('is_success', 'key_lessons')
        }),
        ('Media', {
            'fields': ('featured_image',),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('status', 'is_featured', 'published_at')
        }),
        ('Stats', {
            'fields': ('view_count',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['view_count']
    
    def status_badge(self, obj):
        colors = {'draft': 'gray', 'published': 'green', 'archived': 'red'}
        color = colors.get(obj.status, 'gray')
        bg = 'gray' if color == 'gray' else ('#10b981' if color == 'green' else '#ef4444')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">{}</span>',
            bg, obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    actions = ['publish_case_studies']
    
    def publish_case_studies(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='published', published_at=timezone.now())
    publish_case_studies.short_description = 'Publish selected case studies'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'usage_count']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['usage_count']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'article', 'is_approved', 'like_count', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['user_name', 'user_email', 'content']
    
    actions = ['approve_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = 'Approve selected comments'