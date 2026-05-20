from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.core.validators import EmailValidator, MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

from apps.core.constants import UserTier


class UserManager(BaseUserManager):
    """Custom user manager with email as username."""

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular user."""
        if not email:
            raise ValueError('Email address is required')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superuser."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('tier', UserTier.PREMIUM)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model with email as username field.
    Supports tier-based access: Regular, Premium, One-time Purchase.
    """
    
    # ============================================
    # BASIC INFORMATION
    # ============================================
    
    email = models.EmailField(
        max_length=255,
        unique=True,
        validators=[EmailValidator()],
        error_messages={
            'unique': 'A user with this email already exists.',
        },
        help_text='Email address used for login and notifications.'
    )
    
    first_name = models.CharField(
        max_length=100, 
        blank=True,
        help_text='User\'s first name.'
    )
    
    last_name = models.CharField(
        max_length=100, 
        blank=True,
        help_text='User\'s last name.'
    )
    
    phone = models.CharField(
        max_length=20, 
        blank=True,
        help_text='Contact phone number.'
    )
    
    # ============================================
    # LOCATION & BIO
    # ============================================
    
    location = models.CharField(
        max_length=200, 
        blank=True,
        help_text='City or region where the user is based.'
    )
    
    bio = models.TextField(
        blank=True,
        help_text='Short bio or professional background.'
    )
    
    # ============================================
    # USER TYPE FLAGS
    # ============================================
    
    is_entrepreneur = models.BooleanField(
        default=False,
        help_text='User identifies as an entrepreneur.'
    )
    
    is_investor = models.BooleanField(
        default=False,
        help_text='User identifies as an investor (local or diaspora).'
    )
    
    is_student = models.BooleanField(
        default=False,
        help_text='User is a student learning about business.'
    )
    
    # ============================================
    # ACCOUNT STATUS
    # ============================================
    
    is_active = models.BooleanField(
        default=True,
        help_text='Designates whether this user should be treated as active.'
    )
    
    is_staff = models.BooleanField(
        default=False,
        help_text='Designates whether the user can log into this admin site.'
    )
    
    date_joined = models.DateTimeField(
        default=timezone.now,
        help_text='Date and time when the user registered.'
    )
    
    last_login_ip = models.GenericIPAddressField(
        null=True, 
        blank=True,
        help_text='IP address of the last login.'
    )
    
    # ============================================
    # USER TIER (Access Level)
    # ============================================
    
    tier = models.CharField(
        max_length=20,
        choices=UserTier.choices,
        default=UserTier.REGULAR,
        help_text='Access level: Regular (free), Premium (subscription), One-time Purchase.'
    )
    
    tier_expires_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='For Premium users, when the subscription expires. Null for Regular or One-time.'
    )
    
    # ============================================
    # PREFERENCES
    # ============================================
    
    newsletter_subscribed = models.BooleanField(
        default=True,
        help_text='User has opted in to receive email newsletters.'
    )
    
    email_notifications = models.BooleanField(
        default=True,
        help_text='User wants to receive email notifications.'
    )
    
    # ============================================
    # METADATA
    # ============================================
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['tier']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return self.email
    
    @property
    def full_name(self):
        """Return full name if available, otherwise email."""
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}".strip()
        return self.email
    
    @property
    def has_premium_access(self):
        """
        Check if user has access to premium content.
        Returns True for Premium (if not expired) and One-time Purchase users.
        """
        if self.tier == UserTier.ONE_TIME:
            return True
        if self.tier == UserTier.PREMIUM:
            if self.tier_expires_at:
                return self.tier_expires_at > timezone.now()
            return True  # No expiry date means active
        return False
    
    @property
    def tier_display(self):
        """Human-readable tier name."""
        return UserTier(self.tier).label
    
    def upgrade_to_premium(self, duration_days=30):
        """
        Upgrade user to Premium tier.
        If already Premium, extend the expiry date.
        """
        self.tier = UserTier.PREMIUM
        new_expiry = timezone.now() + timezone.timedelta(days=duration_days)
        
        if self.tier_expires_at and self.tier_expires_at > timezone.now():
            # Extend existing subscription
            self.tier_expires_at = self.tier_expires_at + timezone.timedelta(days=duration_days)
        else:
            self.tier_expires_at = new_expiry
        
        self.save()
    
    def upgrade_to_one_time(self):
        """
        Upgrade user to One-time Purchase tier.
        This grants permanent access to purchased content.
        """
        self.tier = UserTier.ONE_TIME
        self.tier_expires_at = None  # No expiration
        self.save()
    
    def downgrade_to_regular(self):
        """Downgrade user to Regular (free) tier."""
        self.tier = UserTier.REGULAR
        self.tier_expires_at = None
        self.save()


