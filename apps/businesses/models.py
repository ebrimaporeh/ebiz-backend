from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
import os
from django.utils import timezone
from apps.core.models import BaseModel
from apps.core.constants import Status, ScaleType, Priority, RiskCategory, FeasibilityCategory
from apps.sectors.models import Sector


# ============================================
# BUSINESS MODEL
# ============================================

def business_image_path(instance, filename):
    """Generate path for business images: businesses/slug/filename.jpg"""
    ext = filename.split('.')[-1] if '.' in filename else 'jpg'
    new_filename = f"{timezone.now().strftime('%Y%m%d%H%M%S')}.{ext}"
    return f"businesses/{instance.slug}/{new_filename}"


class Business(BaseModel):
    """Main business entity (e.g., Poultry Farming, Taxi Services)"""
    
    sector = models.ForeignKey(
        Sector,
        on_delete=models.CASCADE,
        related_name='businesses',
        help_text="Sector this business belongs to"
    )
    
    name = models.CharField(
        max_length=200,
        help_text="Business name (e.g., Poultry Farming - Broilers)"
    )
    
    short_description = models.CharField(
        max_length=200,
        blank=True,
        help_text="Short tagline for cards and listings"
    )
    
    overview = models.TextField(
        help_text="2-3 paragraph explanation of what this business does day-to-day"
    )
    
    opportunity_thesis = models.TextField(
        help_text="Why this business makes sense in The Gambia today"
    )
    
    featured_image = models.ImageField(
        upload_to=business_image_path,
        blank=True,
        null=True,
        help_text="Main image for the business"
    )
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        help_text="Publication status"
    )
    
    is_featured = models.BooleanField(
        default=False,
        help_text="Display on homepage and featured sections"
    )
    
    view_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of times this business has been viewed"
    )
    
    class Meta:
        db_table = 'businesses'
        verbose_name = 'Business'
        verbose_name_plural = 'Businesses'
        ordering = ['-is_featured', 'name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['sector', 'status']),
            models.Index(fields=['is_featured']),
        ]
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Business.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def increment_view_count(self):
        """Increment view count by 1"""
        self.view_count += 1
        self.save(update_fields=['view_count'])


# ============================================
# BUSINESS SCALE
# ============================================

class BusinessScale(models.Model):
    """Scale-specific data for a business (Small, Medium, Large)"""
    
    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name='scales',
        help_text="Business this scale belongs to"
    )
    
    scale_type = models.CharField(
        max_length=20,
        choices=ScaleType.choices,
        help_text="Small, Medium, or Large scale"
    )
    
    # Scale Definition
    capacity_definition = models.CharField(
        max_length=200,
        help_text="e.g., '100-300 birds', '1-3 vehicles', '50-100 students'"
    )
    
    target_market = models.TextField(
        help_text="Who buys from this scale (e.g., local households, restaurants)"
    )
    
    location_type = models.CharField(
        max_length=100,
        help_text="Where it operates (e.g., backyard, peri-urban, rural commercial)"
    )
    
    labor_needed = models.CharField(
        max_length=100,
        help_text="Staff requirements (e.g., '1 part-time', '3+ employees')"
    )
    
    # Feasibility
    overall_feasibility_score = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
        help_text="Overall feasibility score out of 10"
    )
    
    # Metadata
    last_updated = models.DateField(
        auto_now=True,
        help_text="Date when this scale data was last updated"
    )
    
    class Meta:
        db_table = 'business_scales'
        verbose_name = 'Business Scale'
        verbose_name_plural = 'Business Scales'
        unique_together = ['business', 'scale_type']
        ordering = ['business', 'scale_type']
    
    def __str__(self):
        return f"{self.business.name} - {self.get_scale_type_display()}"
    
    @property
    def scale_label(self):
        return self.get_scale_type_display()


# ============================================
# CAPITAL REQUIREMENTS
# ============================================

