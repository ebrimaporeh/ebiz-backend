"""
apps/core/models.py

Foundation layer for all GAMBIH models.
"""

import uuid
import secrets
from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

from .constants import (
    Status, ScaleType, Priority, RiskCategory, FeasibilityCategory,
    Country as CountryChoice, Region as RegionChoice, 
    Currency, CURRENCY_SYMBOLS, COUNTRY_CURRENCY, COUNTRY_FLAGS,
    get_country_info, get_active_countries, REGION_COUNTRIES
)


# ============================================
# BASE MIXINS
# ============================================

class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteMixin(models.Model):
    is_deleted = models.BooleanField(default=False, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "deleted_at"])

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.save(update_fields=["is_deleted", "deleted_at"])

    class Meta:
        abstract = True


class SlugMixin(models.Model):
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def _generate_slug(self, source_field: str = "name") -> str:
        if self.slug:
            return self.slug
        base = slugify(getattr(self, source_field, "") or "")
        slug, n = base, 1
        qs = self.__class__.objects
        while qs.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base}-{n}"
            n += 1
        return slug

    class Meta:
        abstract = True


class BaseModel(TimeStampMixin, SoftDeleteMixin, SlugMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


# ============================================
# COUNTRY MODEL
# ============================================

class Country(models.Model):
    """
    Country entity for geographic scoping.
    This is a MODEL, not the enum from constants.
    """
    
    code = models.CharField(
        max_length=2,
        choices=CountryChoice.choices,
        unique=True,
        db_index=True,
        help_text="ISO country code"
    )
    name = models.CharField(max_length=100)
    flag_emoji = models.CharField(max_length=10, blank=True)
    currency = models.CharField(
        max_length=3,
        choices=Currency.choices,
        default=Currency.GMD
    )
    currency_symbol = models.CharField(max_length=5, blank=True)
    
    # Market data
    population = models.PositiveIntegerField(null=True, blank=True)
    gdp_per_capita_usd = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    
    # Display
    is_active = models.BooleanField(default=True, db_index=True)
    order = models.PositiveIntegerField(default=0)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "countries"
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        ordering = ["order", "name"]
    
    def __str__(self):
        return f"{self.flag_emoji} {self.name}"
    
    def save(self, *args, **kwargs):
        if not self.flag_emoji:
            self.flag_emoji = COUNTRY_FLAGS.get(self.code, "")
        if not self.currency:
            self.currency = COUNTRY_CURRENCY.get(self.code, Currency.GMD)
        if not self.currency_symbol:
            self.currency_symbol = CURRENCY_SYMBOLS.get(self.currency, "$")
        if not self.name:
            self.name = dict(CountryChoice.choices).get(self.code, self.code)
        super().save(*args, **kwargs)
    
    @property
    def display_name(self) -> str:
        return f"{self.flag_emoji} {self.name}"


# ============================================
# REGION MODEL
# ============================================

class Region(models.Model):
    """
    Regional grouping for cross-country analysis.
    """
    
    name = models.CharField(max_length=100, choices=RegionChoice.choices, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    countries = models.ManyToManyField(
        Country,  # ← This is the Country MODEL
        related_name='regions',
        blank=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "regions"
        verbose_name = "Region"
        verbose_name_plural = "Regions"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    @property
    def country_count(self) -> int:
        return self.countries.count()


# ============================================
# SOURCE REGISTRY
# ============================================

class Source(models.Model):
    """Central registry for every data source used on the platform."""

    class SourceType(models.TextChoices):
        GOVERNMENT = "government", "Government statistics"
        FIELD_SURVEY = "field_survey", "Field survey"
        INTERVIEW = "interview", "Operator interview"
        INDUSTRY = "industry", "Industry report"
        ACADEMIC = "academic", "Academic research"
        INTERNAL = "internal", "GAMBIH research"
        PROJECTION = "projection", "Projection / forecast"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    reference = models.CharField(max_length=300, blank=True)
    url = models.URLField(blank=True)
    publication_date = models.DateField(null=True, blank=True)
    year = models.IntegerField(db_index=True)
    source_type = models.CharField(max_length=30, choices=SourceType.choices, default=SourceType.INTERNAL)
    confidence_rating = models.DecimalField(
        max_digits=3, decimal_places=1, default=7.0,
        validators=[MinValueValidator(1.0), MaxValueValidator(10.0)]
    )
    is_primary_source = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "sources"
        verbose_name = "Source"
        verbose_name_plural = "Sources"
        ordering = ["-year", "-confidence_rating", "name"]

    def __str__(self):
        year_str = f" ({self.year})" if self.year else ""
        if self.reference:
            return f"{self.name}{year_str} – {self.reference}"
        return f"{self.name}{year_str}"


# ============================================
# RATING VALUE
# ============================================

class RatingValue(models.Model):
    """A 1–10 rating with source attribution."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    value = models.DecimalField(
        max_digits=3, decimal_places=1,
        validators=[MinValueValidator(1.0), MaxValueValidator(10.0)]
    )
    year = models.IntegerField(db_index=True)
    source = models.ForeignKey(Source, on_delete=models.PROTECT, related_name="ratings")
    confidence_score = models.DecimalField(
        max_digits=3, decimal_places=1, default=7.0,
        validators=[MinValueValidator(1.0), MaxValueValidator(10.0)]
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ratings"
        verbose_name = "Rating value"
        verbose_name_plural = "Rating values"

    def __str__(self):
        return f"{self.value}/10 ({self.year})"

    @property
    def normalized_100(self) -> int:
        return int(float(self.value) * 10)


# ============================================
# API KEY MODEL
# ============================================

class APIKey(models.Model):
    """API key for programmatic access to GAMBIH data."""

    class Tier(models.TextChoices):
        FREE = "free", "Free (rate limited)"
        PREMIUM = "premium", "Premium"
        PRO = "pro", "Pro"
        ENTERPRISE = "enterprise", "Enterprise (unlimited)"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.CharField(max_length=200)
    key = models.CharField(max_length=64, unique=True, db_index=True, editable=False)
    tier = models.CharField(max_length=20, choices=Tier.choices, default=Tier.FREE)
    rate_limit_per_minute = models.IntegerField(default=60)
    is_active = models.BooleanField(default=True, db_index=True)
    last_used = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    contact_name = models.CharField(max_length=200, blank=True)
    contact_email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "api_keys"
        verbose_name = "API Key"
        verbose_name_plural = "API Keys"

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = f"gb_{secrets.token_urlsafe(32)}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.organization} ({self.tier})"