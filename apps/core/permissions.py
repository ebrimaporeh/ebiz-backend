"""
apps/core/permissions.py

Custom permission classes for GAMBIH API.
Handles subscription tiers, report access, and premium content.
"""

from rest_framework import permissions


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """Read-only for guests, write for authenticated users."""
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated


class IsAdminOrReadOnly(permissions.BasePermission):
    """Admin only for write operations."""
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsAdminOrAuthenticatedReadOnly(permissions.BasePermission):
    """
    Authenticated users can read, admin users can write.
    Unauthenticated users cannot access at all.
    """
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff


class IsPremiumUser(permissions.BasePermission):
    """
    Premium content access for subscribers or one-time purchasers.
    Checks user's subscription tier or report purchase history.
    """
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            if not request.user.is_authenticated:
                return False
            return request.user.has_premium_access()
        return request.user.is_authenticated


class IsProOrReadOnly(permissions.BasePermission):
    """
    Pro tier or higher for write operations.
    Read-only for authenticated users below Pro tier.
    
    - Read: All authenticated users
    - Write: Pro or Enterprise users only
    """
    
    def has_permission(self, request, view):
        # Read-only for all authenticated users
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Write operations require Pro or Enterprise
        return request.user and request.user.is_authenticated and request.user.tier in ['pro', 'enterprise']


class IsProUser(permissions.BasePermission):
    """
    Pro tier access (includes Premium features plus Pro-only content).
    Write and read both require Pro or higher.
    """
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.tier in ['pro', 'enterprise']


class IsEnterpriseUser(permissions.BasePermission):
    """
    Enterprise tier access - highest level.
    """
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            if not request.user.is_authenticated:
                return False
            return request.user.tier == 'enterprise'
        return request.user.is_authenticated


class IsPremiumOrReadOnly(permissions.BasePermission):
    """
    Premium tier or higher for write operations.
    Read-only for all authenticated users.
    """
    
    def has_permission(self, request, view):
        # Read-only for all authenticated users
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Write operations require Premium, Pro, or Enterprise
        return request.user and request.user.is_authenticated and request.user.has_premium_access()


class HasReportAccess(permissions.BasePermission):
    """
    Check if user has access to a specific report.
    - Free reports: accessible to all authenticated users
    - Premium/Pro reports: check subscription tier
    - One-time purchase: check if user purchased the report
    """
    
    def has_object_permission(self, request, view, obj):
        """Check permission for a specific report object."""
        from apps.reports.models import Report, ReportPurchase
        
        if not request.user.is_authenticated:
            return False
        
        # Free reports are accessible to all authenticated users
        if not getattr(obj, 'is_gated', True):
            return True
        
        # Check subscription tier
        if request.user.tier == 'enterprise':
            return True
        
        if request.user.tier == 'pro' and obj.tier_required in ['pro', 'premium']:
            return True
        
        if request.user.tier == 'premium' and obj.tier_required == 'premium':
            return True
        
        # Check for one-time purchase
        if hasattr(obj, 'purchases'):
            has_purchased = obj.purchases.filter(
                user=request.user,
                status='completed'
            ).exists()
            if has_purchased:
                return True
        
        return False


class CanAccessBusinessData(permissions.BasePermission):
    """
    Control access to business intelligence data based on scale.
    
    Tier mapping:
    - Free: small scale only
    - Premium: small + medium scale
    - Pro: small + medium + large scale
    - Enterprise: all scales + API access
    """
    
    def has_permission(self, request, view):
        """Check list permission."""
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """Check object permission based on scale type."""
        if not request.user.is_authenticated:
            # Unauthenticated users: only small scale
            scale = getattr(obj, 'scale_type', None) or getattr(obj, 'scale', None)
            if scale and hasattr(scale, 'scale_type'):
                scale = scale.scale_type
            return scale in [None, 'small']
        
        # Check based on user tier
        tier = getattr(request.user, 'tier', 'free')
        scale = getattr(obj, 'scale_type', None)
        
        # If obj is BusinessScale or has scale attribute
        if hasattr(obj, 'scale_type'):
            scale = obj.scale_type
        elif hasattr(obj, 'scale') and obj.scale:
            scale = obj.scale.scale_type
        
        if tier == 'enterprise':
            return True
        if tier == 'pro':
            return True  # Pro has all scales
        if tier == 'premium':
            return scale in [None, 'small', 'medium']
        # Free tier
        return scale in [None, 'small']


class CanAccessAPIData(permissions.BasePermission):
    """
    API access permission for enterprise clients.
    Checks valid API key in request headers.
    """
    
    def has_permission(self, request, view):
        """Check if request has valid API key."""
        from apps.core.models import APIKey
        from django.utils import timezone
        
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            return False
        
        try:
            key_obj = APIKey.objects.get(key=api_key, is_active=True)
            
            # Check expiration
            if key_obj.expires_at and key_obj.expires_at < timezone.now():
                return False
            
            # Update last used
            key_obj.last_used = timezone.now()
            key_obj.save(update_fields=['last_used'])
            
            # Store tier in request for later use
            request.api_tier = key_obj.tier
            
            return True
        except APIKey.DoesNotExist:
            return False


class CanAccessComparisonTool(permissions.BasePermission):
    """
    Comparison tool access.
    - Free: compare up to 2 businesses
    - Premium: compare up to 5 businesses
    - Pro/Enterprise: compare unlimited
    """
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            # Unauthenticated: limited to 2
            compare_ids = request.query_params.get('ids', '').split(',')
            if len(compare_ids) > 2 and compare_ids[0]:
                return False
            return True
        
        tier = getattr(request.user, 'tier', 'free')
        compare_ids = request.query_params.get('ids', '').split(',')
        
        if tier == 'free' and len(compare_ids) > 2 and compare_ids[0]:
            return False
        if tier == 'premium' and len(compare_ids) > 5 and compare_ids[0]:
            return False
        
        return True


class CanDownloadReport(permissions.BasePermission):
    """
    Check if user can download a report file.
    Similar to HasReportAccess but specifically for file downloads.
    """
    
    def has_object_permission(self, request, view, obj):
        """Check if user can download this report."""
        from apps.reports.models import ReportPurchase
        
        if not request.user.is_authenticated:
            return False
        
        # Check if report has a file
        if not obj.file:
            return False
        
        # Free reports
        if not getattr(obj, 'is_gated', True):
            return True
        
        # Subscription check
        if request.user.tier == 'enterprise':
            return True
        
        if request.user.tier == 'pro' and obj.tier_required in ['pro', 'premium']:
            return True
        
        if request.user.tier == 'premium' and obj.tier_required == 'premium':
            return True
        
        # One-time purchase check
        has_purchased = ReportPurchase.objects.filter(
            report=obj,
            user=request.user,
            status='completed'
        ).exists()
        
        return has_purchased


class CanAccessConsultantMatching(permissions.BasePermission):
    """
    Consultant matching feature access.
    Available to Pro and Enterprise users.
    """
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        tier = getattr(request.user, 'tier', 'free')
        return tier in ['pro', 'enterprise']


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners to edit.
    Assumes the model instance has a `user` or `owner` attribute.
    """
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Check if obj has user or owner attribute
        owner = getattr(obj, 'user', None) or getattr(obj, 'owner', None)
        if owner:
            return owner == request.user
        
        return request.user.is_staff