class CapitalItem(models.Model):
    """Itemized startup costs for a specific business scale"""
    
    scale = models.ForeignKey(
        BusinessScale,
        on_delete=models.CASCADE,
        related_name='capital_items',
        help_text="Business scale these costs apply to"
    )
    
    category = models.CharField(
        max_length=50,
        choices=[
            ('registration', 'Registration & Legal'),
            ('premises', 'Premises & Housing'),
            ('equipment', 'Equipment & Tools'),
            ('inventory', 'Initial Inventory'),
        ],
        help_text="Category of capital expense"
    )
    
    item_name = models.CharField(
        max_length=200,
        help_text="Name of the item (e.g., 'Day-old Chicks', 'Poultry House')"
    )
    
    quantity = models.PositiveIntegerField(
        default=1,
        help_text="Number of units needed"
    )
    
    unit_cost = models.PositiveIntegerField(
        help_text="Cost per unit in Dalasi"
    )
    
    total_cost = models.PositiveIntegerField(
        editable=False,
        help_text="Quantity × Unit Cost (auto-calculated)"
    )
    
    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.ESSENTIAL,
        help_text="How essential this item is"
    )
    
    notes = models.TextField(
        blank=True,
        help_text="Additional information or where to buy"
    )
    
    class Meta:
        db_table = 'capital_items'
        verbose_name = 'Capital Item'
        verbose_name_plural = 'Capital Items'
        ordering = ['scale', 'category', 'priority', 'item_name']
    
    def save(self, *args, **kwargs):
        self.total_cost = self.quantity * self.unit_cost
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.item_name} - D{self.total_cost:,}"


# ============================================
# OPERATING COSTS
# ============================================

class OperatingCost(models.Model):
    """Weekly operating costs for a specific business scale"""
    
    scale = models.ForeignKey(
        BusinessScale,
        on_delete=models.CASCADE,
        related_name='operating_costs',
        help_text="Business scale these costs apply to"
    )
    
    week_range = models.CharField(
        max_length=20,
        help_text="Week range (e.g., '1-2', '3-4', '5-6', '7-8')"
    )
    
    # Feed costs (specific to poultry/agriculture - make generic for other businesses)
    feed_starter = models.PositiveIntegerField(
        default=0,
        help_text="Cost of starter feed (if applicable)"
    )
    
    feed_grower = models.PositiveIntegerField(
        default=0,
        help_text="Cost of grower feed (if applicable)"
    )
    
    feed_finisher = models.PositiveIntegerField(
        default=0,
        help_text="Cost of finisher feed (if applicable)"
    )
    
    # Generic costs
    utilities = models.PositiveIntegerField(
        default=0,
        help_text="Electricity, water, etc."
    )
    
    water = models.PositiveIntegerField(
        default=0,
        help_text="Water costs"
    )
    
    medication = models.PositiveIntegerField(
        default=0,
        help_text="Medication, vaccines, etc."
    )
    
    labor = models.PositiveIntegerField(
        default=0,
        help_text="Staff wages"
    )
    
    transport_misc = models.PositiveIntegerField(
        default=0,
        help_text="Transportation and miscellaneous costs"
    )
    
    total = models.PositiveIntegerField(
        editable=False,
        help_text="Sum of all costs (auto-calculated)"
    )
    
    class Meta:
        db_table = 'operating_costs'
        verbose_name = 'Operating Cost'
        verbose_name_plural = 'Operating Costs'
        unique_together = ['scale', 'week_range']
        ordering = ['scale', 'week_range']
    
    def save(self, *args, **kwargs):
        self.total = (
            self.feed_starter + self.feed_grower + self.feed_finisher +
            self.utilities + self.water + self.medication +
            self.labor + self.transport_misc
        )
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.scale.business.name} - {self.scale.get_scale_type_display()} - Week {self.week_range}"


# ============================================
# REVENUE PROJECTIONS
# ============================================

class RevenueProjection(models.Model):
    """Cycle-by-cycle revenue projections for a specific business scale"""
    
    scale = models.ForeignKey(
        BusinessScale,
        on_delete=models.CASCADE,
        related_name='revenue_projections',
        help_text="Business scale these projections apply to"
    )
    
    cycle_number = models.PositiveSmallIntegerField(
        help_text="Production cycle number (1, 2, 3, etc.)"
    )
    
    unit_sales = models.PositiveIntegerField(
        help_text="Number of units sold in this cycle"
    )
    
    price_per_unit = models.PositiveIntegerField(
        help_text="Price per unit in Dalasi"
    )
    
    total_revenue = models.PositiveIntegerField(
        editable=False,
        help_text="Unit Sales × Price per Unit (auto-calculated)"
    )
    
    cost_of_goods = models.PositiveIntegerField(
        help_text="Cost of goods sold for this cycle"
    )
    
    gross_profit = models.PositiveIntegerField(
        editable=False,
        help_text="Total Revenue - COGS (auto-calculated)"
    )
    
    operating_expenses = models.PositiveIntegerField(
        help_text="Fixed overheads for this cycle"
    )
    
    net_profit = models.PositiveIntegerField(
        editable=False,
        help_text="Gross Profit - Operating Expenses (auto-calculated)"
    )
    
    cumulative_cash_flow = models.IntegerField(
        editable=False,
        help_text="Running total of net profits (auto-calculated)"
    )
    
    class Meta:
        db_table = 'revenue_projections'
        verbose_name = 'Revenue Projection'
        verbose_name_plural = 'Revenue Projections'
        unique_together = ['scale', 'cycle_number']
        ordering = ['scale', 'cycle_number']
    
    def save(self, *args, **kwargs):
        self.total_revenue = self.unit_sales * self.price_per_unit
        self.gross_profit = self.total_revenue - self.cost_of_goods
        self.net_profit = self.gross_profit - self.operating_expenses
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.scale.business.name} - Cycle {self.cycle_number}"


