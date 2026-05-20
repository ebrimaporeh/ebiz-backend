from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.core.models import BaseModel
from apps.core.constants import Status
from apps.sectors.models import Sector
from apps.businesses.models import Business
from apps.users.models import User


class ReportType(models.TextChoices):
    INDUSTRY = 'industry', 'Industry Report'
    BUSINESS = 'business', 'Business Report'
    MARKET = 'market', 'Market Analysis'
    INVESTMENT = 'investment', 'Investment Guide'
    REGULATORY = 'regulatory', 'Regulatory Guide'
    TEMPLATE = 'template', 'Business Template'


class ReportFormat(models.TextChoices):
    PDF = 'pdf', 'PDF Document'
    EXCEL = 'excel', 'Excel Spreadsheet'
    WORD = 'word', 'Word Document'
    BUNDLE = 'bundle', 'Bundle Package'


# ============================================
# REPORT MODEL
# ============================================

class Report(BaseModel):
    """Premium reports and downloadable guides"""
    
    title = models.CharField(
        max_length=200,
        help_text="Report title"
    )
    
    subtitle = models.CharField(
        max_length=200,
        blank=True,
        help_text="Report subtitle or tagline"
    )
    
    description = models.TextField(
        help_text="Detailed description of the report"
    )
    
    short_description = models.CharField(
        max_length=200,
        blank=True,
        help_text="Short description for listings and cards"
    )
    
    cover_image = models.ImageField(
        upload_to='reports/covers/',
        blank=True,
        null=True,
        help_text="Cover image for the report"
    )
    
    file = models.FileField(
        upload_to='reports/files/',
        help_text="The actual report file (PDF, Excel, etc.)"
    )
    
    file_size = models.PositiveIntegerField(
        default=0,
        help_text="File size in bytes (auto-calculated)"
    )
    
    # Report type and relationships
    report_type = models.CharField(
        max_length=20,
        choices=ReportType.choices,
        default=ReportType.INDUSTRY,
        help_text="Type of report"
    )
    
    format = models.CharField(
        max_length=20,
        choices=ReportFormat.choices,
        default=ReportFormat.PDF,
        help_text="File format"
    )
    
    sector = models.ForeignKey(
        Sector,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reports',
        help_text="Sector this report belongs to"
    )
    
    business = models.ForeignKey(
        Business,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reports',
        help_text="Business this report belongs to"
    )
    
    # Pricing
    price = models.PositiveIntegerField(
        default=0,
        help_text="Price in Dalasi (0 for free)"
    )
    
    is_free = models.BooleanField(
        default=False,
        help_text="Whether this report is free to download"
    )
    
    # Content
    table_of_contents = models.TextField(
        blank=True,
        help_text="Table of contents (markdown or HTML)"
    )
    
    key_highlights = models.TextField(
        blank=True,
        help_text="Key highlights and takeaways"
    )
    
    # Metadata
    page_count = models.PositiveSmallIntegerField(
        default=0,
        help_text="Number of pages"
    )
    
    version = models.CharField(
        max_length=10,
        default="1.0",
        help_text="Report version"
    )
    
    author = models.CharField(
        max_length=100,
        default="GBI Research Team",
        help_text="Author or organization"
    )
    
    is_featured = models.BooleanField(
        default=False,
        help_text="Display on homepage and featured sections"
    )
    
    is_bestseller = models.BooleanField(
        default=False,
        help_text="Mark as bestseller"
    )
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        help_text="Publication status"
    )
    
    published_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the report was published"
    )
    
    # Stats
    download_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of downloads"
    )
    
    view_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of views"
    )
    
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0,
        help_text="Average rating (0-5)"
    )
    
    review_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of reviews"
    )
    
    # SEO
    meta_title = models.CharField(
        max_length=150,
        blank=True,
        help_text="SEO title (defaults to report title)"
    )
    
    meta_description = models.CharField(
        max_length=300,
        blank=True,
        help_text="SEO description"
    )
    
    class Meta:
        db_table = 'reports'
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'
        ordering = ['-is_featured', '-published_at', '-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['status', 'published_at']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['report_type']),
            models.Index(fields=['sector']),
            models.Index(fields=['business']),
            models.Index(fields=['download_count']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Report.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        
        # Calculate file size if file exists
        if self.file and not self.file_size:
            try:
                self.file_size = self.file.size
            except:
                pass
        
        # Set is_free based on price
        if self.price == 0:
            self.is_free = True
        
        super().save(*args, **kwargs)
    
    def increment_download_count(self):
        """Increment download count by 1"""
        self.download_count += 1
        self.save(update_fields=['download_count'])
    
    def increment_view_count(self):
        """Increment view count by 1"""
        self.view_count += 1
        self.save(update_fields=['view_count'])
    
    @property
    def price_display(self):
        """Display price in Dalasi format"""
        if self.price == 0:
            return "Free"
        return f"D{self.price:,}"
    
    @property
    def file_size_display(self):
        """Display file size in human-readable format"""
        if self.file_size < 1024:
            return f"{self.file_size} B"
        elif self.file_size < 1024 * 1024:
            return f"{self.file_size / 1024:.1f} KB"
        else:
            return f"{self.file_size / (1024 * 1024):.1f} MB"


# ============================================
# REPORT PURCHASE MODEL
# ============================================

class ReportPurchase(BaseModel):
    """Track individual report purchases"""
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='report_purchases',
        help_text="User who purchased the report"
    )
    
    report = models.ForeignKey(
        Report,
        on_delete=models.CASCADE,
        related_name='purchases',
        help_text="Report that was purchased"
    )
    
    amount_paid = models.PositiveIntegerField(
        help_text="Amount paid in Dalasi"
    )
    
    payment_method = models.CharField(
        max_length=50,
        blank=True,
        help_text="Payment method used"
    )
    
    transaction_reference = models.CharField(
        max_length=200,
        blank=True,
        unique=True,
        null=True,
        help_text="Transaction reference from payment processor"
    )
    
    is_paid = models.BooleanField(
        default=True,
        help_text="Whether payment has been confirmed"
    )
    
    paid_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When payment was made"
    )
    
    has_downloaded = models.BooleanField(
        default=False,
        help_text="Whether user has downloaded the report"
    )
    
    download_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of times downloaded"
    )
    
    last_downloaded_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Last download timestamp"
    )
    
    # For bundle purchases
    is_bundle = models.BooleanField(
        default=False,
        help_text="Whether this is part of a bundle purchase"
    )
    
    bundle_reference = models.CharField(
        max_length=100,
        blank=True,
        help_text="Reference for bundle purchases"
    )
    
    class Meta:
        db_table = 'report_purchases'
        verbose_name = 'Report Purchase'
        verbose_name_plural = 'Report Purchases'
        unique_together = ['user', 'report']
        ordering = ['-paid_at']
        indexes = [
            models.Index(fields=['user', 'report']),
            models.Index(fields=['transaction_reference']),
            models.Index(fields=['is_paid']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.report.title}"
    
    def record_download(self):
        """Record a download action"""
        self.download_count += 1
        self.has_downloaded = True
        from django.utils import timezone
        self.last_downloaded_at = timezone.now()
        self.save(update_fields=['download_count', 'has_downloaded', 'last_downloaded_at'])
        
        # Also increment report's download count
        self.report.increment_download_count()


# ============================================
# REPORT BUNDLE MODEL
# ============================================

class ReportBundle(BaseModel):
    """Bundle of multiple reports sold together"""
    
    name = models.CharField(
        max_length=200,
        help_text="Bundle name"
    )
    
    description = models.TextField(
        help_text="Bundle description"
    )
    
    reports = models.ManyToManyField(
        Report,
        related_name='bundles',
        help_text="Reports included in this bundle"
    )
    
    price = models.PositiveIntegerField(
        help_text="Bundle price in Dalasi"
    )
    
    original_price = models.PositiveIntegerField(
        help_text="Original total price of individual reports"
    )
    
    discount_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        help_text="Discount percentage (auto-calculated)"
    )
    
    cover_image = models.ImageField(
        upload_to='reports/bundles/',
        blank=True,
        null=True,
        help_text="Bundle cover image"
    )
    
    is_featured = models.BooleanField(
        default=False,
        help_text="Display on homepage and featured sections"
    )
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PUBLISHED,
        help_text="Publication status"
    )
    
    valid_until = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Optional expiry date for the bundle"
    )
    
    purchase_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of times this bundle was purchased"
    )
    
    class Meta:
        db_table = 'report_bundles'
        verbose_name = 'Report Bundle'
        verbose_name_plural = 'Report Bundles'
        ordering = ['-is_featured', '-created_at']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        
        # Calculate discount percentage
        if self.original_price > 0:
            discount = ((self.original_price - self.price) / self.original_price) * 100
            self.discount_percent = round(discount, 2)
        
        super().save(*args, **kwargs)
    
    @property
    def savings_display(self):
        """Display savings in Dalasi"""
        savings = self.original_price - self.price
        return f"D{savings:,}"
    
    @property
    def price_display(self):
        """Display price in Dalasi format"""
        return f"D{self.price:,}"
    
    @property
    def original_price_display(self):
        """Display original price in Dalasi format"""
        return f"D{self.original_price:,}"
    
    def increment_purchase_count(self):
        """Increment purchase count by 1"""
        self.purchase_count += 1
        self.save(update_fields=['purchase_count'])


