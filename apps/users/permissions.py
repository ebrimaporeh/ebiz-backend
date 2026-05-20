from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow users to edit only their own profile.
    Read-only for others.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only to the owner
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return obj == request.user


class HasPremiumAccess(permissions.BasePermission):
    """
    Permission to check if user has premium access.
    Used for premium content endpoints.
    """
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.has_premium_access


class HasPurchasedReport(permissions.BasePermission):
    """
    Permission to check if user has purchased a specific report.
    Used for report download endpoints.
    """
    
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        # Check if user has purchased this report
        from .models import OneTimePurchase
        report_id = obj.id if hasattr(obj, 'id') else obj
        return OneTimePurchase.objects.filter(
            user=request.user, 
            report_id=report_id,
            is_paid=True
        ).exists()


class CanManageSubscriptions(permissions.BasePermission):
    """
    Permission for managing subscriptions.
    Only staff or the subscription owner can manage.
    """
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        
        # Check if the user is the subscription owner
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return False