from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.urls import reverse

from .models import User, UserProfile, Subscription, OneTimePurchase


class UserProfileInline(admin.StackedInline):
    """Inline admin for UserProfile."""
    
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fieldsets = (
        ('Profile Picture', {
            'fields': ('avatar',)
        }),
        ('Social Links', {
            'fields': ('linkedin_url', 'twitter_handle', 'website_url'),
            'classes': ('collapse',)
        }),
    )


class SubscriptionInline(admin.TabularInline):
    """Inline admin for Subscriptions."""
    
    model = Subscription
    fields = ('plan_type', 'amount', 'started_at', 'expires_at', 'is_active', 'is_paid')
    readonly_fields = ('started_at', 'expires_at', 'created_at')
    extra = 0
    can_delete = False
    show_change_link = True
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-created_at')[:5]


class OneTimePurchaseInline(admin.TabularInline):
    """Inline admin for One-Time Purchases."""
    
    model = OneTimePurchase
    fields = ('report_title', 'amount', 'purchased_at', 'has_downloaded', 'download_count')
    readonly_fields = ('purchased_at',)
    extra = 0
    can_delete = False
    show_change_link = True
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-purchased_at')[:5]


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom admin for User model."""
    
    inlines = [UserProfileInline, SubscriptionInline, OneTimePurchaseInline]
    
    list_display = (
        'email', 
        'full_name', 
        'tier_badge', 
        'has_premium_badge',
        'user_type_badges',
        'is_active', 
        'is_staff',
        'date_joined'
    )
    
    list_filter = (
        'tier', 
        'is_active', 
        'is_staff', 
        'is_entrepreneur', 
        'is_investor', 
        'is_student',
        'newsletter_subscribed',
    )
    
    search_fields = ('email', 'first_name', 'last_name', 'phone')
    ordering = ('-date_joined',)
    
    readonly_fields = ('date_joined', 'last_login', 'last_login_ip', 'created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'phone', 'location', 'bio')
        }),
        ('Access Level (Tier)', {
            'fields': ('tier', 'tier_expires_at'),
            'classes': ('wide',),
            'description': 'Regular = free access only. Premium = subscription access. One-time = purchased specific reports.'
        }),
        ('User Type', {
            'fields': ('is_entrepreneur', 'is_investor', 'is_student'),
            'classes': ('collapse',)
        }),
        ('Preferences', {
            'fields': ('newsletter_subscribed', 'email_notifications'),
            'classes': ('collapse',)
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Important Dates', {
            'fields': ('date_joined', 'last_login', 'last_login_ip', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    
    def full_name(self, obj):
        """Display full name."""
        return obj.full_name
    full_name.short_description = 'Full Name'
    full_name.admin_order_field = 'first_name'
    
    def tier_badge(self, obj):
        """Display tier as a colored badge."""
        colors = {
            'regular': 'gray',
            'premium': 'gold',
            'one_time': 'green',
        }
        color = colors.get(obj.tier, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">{}</span>',
            'gray' if color == 'gray' else ('#f59e0b' if color == 'gold' else '#10b981'),
            obj.get_tier_display()
        )
    tier_badge.short_description = 'Tier'
    
    def has_premium_badge(self, obj):
        """Show if user has premium access."""
        if obj.has_premium_access:
            return format_html(
                '<span style="background-color: #10b981; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">✓ Has Access</span>'
            )
        return format_html(
            '<span style="background-color: #6b7280; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">No Access</span>'
        )
    has_premium_badge.short_description = 'Premium Access'
    
    def user_type_badges(self, obj):
        """Display user type as badges."""
        badges = []
        if obj.is_entrepreneur:
            badges.append('<span style="background-color: #3b82f6; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px; margin-right: 4px;">Entrepreneur</span>')
        if obj.is_investor:
            badges.append('<span style="background-color: #8b5cf6; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px; margin-right: 4px;">Investor</span>')
        if obj.is_student:
            badges.append('<span style="background-color: #ef4444; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">Student</span>')
        
        if not badges:
            return '—'
        return format_html(''.join(badges))
    user_type_badges.short_description = 'User Type'
    
    actions = ['upgrade_to_premium_30_days', 'downgrade_to_regular']
    
    def upgrade_to_premium_30_days(self, request, queryset):
        """Bulk upgrade users to Premium for 30 days."""
        count = 0
        for user in queryset:
            user.upgrade_to_premium(duration_days=30)
            count += 1
        self.message_user(request, f'{count} users upgraded to Premium (30 days).')
    upgrade_to_premium_30_days.short_description = 'Upgrade selected to Premium (30 days)'
    
    def downgrade_to_regular(self, request, queryset):
        """Bulk downgrade users to Regular."""
        count = 0
        for user in queryset:
            user.downgrade_to_regular()
            count += 1
        self.message_user(request, f'{count} users downgraded to Regular.')
    downgrade_to_regular.short_description = 'Downgrade selected to Regular'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin for UserProfile."""
    
    list_display = ('user', 'get_user_email', 'get_user_tier', 'linkedin_url', 'created_at')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    list_filter = ('user__tier',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Profile Picture', {
            'fields': ('avatar',)
        }),
        ('Social Links', {
            'fields': ('linkedin_url', 'twitter_handle', 'website_url')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_user_email(self, obj):
        """Display user email."""
        return obj.user.email
    get_user_email.short_description = 'Email'
    get_user_email.admin_order_field = 'user__email'
    
    def get_user_tier(self, obj):
        """Display user tier."""
        return obj.user.get_tier_display()
    get_user_tier.short_description = 'Tier'
    get_user_tier.admin_order_field = 'user__tier'


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Admin for Subscription."""
    
    list_display = (
        'user_email', 
        'plan_type_badge', 
        'amount_display', 
        'started_at', 
        'expires_at', 
        'is_active_badge',
        'is_paid_badge',
        'days_remaining'
    )
    
    list_filter = ('plan_type', 'is_active', 'is_paid', 'started_at')
    search_fields = ('user__email', 'transaction_reference')
    readonly_fields = ('created_at', 'updated_at', 'days_remaining')
    
    fieldsets = (
        ('User & Plan', {
            'fields': ('user', 'plan_type', 'amount')
        }),
        ('Duration', {
            'fields': ('duration_days', 'started_at', 'expires_at', 'days_remaining')
        }),
        ('Payment', {
            'fields': ('payment_method', 'transaction_reference', 'is_paid', 'paid_at')
        }),
        ('Status', {
            'fields': ('is_active', 'cancelled_at')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def user_email(self, obj):
        """Display user email with link to user admin."""
        url = reverse('admin:users_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.email)
    user_email.short_description = 'User'
    user_email.admin_order_field = 'user__email'
    
    def amount_display(self, obj):
        """Display amount in Dalasi."""
        return f"D{obj.amount:,}"
    amount_display.short_description = 'Amount'
    
    def plan_type_badge(self, obj):
        """Display plan type as badge."""
        colors = {
            'regular': 'gray',
            'premium': 'gold',
            'one_time': 'green',
        }
        color = colors.get(obj.plan_type, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">{}</span>',
            'gray' if color == 'gray' else ('#f59e0b' if color == 'gold' else '#10b981'),
            obj.get_plan_type_display()
        )
    plan_type_badge.short_description = 'Plan'
    
    def is_active_badge(self, obj):
        """Display active status as badge."""
        if obj.is_active and not obj.is_expired:
            return format_html('<span style="background-color: #10b981; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">Active</span>')
        elif obj.is_expired:
            return format_html('<span style="background-color: #ef4444; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">Expired</span>')
        return format_html('<span style="background-color: #6b7280; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">Inactive</span>')
    is_active_badge.short_description = 'Status'
    
    def is_paid_badge(self, obj):
        """Display paid status as badge."""
        if obj.is_paid:
            return format_html('<span style="background-color: #10b981; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">Paid</span>')
        return format_html('<span style="background-color: #ef4444; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">Unpaid</span>')
    is_paid_badge.short_description = 'Payment'
    
    def days_remaining(self, obj):
        """Display days remaining until expiry."""
        if not obj.is_active or obj.is_expired:
            return '—'
        return f"{obj.days_remaining} days"
    days_remaining.short_description = 'Days Left'


@admin.register(OneTimePurchase)
class OneTimePurchaseAdmin(admin.ModelAdmin):
    """Admin for OneTimePurchase."""
    
    list_display = (
        'user_email', 
        'report_title', 
        'amount_display', 
        'purchased_at', 
        'has_downloaded_badge',
        'download_count'
    )
    
    list_filter = ('is_paid', 'has_downloaded', 'purchased_at')
    search_fields = ('user__email', 'report_title', 'transaction_reference')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User & Report', {
            'fields': ('user', 'report_id', 'report_title')
        }),
        ('Payment', {
            'fields': ('amount', 'payment_method', 'transaction_reference', 'is_paid', 'purchased_at')
        }),
        ('Download Information', {
            'fields': ('has_downloaded', 'download_count', 'last_downloaded_at')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def user_email(self, obj):
        """Display user email with link to user admin."""
        url = reverse('admin:users_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.email)
    user_email.short_description = 'User'
    user_email.admin_order_field = 'user__email'
    
    def amount_display(self, obj):
        """Display amount in Dalasi."""
        return f"D{obj.amount:,}"
    amount_display.short_description = 'Amount'
    
    def has_downloaded_badge(self, obj):
        """Display download status as badge."""
        if obj.has_downloaded:
            return format_html('<span style="background-color: #10b981; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">Downloaded</span>')
        return format_html('<span style="background-color: #6b7280; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">Not Downloaded</span>')
    has_downloaded_badge.short_description = 'Status'