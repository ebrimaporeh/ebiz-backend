from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

from .models import User, UserProfile, Subscription, OneTimePurchase
from apps.core.constants import UserTier


# ============================================
# AUTHENTICATION SERIALIZERS
# ============================================

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Handles creating a new user with email and password.
    """
    
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
        help_text='Email address used for login.'
    )
    
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'},
        help_text='Password (minimum 8 characters).'
    )
    
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text='Confirm password.'
    )
    
    class Meta:
        model = User
        fields = (
            'email', 
            'password', 
            'password_confirm', 
            'first_name', 
            'last_name',
            'phone', 
            'location', 
            'is_entrepreneur', 
            'is_investor', 
            'is_student'
        )
        extra_kwargs = {
            'first_name': {'required': False, 'allow_blank': True},
            'last_name': {'required': False, 'allow_blank': True},
            'phone': {'required': False, 'allow_blank': True},
            'location': {'required': False, 'allow_blank': True},
            'is_entrepreneur': {'required': False},
            'is_investor': {'required': False},
            'is_student': {'required': False},
        }
    
    def validate(self, attrs):
        """Check that password and password_confirm match."""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                'password_confirm': 'Passwords do not match.'
            })
        return attrs
    
    def create(self, validated_data):
        """Create user and profile."""
        password = validated_data.pop('password')
        validated_data.pop('password_confirm')
        
        user = User.objects.create_user(
            email=validated_data.pop('email'),
            password=password,
            **validated_data
        )
        
        # Create profile
        UserProfile.objects.create(user=user)
        
        # Create auth token
        Token.objects.create(user=user)
        
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    Authenticates user and returns user data with token.
    """
    
    email = serializers.EmailField(
        required=True,
        help_text='Registered email address.'
    )
    
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text='Account password.'
    )
    
    def validate(self, attrs):
        """Authenticate user."""
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                email=email,
                password=password
            )
            
            if not user:
                raise serializers.ValidationError({
                    'error': 'Invalid email or password.'
                }, code='authorization')
            
            if not user.is_active:
                raise serializers.ValidationError({
                    'error': 'This account is disabled.'
                }, code='authorization')
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError({
                'error': 'Email and password are required.'
            }, code='authorization')


class UserLogoutSerializer(serializers.Serializer):
    """
    Serializer for user logout.
    Placeholder for logout validation.
    """
    pass


# ============================================
# PROFILE SERIALIZERS
# ============================================

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for UserProfile model.
    Handles user profile data including social links.
    """
    
    class Meta:
        model = UserProfile
        fields = (
            'avatar',
            'linkedin_url',
            'twitter_handle',
            'website_url',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('created_at', 'updated_at')
    
    def validate_linkedin_url(self, value):
        """Validate LinkedIn URL format."""
        if value and 'linkedin.com' not in value:
            raise serializers.ValidationError('Must be a valid LinkedIn URL.')
        return value


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    Returns user data with nested profile.
    """
    
    profile = UserProfileSerializer(read_only=True)
    full_name = serializers.ReadOnlyField()
    tier_display = serializers.ReadOnlyField()
    has_premium_access = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'phone',
            'location',
            'bio',
            'is_entrepreneur',
            'is_investor',
            'is_student',
            'tier',
            'tier_display',
            'has_premium_access',
            'newsletter_subscribed',
            'email_notifications',
            'date_joined',
            'profile',
        )
        read_only_fields = (
            'id', 
            'email', 
            'date_joined', 
            'full_name', 
            'tier', 
            'tier_display', 
            'has_premium_access'
        )


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile.
    Allows users to update their own information.
    """
    
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'phone',
            'location',
            'bio',
            'is_entrepreneur',
            'is_investor',
            'is_student',
            'newsletter_subscribed',
            'email_notifications',
        )
    
    def update(self, instance, validated_data):
        """Update user instance with validated data."""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class UserPreferencesSerializer(serializers.ModelSerializer):
    """
    Serializer for user preferences.
    Separate serializer for preference updates.
    """
    
    class Meta:
        model = User
        fields = (
            'newsletter_subscribed',
            'email_notifications',
        )


# ============================================
# PASSWORD MANAGEMENT SERIALIZERS
# ============================================

class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing password.
    Requires old password and new password confirmation.
    """
    
    old_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text='Current password.'
    )
    
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'},
        help_text='New password (minimum 8 characters).'
    )
    
    new_password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text='Confirm new password.'
    )
    
    def validate(self, attrs):
        """Check that new passwords match."""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({
                'new_password_confirm': 'Passwords do not match.'
            })
        return attrs


class ForgotPasswordSerializer(serializers.Serializer):
    """
    Serializer for forgot password request.
    Validates email exists and triggers password reset email.
    """
    
    email = serializers.EmailField(
        required=True,
        help_text='Email address associated with your account.'
    )
    
    def validate_email(self, value):
        """Check if user exists with this email."""
        if not User.objects.filter(email=value, is_active=True).exists():
            raise serializers.ValidationError(
                'No active account found with this email address.'
            )
        return value


class ResetPasswordSerializer(serializers.Serializer):
    """
    Serializer for password reset with token.
    Validates token and sets new password.
    """
    
    token = serializers.CharField(
        required=True,
        help_text='Password reset token received via email.'
    )
    
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'},
        help_text='New password (minimum 8 characters).'
    )
    
    new_password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text='Confirm new password.'
    )
    
    def validate(self, attrs):
        """Check that new passwords match."""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({
                'new_password_confirm': 'Passwords do not match.'
            })
        return attrs


# ============================================
# SUBSCRIPTION SERIALIZERS
# ============================================