# ============================================
# REPORT REVIEW MODEL
# ============================================

class ReportReview(BaseModel):
    """User reviews and ratings for reports"""
    
    report = models.ForeignKey(
        Report,
        on_delete=models.CASCADE,
        related_name='reviews',
        help_text="Report being reviewed"
    )
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='report_reviews',
        help_text="User who wrote the review"
    )
    
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5 stars"
    )
    
    title = models.CharField(
        max_length=200,
        help_text="Review title"
    )
    
    content = models.TextField(
        help_text="Review content"
    )
    
    is_verified_purchase = models.BooleanField(
        default=False,
        help_text="Whether reviewer purchased the report"
    )
    
    is_approved = models.BooleanField(
        default=False,
        help_text="Whether review is approved for display"
    )
    
    helpful_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of users who found this helpful"
    )
    
    class Meta:
        db_table = 'report_reviews'
        verbose_name = 'Report Review'
        verbose_name_plural = 'Report Reviews'
        unique_together = ['report', 'user']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.report.title} - {self.rating}★"
    
    def approve(self):
        """Approve the review and update report rating"""
        self.is_approved = True
        self.save(update_fields=['is_approved'])
        self.update_report_rating()
    
    def update_report_rating(self):
        """Update the report's average rating"""
        approved_reviews = self.report.reviews.filter(is_approved=True)
        if approved_reviews.exists():
            avg_rating = approved_reviews.aggregate(
                avg=models.Avg('rating')
            )['avg']
            self.report.rating = round(avg_rating, 2)
            self.report.review_count = approved_reviews.count()
            self.report.save(update_fields=['rating', 'review_count'])