class UserProfile(models.Model):
    """
    Extended user profile for additional data and saved items.
    One-to-one relationship with User.
    """
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        help_text='The user this profile belongs to.'
    )
    
    # ============================================
    # PROFILE PICTURE
    # ============================================
    
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        help_text='Profile picture/avatar.'
    )
    
    # ============================================
    # SOCIAL LINKS
    # ============================================
    
    linkedin_url = models.URLField(
        blank=True,
        help_text='LinkedIn profile URL.'
    )
    
    twitter_handle = models.CharField(
        max_length=100,
        blank=True,
        help_text='Twitter/X handle (without @).'
    )
    
    website_url = models.URLField(
        blank=True,
        help_text='Personal or business website.'
    )
    
    # ============================================
    # BUSINESS INTERESTS (Many-to-many via separate model)
    # ============================================
    # This will be populated when we have the businesses app
    
    # ============================================
    # SAVED CONTENT (Many-to-many via separate models)
    # ============================================
    # saved_businesses = models.ManyToManyField('businesses.Business', blank=True)
    # saved_reports = models.ManyToManyField('reports.Report', blank=True)
    # saved_articles = models.ManyToManyField('content.Article', blank=True)
    
    # ============================================
    # METADATA
    # ============================================
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_profiles'
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
    
    def __str__(self):
        return f"Profile: {self.user.email}"
    
    def get_initials(self):
        """Return user initials for avatar placeholder."""
        first = self.user.first_name[0] if self.user.first_name else ''
        last = self.user.last_name[0] if self.user.last_name else ''
        if first or last:
            return f"{first}{last}".upper()
        return self.user.email[0].upper()


