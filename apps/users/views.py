from rest_framework import status, generics, viewsets, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.decorators import action
from django.contrib.auth import logout as django_logout
from django.utils import timezone

from .models import User, UserProfile, Subscription, OneTimePurchase
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserLogoutSerializer,
    UserProfileSerializer,
    UserSerializer,
    UserUpdateSerializer,
    UserPreferencesSerializer,
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
    SubscriptionSerializer,
    CreateSubscriptionSerializer,
    OneTimePurchaseSerializer,
    CreateOneTimePurchaseSerializer,
    TokenSerializer,
    PublicUserSerializer,
)
from .permissions import (
    IsOwnerOrReadOnly,
    HasPremiumAccess,
    HasPurchasedReport,
    CanManageSubscriptions,
)
from apps.core.permissions import IsAuthenticatedOrReadOnly


# ============================================
# AUTHENTICATION VIEWS
# ============================================

class RegisterView(generics.CreateAPIView):
    """
    User registration endpoint.
    
    Creates a new user account with email and password.
    Returns user data and authentication token.
    
    POST /api/v1/auth/register/
    """
    
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Get or create token
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key,
            'message': 'Registration successful.'
        }, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    """
    User login endpoint.
    
    Authenticates user with email and password.
    Returns user data and authentication token.
    
    POST /api/v1/auth/login/
    """
    
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        # Update last login IP
        user.last_login_ip = self.get_client_ip(request)
        user.save(update_fields=['last_login_ip'])
        
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key,
            'message': 'Login successful.'
        }, status=status.HTTP_200_OK)
    
    def get_client_ip(self, request):
        """Extract client IP from request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class LogoutView(APIView):
    """
    User logout endpoint.
    
    Deletes the user's authentication token.
    
    POST /api/v1/auth/logout/
    """
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        # Delete the user's token
        request.user.auth_token.delete()
        
        # Also logout from Django session if using session auth
        django_logout(request)
        
        return Response({
            'message': 'Logout successful.'
        }, status=status.HTTP_200_OK)


# ============================================
# USER PROFILE VIEWS
# ============================================

class MeView(generics.RetrieveUpdateAPIView):
    """
    Get and update current user profile.
    
    Returns full user data including profile information.
    Only accessible to authenticated users.
    
    GET /api/v1/auth/me/
    PUT /api/v1/auth/me/
    PATCH /api/v1/auth/me/
    """
    
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def get_serializer_class(self):
        """Use different serializer for update operations."""
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    User profile endpoint.
    
    Get or update user profile data (avatar, social links, etc.).
    
    GET /api/v1/users/profile/
    PUT /api/v1/users/profile/
    PATCH /api/v1/users/profile/
    """
    
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_object(self):
        return self.request.user.profile


