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


class IsPremiumUser(permissions.BasePermission):
    """Premium content access for subscribers or one-time purchasers."""
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            if not request.user.is_authenticated:
                return False
            return request.user.has_premium_access()
        return request.user.is_authenticated