class SubscriptionSerializer(serializers.ModelSerializer):
    """
    Serializer for Subscription model.
    Returns subscription details for a user.
    """
    
    plan_type_display = serializers.ReadOnlyField(source='get_plan_type_display')
    amount_display = serializers.SerializerMethodField()
    is_expired = serializers.ReadOnlyField()
    days_remaining = serializers.ReadOnlyField()
    
    class Meta:
        model = Subscription
        fields = (
            'id',
            'plan_type',
            'plan_type_display',
            'amount',
            'amount_display',
            'duration_days',
            'started_at',
            'expires_at',
            'is_active',
            'is_expired',
            'days_remaining',
            'is_paid',
            'paid_at',
            'created_at',
        )
        read_only_fields = (
            'id', 'started_at', 'expires_at', 'is_active', 'is_expired', 
            'days_remaining', 'is_paid', 'paid_at', 'created_at'
        )
    
    def get_amount_display(self, obj):
        """Format amount as Dalasi."""
        return f"D{obj.amount:,}"
    
    def validate(self, attrs):
        """Ensure plan_type is Premium for subscriptions."""
        if attrs.get('plan_type') != UserTier.PREMIUM:
            attrs['plan_type'] = UserTier.PREMIUM
        return attrs


class CreateSubscriptionSerializer(serializers.Serializer):
    """
    Serializer for creating a new subscription.
    Used when user purchases a premium subscription.
    """
    
    plan_type = serializers.ChoiceField(
        choices=[(UserTier.PREMIUM, UserTier.PREMIUM.label)],
        default=UserTier.PREMIUM,
        help_text='Subscription plan type (only Premium available).'
    )
    
    duration_days = serializers.ChoiceField(
        choices=[(30, '30 days'), (90, '90 days'), (365, '365 days')],
        default=30,
        help_text='Subscription duration in days.'
    )
    
    payment_method = serializers.CharField(
        max_length=50,
        required=False,
        allow_blank=True,
        help_text='Payment method used.'
    )
    
    transaction_reference = serializers.CharField(
        max_length=200,
        required=False,
        allow_blank=True,
        help_text='Transaction reference from payment processor.'
    )
    
    def validate_duration_days(self, value):
        """Validate duration days and calculate amount."""
        self.duration_days = value
        return value
    
    def validate(self, attrs):
        """Calculate amount based on duration."""
        # Pricing: D500 for 30 days, D1,350 for 90 days (10% discount), D5,000 for 365 days (17% discount)
        pricing = {
            30: 500,
            90: 1350,
            365: 5000,
        }
        duration = attrs.get('duration_days', 30)
        attrs['amount'] = pricing.get(duration, 500)
        return attrs


# ============================================
# ONE-TIME PURCHASE SERIALIZERS
# ============================================

class OneTimePurchaseSerializer(serializers.ModelSerializer):
    """
    Serializer for OneTimePurchase model.
    Returns purchase details for a user.
    """
    
    amount_display = serializers.SerializerMethodField()
    
    class Meta:
        model = OneTimePurchase
        fields = (
            'id',
            'report_id',
            'report_title',
            'amount',
            'amount_display',
            'purchased_at',
            'has_downloaded',
            'download_count',
            'last_downloaded_at',
        )
        read_only_fields = (
            'id', 'purchased_at', 'has_downloaded', 'download_count', 'last_downloaded_at'
        )
    
    def get_amount_display(self, obj):
        """Format amount as Dalasi."""
        return f"D{obj.amount:,}"


class CreateOneTimePurchaseSerializer(serializers.Serializer):
    """
    Serializer for creating a one-time purchase.
    Used when user buys a report.
    """
    
    report_id = serializers.IntegerField(
        required=True,
        help_text='ID of the report being purchased.'
    )
    
    report_title = serializers.CharField(
        max_length=200,
        required=True,
        help_text='Title of the report being purchased.'
    )
    
    amount = serializers.IntegerField(
        required=True,
        min_value=1,
        help_text='Amount paid for the report in Dalasi.'
    )
    
    payment_method = serializers.CharField(
        max_length=50,
        required=False,
        allow_blank=True,
        help_text='Payment method used.'
    )
    
    transaction_reference = serializers.CharField(
        max_length=200,
        required=False,
        allow_blank=True,
        help_text='Transaction reference from payment processor.'
    )
    
    def validate(self, attrs):
        """Check if user already purchased this report."""
        user = self.context.get('user')
        report_id = attrs.get('report_id')
        
        if user and report_id:
            if OneTimePurchase.objects.filter(user=user, report_id=report_id).exists():
                raise serializers.ValidationError({
                    'report_id': 'You have already purchased this report.'
                })
        
        return attrs


# ============================================
# TOKEN SERIALIZERS
# ============================================

class TokenSerializer(serializers.ModelSerializer):
    """
    Serializer for auth token.
    Returns token data after login.
    """
    
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Token
        fields = ('key', 'user', 'created')
        read_only_fields = ('key', 'created')


# ============================================
# PUBLIC PROFILE SERIALIZER (for displaying user info to others)
# ============================================

class PublicUserSerializer(serializers.ModelSerializer):
    """
    Serializer for public user profiles.
    Limited fields to protect privacy.
    """
    
    full_name = serializers.ReadOnlyField()
    initials = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = (
            'id',
            'full_name',
            'location',
            'bio',
            'is_entrepreneur',
            'is_investor',
            'is_student',
            'initials',
        )
        read_only_fields = fields
    
    def get_initials(self, obj):
        """Get user initials for avatar placeholder."""
        if obj.first_name or obj.last_name:
            first = obj.first_name[0] if obj.first_name else ''
            last = obj.last_name[0] if obj.last_name else ''
            return f"{first}{last}".upper()
        return obj.email[0].upper()