# ============================================
# FINANCIAL METRICS
# ============================================

class FinancialMetric(models.Model):
    """Key financial metrics for a specific business scale"""
    
    scale = models.ForeignKey(
        BusinessScale,
        on_delete=models.CASCADE,
        related_name='financial_metrics',
        help_text="Business scale these metrics apply to"
    )
    
    breakeven_cycles = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        help_text="Number of cycles to break even"
    )
    
    gross_margin_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Gross margin percentage"
    )
    
    net_margin_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Net margin percentage"
    )
    
    roi_percent = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text="Return on Investment percentage"
    )
    
    payback_months = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        help_text="Payback period in months"
    )
    
    data_source = models.CharField(
        max_length=200,
        help_text="Source of this data (e.g., 'Field Survey 2024', 'GBoS 2024')"
    )
    
    last_updated = models.DateField(
        auto_now=True,
        help_text="Date when this data was last updated"
    )
    
    class Meta:
        db_table = 'financial_metrics'
        verbose_name = 'Financial Metric'
        verbose_name_plural = 'Financial Metrics'
        unique_together = ['scale', 'data_source']
    
    def __str__(self):
        return f"{self.scale.business.name} - {self.scale.get_scale_type_display()}"


# ============================================
# RISK ASSESSMENT
# ============================================

class Risk(models.Model):
    """Risk assessment for a specific business scale"""
    
    scale = models.ForeignKey(
        BusinessScale,
        on_delete=models.CASCADE,
        related_name='risks',
        help_text="Business scale these risks apply to"
    )
    
    category = models.CharField(
        max_length=50,
        choices=RiskCategory.choices,
        help_text="Risk category"
    )
    
    specific_risk = models.CharField(
        max_length=200,
        help_text="Description of the specific risk"
    )
    
    likelihood = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Likelihood (1=Very Low, 5=Very High)"
    )
    
    impact = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Impact (1=Very Low, 5=Very High)"
    )
    
    risk_score = models.PositiveSmallIntegerField(
        editable=False,
        help_text="Likelihood × Impact (auto-calculated)"
    )
    
    mitigation_strategy = models.TextField(
        help_text="How to mitigate this risk"
    )
    
    last_updated = models.DateField(
        auto_now=True,
        help_text="Date when this risk was last updated"
    )
    
    class Meta:
        db_table = 'risks'
        verbose_name = 'Risk'
        verbose_name_plural = 'Risks'
        ordering = ['scale', '-risk_score']
    
    def save(self, *args, **kwargs):
        self.risk_score = self.likelihood * self.impact
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.specific_risk} (Score: {self.risk_score})"


# ============================================
# FEASIBILITY FACTOR
# ============================================

class FeasibilityFactor(models.Model):
    """Individual feasibility factor with rating for a specific business scale"""
    
    scale = models.ForeignKey(
        BusinessScale,
        on_delete=models.CASCADE,
        related_name='feasibility_factors',
        help_text="Business scale these factors apply to"
    )
    
    category = models.CharField(
        max_length=50,
        choices=FeasibilityCategory.choices,
        help_text="Feasibility category"
    )
    
    sub_category = models.CharField(
        max_length=100,
        help_text="Specific factor (e.g., 'Market Size', 'Startup Capital')"
    )
    
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Rating out of 10 (1=Poor, 10=Excellent)"
    )
    
    notes = models.TextField(
        blank=True,
        help_text="Additional context about this rating"
    )
    
    data_source = models.CharField(
        max_length=200,
        help_text="Source of this data (e.g., 'GBoS 2024', 'Field Survey')"
    )
    
    last_updated = models.DateField(
        auto_now=True,
        help_text="Date when this factor was last updated"
    )
    
    class Meta:
        db_table = 'feasibility_factors'
        verbose_name = 'Feasibility Factor'
        verbose_name_plural = 'Feasibility Factors'
        unique_together = ['scale', 'category', 'sub_category']
        ordering = ['scale', 'category', 'sub_category']
    
    def __str__(self):
        return f"{self.sub_category}: {self.rating}/10"