class Subscription(models.Model):
    """
    Track subscription payments and history.
    """
    
    # ============================================
    # RELATIONSHIPS
    # ============================================
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        help_text='User who made the subscription purchase.'
    )
    
    # ============================================
    # SUBSCRIPTION DETAILS
    # ============================================
    
    plan_type = models.CharField(
        max_length=20,
        choices=UserTier.choices,
        default=UserTier.PREMIUM,
        help_text='Type of subscription purchased.'
    )
    
    amount = models.PositiveIntegerField(
        help_text='Amount paid in Dalasi (D).'
    )
    
    duration_days = models.PositiveIntegerField(
        default=30,
        help_text='Number of days the subscription covers.'
    )
    
    started_at = models.DateTimeField(
        default=timezone.now,
        help_text='Date and time when the subscription started.'
    )
    
    expires_at = models.DateTimeField(
        help_text='Date and time when the subscription expires.'
    )
    
    # ============================================
    # PAYMENT INFORMATION
    # ============================================
    
    payment_method = models.CharField(
        max_length=50,
        blank=True,
        help_text='Payment method used (card, mobile money, bank transfer, etc.)'
    )
    
    transaction_reference = models.CharField(
        max_length=200,
        blank=True,
        unique=True,
        null=True,
        help_text='Reference number from payment processor.'
    )
    
    is_paid = models.BooleanField(
        default=True,
        help_text='Whether payment has been confirmed.'
    )
    
    paid_at = models.DateTimeField(
        default=timezone.now,
        help_text='Date and time when payment was confirmed.'
    )
    
    # ============================================
    # STATUS
    # ============================================
    
    is_active = models.BooleanField(
        default=True,
        help_text='Whether this subscription is currently active.'
    )
    
    cancelled_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Date and time when subscription was cancelled.'
    )
    
    # ============================================
    # METADATA
    # ============================================
    
    notes = models.TextField(
        blank=True,
        help_text='Internal notes about this subscription.'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'subscriptions'
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['expires_at']),
            models.Index(fields=['transaction_reference']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.get_plan_type_display()} - {self.started_at.date()}"
    
    def save(self, *args, **kwargs):
        """Auto-calculate expires_at based on started_at and duration_days."""
        if not self.expires_at and self.started_at and self.duration_days:
            self.expires_at = self.started_at + timezone.timedelta(days=self.duration_days)
        super().save(*args, **kwargs)
    
    @property
    def is_expired(self):
        """Check if subscription has expired."""
        if self.expires_at is None:
            return False
        return self.expires_at < timezone.now()
    
    @property
    def days_remaining(self):
        """Number of days remaining until expiry."""
        if not self.expires_at:
            return 0

        if self.expires_at < timezone.now():
            return 0

        return (self.expires_at - timezone.now()).days


class OneTimePurchase(models.Model):
    """
    Track one-time purchases of reports or guides.
    Users with one-time purchases get permanent access to specific content.
    """
    
    # ============================================
    # RELATIONSHIPS
    # ============================================
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='purchases',
        help_text='User who made the purchase.'
    )
    
    # This will reference reports.Report when that app is created
    # report = models.ForeignKey('reports.Report', on_delete=models.CASCADE)
    report_id = models.PositiveIntegerField(
        help_text='ID of the purchased report (temporary until reports app exists).'
    )
    report_title = models.CharField(
        max_length=200,
        help_text='Title of the purchased report.'
    )
    
    # ============================================
    # PURCHASE DETAILS
    # ============================================
    
    amount = models.PositiveIntegerField(
        help_text='Amount paid in Dalasi (D).'
    )
    
    payment_method = models.CharField(
        max_length=50,
        blank=True,
        help_text='Payment method used.'
    )
    
    transaction_reference = models.CharField(
        max_length=200,
        blank=True,
        unique=True,
        null=True,
        help_text='Reference number from payment processor.'
    )
    
    is_paid = models.BooleanField(
        default=True,
        help_text='Whether payment has been confirmed.'
    )
    
    purchased_at = models.DateTimeField(
        default=timezone.now,
        help_text='Date and time of purchase.'
    )
    
    # ============================================
    # ACCESS
    # ============================================
    
    has_downloaded = models.BooleanField(
        default=False,
        help_text='Whether the user has downloaded the report.'
    )
    
    download_count = models.PositiveIntegerField(
        default=0,
        help_text='Number of times the report has been downloaded.'
    )
    
    last_downloaded_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Date and time of last download.'
    )
    
    # ============================================
    # METADATA
    # ============================================
    
    notes = models.TextField(
        blank=True,
        help_text='Internal notes about this purchase.'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'one_time_purchases'
        verbose_name = 'One-Time Purchase'
        verbose_name_plural = 'One-Time Purchases'
        indexes = [
            models.Index(fields=['user', 'report_id']),
            models.Index(fields=['transaction_reference']),
        ]
        unique_together = ['user', 'report_id']  # One purchase per report per user
        ordering = ['-purchased_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.report_title} - {self.purchased_at.date()}"
    
    def record_download(self):
        """Increment download counter and record timestamp."""
        self.download_count += 1
        self.has_downloaded = True
        self.last_downloaded_at = timezone.now()
        self.save()