class UserPreferencesView(generics.RetrieveUpdateAPIView):
    """
    User preferences endpoint.
    
    Get or update notification preferences.
    
    GET /api/v1/users/preferences/
    PUT /api/v1/users/preferences/
    PATCH /api/v1/users/preferences/
    """
    
    serializer_class = UserPreferencesSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class ChangePasswordView(generics.GenericAPIView):
    """
    Change password endpoint.
    
    Requires old password and new password confirmation.
    
    POST /api/v1/auth/change-password/
    """
    
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        
        # Check old password
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({
                'old_password': 'Current password is incorrect.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Set new password
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        # Optionally invalidate all existing tokens
        # Token.objects.filter(user=user).delete()
        
        return Response({
            'message': 'Password changed successfully.'
        }, status=status.HTTP_200_OK)


class ForgotPasswordView(generics.GenericAPIView):
    """
    Forgot password endpoint.
    
    Sends password reset email to the provided email address.
    
    POST /api/v1/auth/forgot-password/
    """
    
    serializer_class = ForgotPasswordSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        user = User.objects.get(email=email)
        
        # TODO: Generate password reset token and send email
        # This will be implemented when email service is ready
        
        # For now, just return success without sending email
        return Response({
            'message': 'If an account exists with this email, you will receive password reset instructions.'
        }, status=status.HTTP_200_OK)


class ResetPasswordView(generics.GenericAPIView):
    """
    Reset password endpoint.
    
    Validates token and sets new password.
    
    POST /api/v1/auth/reset-password/
    """
    
    serializer_class = ResetPasswordSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']
        
        # TODO: Validate token and reset password
        # This will be implemented when token system is ready
        
        return Response({
            'message': 'Password reset successful.'
        }, status=status.HTTP_200_OK)


# ============================================
# SUBSCRIPTION VIEWSET
# ============================================

class SubscriptionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user subscriptions.
    
    Provides CRUD operations for subscriptions.
    Only staff or subscription owners can access.
    
    GET /api/v1/subscriptions/
    GET /api/v1/subscriptions/{id}/
    POST /api/v1/subscriptions/
    PUT /api/v1/subscriptions/{id}/
    PATCH /api/v1/subscriptions/{id}/
    DELETE /api/v1/subscriptions/{id}/
    """
    
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated, CanManageSubscriptions]
    
    def get_queryset(self):
        """Return subscriptions for the current user, or all for staff."""
        if self.request.user.is_staff:
            return Subscription.objects.all()
        return Subscription.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Create subscription for current user."""
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['post'], url_path='create')
    def create_subscription(self, request):
        """
        Create a new subscription for the current user.
        
        POST /api/v1/subscriptions/create/
        """
        serializer = CreateSubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        data = serializer.validated_data
        
        # Create subscription
        subscription = Subscription.objects.create(
            user=user,
            plan_type=data['plan_type'],
            amount=data['amount'],
            duration_days=data['duration_days'],
            payment_method=data.get('payment_method', ''),
            transaction_reference=data.get('transaction_reference', ''),
        )
        
        # Upgrade user tier
        user.upgrade_to_premium(duration_days=data['duration_days'])
        
        return Response(
            SubscriptionSerializer(subscription).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel_subscription(self, request, pk=None):
        """
        Cancel an active subscription.
        
        POST /api/v1/subscriptions/{id}/cancel/
        """
        subscription = self.get_object()
        
        if not subscription.is_active:
            return Response({
                'error': 'Subscription is already inactive or expired.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        subscription.is_active = False
        subscription.cancelled_at = timezone.now()
        subscription.save()
        
        return Response({
            'message': 'Subscription cancelled successfully.',
            'subscription': SubscriptionSerializer(subscription).data
        }, status=status.HTTP_200_OK)


# ============================================
# ONE-TIME PURCHASE VIEWSET
# ============================================

class OneTimePurchaseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing one-time purchases.
    
    Provides CRUD operations for purchased reports.
    
    GET /api/v1/purchases/
    GET /api/v1/purchases/{id}/
    POST /api/v1/purchases/
    """
    
    serializer_class = OneTimePurchaseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return purchases for the current user."""
        return OneTimePurchase.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Create purchase for current user."""
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['post'], url_path='create')
    def create_purchase(self, request):
        """
        Create a new one-time purchase for a report.
        
        POST /api/v1/purchases/create/
        """
        serializer = CreateOneTimePurchaseSerializer(
            data=request.data,
            context={'user': request.user}
        )
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        data = serializer.validated_data
        
        # Create purchase
        purchase = OneTimePurchase.objects.create(
            user=user,
            report_id=data['report_id'],
            report_title=data['report_title'],
            amount=data['amount'],
            payment_method=data.get('payment_method', ''),
            transaction_reference=data.get('transaction_reference', ''),
        )
        
        # Check if user should be upgraded to one-time tier
        # Only if they don't already have premium access
        if not user.has_premium_access:
            user.upgrade_to_one_time()
        
        return Response(
            OneTimePurchaseSerializer(purchase).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'], url_path='download')
    def record_download(self, request, pk=None):
        """
        Record a download for a purchased report.
        
        POST /api/v1/purchases/{id}/download/
        """
        purchase = self.get_object()
        
        purchase.record_download()
        
        return Response({
            'message': 'Download recorded successfully.',
            'download_count': purchase.download_count,
            'has_downloaded': purchase.has_downloaded
        }, status=status.HTTP_200_OK)


# ============================================
# PUBLIC USER VIEW
# ============================================

class PublicUserView(generics.RetrieveAPIView):
    """
    Public user profile endpoint.
    
    Returns limited user information for public viewing.
    
    GET /api/v1/users/public/{id}/
    """
    
    serializer_class = PublicUserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = User.objects.filter(is_active=True)
    lookup_field = 'id'