# ============================================
# OPERATIONS CHECKLIST
# ============================================

class OperationsChecklist(models.Model):
    """Daily, weekly, monthly tasks for running the business"""
    
    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name='checklists',
        help_text="Business this checklist belongs to"
    )
    
    scale_type = models.CharField(
        max_length=20,
        choices=ScaleType.choices,
        help_text="Which scale this checklist applies to (or 'all')"
    )
    
    task_type = models.CharField(
        max_length=20,
        choices=[
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('monthly', 'Monthly'),
        ],
        help_text="Frequency of the task"
    )
    
    task_name = models.CharField(
        max_length=200,
        help_text="Name of the task"
    )
    
    description = models.TextField(
        blank=True,
        help_text="Detailed description of how to perform the task"
    )
    
    time_of_day = models.CharField(
        max_length=50,
        blank=True,
        help_text="For daily tasks: e.g., 'Morning', 'Midday', 'Evening'"
    )
    
    responsible = models.CharField(
        max_length=100,
        blank=True,
        help_text="Who typically performs this task"
    )
    
    duration_minutes = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="Estimated time to complete in minutes"
    )
    
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order"
    )
    
    class Meta:
        db_table = 'operations_checklists'
        verbose_name = 'Operations Checklist'
        verbose_name_plural = 'Operations Checklists'
        ordering = ['business', 'scale_type', 'task_type', 'order']
    
    def __str__(self):
        scale_display = "All" if self.scale_type == 'all' else self.get_scale_type_display()
        return f"{self.business.name} ({scale_display}) - {self.task_name}"
    

# ============================================
# BUSINESS PROFILE (for interviewed businesses)
# ============================================

class BusinessProfile(BaseModel):
    """
    Profile for businesses that have been interviewed, featured in content, 
    or listed as partners. Can optionally be linked to a User account.
    """
    
    # Basic Information
    name = models.CharField(
        max_length=200,
        help_text="Business name"
    )
    
    owner_name = models.CharField(
        max_length=200,
        blank=True,
        help_text="Owner or founder name"
    )
    
    owner_position = models.CharField(
        max_length=100,
        blank=True,
        help_text="Owner position (e.g., Founder, CEO, Managing Director)"
    )
    
    description = models.TextField(
        help_text="Business description"
    )
    
    short_description = models.CharField(
        max_length=200,
        blank=True,
        help_text="Short description for listings"
    )
    
    # Logo & Images
    logo = models.ImageField(
        upload_to='business-profiles/logos/',
        blank=True,
        null=True,
        help_text="Business logo"
    )
    
    cover_image = models.ImageField(
        upload_to='business-profiles/covers/',
        blank=True,
        null=True,
        help_text="Cover/banner image"
    )
    
    # Contact Information
    email = models.EmailField(
        blank=True,
        help_text="Business email"
    )
    
    phone = models.CharField(
        max_length=50,
        blank=True,
        help_text="Business phone number"
    )
    
    website = models.URLField(
        blank=True,
        help_text="Business website"
    )
    
    address = models.TextField(
        blank=True,
        help_text="Physical address"
    )
    
    location = models.CharField(
        max_length=200,
        blank=True,
        help_text="City/region (e.g., Banjul, Serrekunda)"
    )
    
    # Social Media
    facebook = models.URLField(
        blank=True,
        help_text="Facebook page URL"
    )
    
    instagram = models.URLField(
        blank=True,
        help_text="Instagram handle or URL"
    )
    
    linkedin = models.URLField(
        blank=True,
        help_text="LinkedIn company page URL"
    )
    
    twitter = models.URLField(
        blank=True,
        help_text="Twitter/X handle or URL"
    )
    
    tiktok = models.URLField(
        blank=True,
        help_text="TikTok handle or URL"
    )
    
    whatsapp = models.CharField(
        max_length=50,
        blank=True,
        help_text="WhatsApp number"
    )
    
    # Business Details
    founded_year = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="Year the business was founded"
    )
    
    employee_count = models.CharField(
        max_length=50,
        blank=True,
        help_text="Number of employees (e.g., '1-5', '10-50')"
    )
    
    business_type = models.CharField(
        max_length=100,
        blank=True,
        help_text="Business type (e.g., 'Sole Proprietorship', 'LLC')"
    )
    
    # Relationships
    sector = models.ForeignKey(
        Sector,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='business_profiles',
        help_text="Primary sector"
    )
    
    # Link to User account (optional - for future self-service)
    user = models.OneToOneField(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='business_profile',
        help_text="Linked user account (if business wants to manage their profile)"
    )
    
    # Categories
    is_partner = models.BooleanField(
        default=False,
        help_text="Is this a trusted partner/service provider"
    )
    
    is_featured = models.BooleanField(
        default=False,
        help_text="Display on homepage and featured sections"
    )
    
    is_verified = models.BooleanField(
        default=False,
        help_text="Has this business been verified by GBI team"
    )
    
    partner_type = models.CharField(
        max_length=50,
        blank=True,
        help_text="If partner: consultant, supplier, legal, etc."
    )
    
    # Interview metadata
    interview_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date when interview was conducted"
    )
    
    interviewed_by = models.CharField(
        max_length=100,
        default="Ebrima Barry",
        help_text="Name of interviewer"
    )
    
    interview_notes = models.TextField(
        blank=True,
        help_text="Internal notes about the interview"
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PUBLISHED,
        help_text="Publication status"
    )
    
    # Stats
    view_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of profile views"
    )
    
    class Meta:
        db_table = 'business_profiles'
        verbose_name = 'Business Profile'
        verbose_name_plural = 'Business Profiles'
        ordering = ['-is_featured', '-is_verified', 'name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_partner', 'is_verified']),
            models.Index(fields=['sector']),
            models.Index(fields=['location']),
        ]
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while BusinessProfile.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def increment_view_count(self):
        self.view_count += 1
        self.save(update_fields=['view_count'])
    
    @property
    def partner_type_display(self):
        """Display partner type in human readable format"""
        types = {
            'consultant': 'Business Consultant',
            'supplier': 'Equipment/Supplier',
            'legal': 'Legal Services',
            'financial': 'Financial Services',
            'marketing': 'Marketing Agency',
            'tech': 'Technology Provider',
            'training': 'Training Provider',
        }
        return types.get(self.partner_type, self.partner_type)
    

# ============================================
# BUSINESS PROFILE FEATURE MODEL
# ============================================

def business_profile_logo_path(instance, filename):
    """Generate path for business profile logos: business-profiles/logos/slug/filename.jpg"""
    ext = filename.split('.')[-1] if '.' in filename else 'jpg'
    return f"business-profiles/logos/{instance.slug}/{filename}"

def business_profile_cover_path(instance, filename):
    """Generate path for business profile covers: business-profiles/covers/slug/filename.jpg"""
    ext = filename.split('.')[-1] if '.' in filename else 'jpg'
    return f"business-profiles/covers/{instance.slug}/{filename}"

class BusinessProfileFeature(models.Model):
    """
    Features/testimonials from the business for display on their profile
    """
    
    business_profile = models.ForeignKey(
        BusinessProfile,
        on_delete=models.CASCADE,
        related_name='features',
        help_text="Business profile this feature belongs to"
    )
    logo = models.ImageField(
        upload_to=business_profile_logo_path,
        blank=True,
        null=True,
        help_text="Business logo"
    )
    
    cover_image = models.ImageField(
        upload_to=business_profile_cover_path,
        blank=True,
        null=True,
        help_text="Cover/banner image"
    )
    
    title = models.CharField(
        max_length=200,
        help_text="Feature title (e.g., '25% Revenue Growth')"
    )
    
    description = models.TextField(
        help_text="Feature description"
    )
    
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Icon name (e.g., 'TrendingUp', 'Users')"
    )
    
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'business_profile_features'
        verbose_name = 'Business Profile Feature'
        verbose_name_plural = 'Business Profile Features'
        ordering = ['order']
    
    def __str__(self):
        return f"{self.business_profile.name} - {self.title}"


# ============================================
# BUSINESS PROFILE TESTIMONIAL MODEL
# ============================================

class BusinessProfileTestimonial(models.Model):
    """
    Testimonial from the business owner about their experience with GBI
    """
    
    business_profile = models.ForeignKey(
        BusinessProfile,
        on_delete=models.CASCADE,
        related_name='testimonials',
        help_text="Business profile this testimonial belongs to"
    )
    
    quote = models.TextField(
        help_text="The testimonial quote"
    )
    
    author_name = models.CharField(
        max_length=100,
        help_text="Name of person giving testimonial"
    )
    
    author_position = models.CharField(
        max_length=100,
        blank=True,
        help_text="Position of author (e.g., 'Founder')"
    )
    
    is_featured = models.BooleanField(
        default=False,
        help_text="Display on homepage"
    )
    
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'business_profile_testimonials'
        verbose_name = 'Business Profile Testimonial'
        verbose_name_plural = 'Business Profile Testimonials'
        ordering = ['order']
    
    def __str__(self):
        return f"{self.business_profile.name} - {self.author_name}"