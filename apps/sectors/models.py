"""
apps/sectors/models.py

Sector taxonomy for GAMBIH with country/region support for West African expansion.

A Sector is the top-level grouping (Agriculture, Transportation, Technology…).
It has no financial data of its own — that lives on Business and BusinessScale.

Design notes
------------
- UUID PK throughout for API safety and future distribution.
- `business_count` is a denormalised cache; update it via a post_save /
  post_delete signal on Business (see signals.py).
- `parent` enables two-level sector trees (e.g. Agriculture → Poultry).
- Country/Region from core constants for geographic expansion.
- `tags` (via SectorTag) supports flexible cross-cutting labels.
"""

import uuid
from django.db import models
from django.utils.text import slugify

from apps.core.models import BaseModel, Status
from apps.core.constants import (
    Country as CountryChoice, 
    Region as RegionChoice, 
    Currency, 
    CURRENCY_SYMBOLS, 
    COUNTRY_FLAGS
)


# ============================================================
# IMAGE UPLOAD PATH
# ============================================================

def sector_image_path(instance, filename: str) -> str:
    """Storage path: sectors/<country_code>/<slug>/<timestamp>.<ext>"""
    from django.utils import timezone
    ext = filename.rsplit(".", 1)[-1] if "." in filename else "jpg"
    ts = timezone.now().strftime("%Y%m%d%H%M%S")
    country_code = getattr(instance, 'country', 'gm')
    return f"sectors/{country_code}/{instance.slug}/{ts}.{ext}"


# ============================================================
# SECTOR
# ============================================================

class Sector(BaseModel):
    """
    Business sector / category with country/region support.

    Examples: Agriculture, Transportation, Retail, Technology, Tourism.

    A sector can have one optional parent to support sub-sector trees:
        Agriculture
        └─ Poultry Farming
        └─ Crop Production

    Country/Region enables expansion across West Africa:
        - Filter by country: Senegal, Nigeria, Ghana, etc.
        - Filter by region: West Africa, ECOWAS, Coastal, Sahelian
    """

    name = models.CharField(
        max_length=100,
        help_text="Sector name, e.g. 'Agriculture', 'Transportation'",
    )
    description = models.TextField(
        blank=True,
        help_text="What this sector covers and why it matters in the local context",
    )

    # Geographic scope (using constants from core)
    country = models.CharField(
        max_length=2,
        choices=CountryChoice.choices,
        default=CountryChoice.GAMBIA,
        db_index=True,
        help_text="Country this sector data applies to",
    )
    region = models.CharField(
        max_length=30,
        choices=RegionChoice.choices,
        blank=True,
        null=True,
        db_index=True,
        help_text="Regional grouping for cross-country analysis",
    )
    currency = models.CharField(
        max_length=3,
        choices=Currency.choices,
        default=Currency.GMD,
        help_text="Default currency for this sector/country",
    )

    # Visual identity
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Lucide React icon name, e.g. 'Truck', 'Leaf', 'ShoppingBag'",
    )
    color = models.CharField(
        max_length=20,
        blank=True,
        help_text="Tailwind colour token or hex, e.g. 'green', '#1D9E75'",
    )
    featured_image = models.ImageField(
        upload_to=sector_image_path,
        blank=True,
        null=True,
    )

    # Taxonomy
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
        help_text="Optional parent sector for two-level taxonomy",
    )

    # Display
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order on listing pages (lower = earlier)",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PUBLISHED,
        db_index=True,
    )

    # Denormalised counters
    business_count = models.PositiveIntegerField(
        default=0,
        help_text="Cached count of published businesses in this sector",
    )

    # Market size (denormalised for quick display)
    estimated_market_size = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Estimated market size in local currency",
    )
    estimated_market_size_display = models.CharField(
        max_length=50,
        blank=True,
        help_text="Formatted market size (e.g., 'D2.4B')",
    )

    # AI / search enrichment
    summary_for_ai = models.TextField(
        blank=True,
        help_text=(
            "Plain-language sector overview written for LLM context injection. "
            "Keep to 2–3 sentences. Updated manually when major changes occur."
        ),
    )

    class Meta:
        db_table = "sectors"
        verbose_name = "Sector"
        verbose_name_plural = "Sectors"
        ordering = ["country", "order", "name"]
        unique_together = ["name", "country"]  # Same sector name can exist in different countries
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["status"]),
            models.Index(fields=["order"]),
            models.Index(fields=["parent"]),
            models.Index(fields=["country", "status"]),
            models.Index(fields=["region", "status"]),
            models.Index(fields=["country", "parent"]),
        ]

    def __str__(self):
        country_display = self.get_country_display()
        if self.country != CountryChoice.GAMBIA:
            return f"{self.name} ({country_display})"
        return self.name

    def save(self, *args, **kwargs):
        # Generate unique slug with country prefix to avoid collisions
        if not self.slug:
            base = slugify(f"{self.name}-{self.country}")
            self.slug = base
            counter = 1
            while Sector.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{base}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    @property
    def is_top_level(self) -> bool:
        return self.parent_id is None

    @property
    def full_name(self) -> str:
        """'Agriculture › Poultry Farming' for sub-sectors with country."""
        name = self.name
        if self.parent_id:
            name = f"{self.parent.name} › {self.name}"
        if self.country != CountryChoice.GAMBIA:
            name = f"{name} ({self.get_country_display()})"
        return name

    @property
    def flag_emoji(self) -> str:
        """Get flag emoji for this sector's country."""
        return COUNTRY_FLAGS.get(self.country, "")

    @property
    def currency_symbol(self) -> str:
        """Get currency symbol for display."""
        return CURRENCY_SYMBOLS.get(self.currency, "D")

    @property
    def country_display_with_flag(self) -> str:
        """Get country name with flag emoji."""
        flag = self.flag_emoji
        country_name = self.get_country_display()
        return f"{flag} {country_name}"


# ============================================================
# SECTOR TAG
# ============================================================

class SectorTag(models.Model):
    """
    Flexible cross-cutting labels attached to sectors.

    Examples: "high-growth", "diaspora-favourite", "low-capital-entry",
    "export-potential", "climate-sensitive".

    These drive frontend filtering chips and future AI recommendation.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    label = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(max_length=60, unique=True)
    description = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "sector_tags"
        verbose_name = "Sector tag"
        verbose_name_plural = "Sector tags"
        ordering = ["label"]

    def __str__(self):
        return self.label

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.label)
        super().save(*args, **kwargs)


class SectorTagAssignment(models.Model):
    """Join table: Sector ↔ SectorTag (many-to-many with metadata)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name="tag_assignments")
    tag = models.ForeignKey(SectorTag, on_delete=models.CASCADE, related_name="sector_assignments")
    added_at = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )

    class Meta:
        db_table = "sector_tag_assignments"
        unique_together = ["sector", "tag"]
        verbose_name = "Sector tag assignment"
        verbose_name_plural = "Sector tag assignments"

    def __str__(self):
        return f"{self.sector.name} → {self.tag.label}"


# ============================================================
# SECTOR STAT (with country/region support)
# ============================================================

class SectorStat(models.Model):
    """
    Macro-level market statistics for a sector, each sourced and dated.
    Supports country and region filtering for cross-border analysis.
    """

    class UnitChoices(models.TextChoices):
        DALASI = "D", "Dalasi (GMD)"
        CFA = "XOF", "CFA Franc"
        CEDI = "GHS", "Ghana Cedi"
        NAIRA = "NGN", "Naira"
        USD = "USD", "US Dollar"
        PERCENT = "%", "Percentage"
        NUMBER = "number", "Number"
        YEARS = "years", "Years"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name="stats")

    label = models.CharField(
        max_length=100,
        help_text="Human-readable stat name, e.g. 'Estimated market size'",
    )
    value = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        help_text="Numeric value (use negative for decreases)",
    )
    unit = models.CharField(
        max_length=20,
        choices=UnitChoices.choices,
        default=UnitChoices.DALASI,
    )
    display_order = models.PositiveSmallIntegerField(
        default=0,
        help_text="Order in which this stat appears on the sector page",
    )
    is_headline = models.BooleanField(
        default=False,
        help_text="Show prominently at the top of the sector card",
    )
    
    # Geographic scope for this stat (can be null = same as sector)
    country = models.CharField(
        max_length=2,
        choices=CountryChoice.choices,
        null=True,
        blank=True,
        db_index=True,
        help_text="Country this stat applies to (null = same as sector)",
    )
    region = models.CharField(
        max_length=30,
        choices=RegionChoice.choices,
        null=True,
        blank=True,
        db_index=True,
        help_text="Region this stat applies to",
    )
    
    # Source attribution (using core Source model)
    source = models.ForeignKey(
        "core.Source",
        on_delete=models.PROTECT,
        related_name="sector_stats",
    )
    year = models.IntegerField(db_index=True, help_text="Year this stat applies to")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "sector_stats"
        verbose_name = "Sector stat"
        verbose_name_plural = "Sector stats"
        ordering = ["sector", "display_order"]
        indexes = [
            models.Index(fields=["sector", "year"]),
            models.Index(fields=["country", "year"]),
            models.Index(fields=["region", "year"]),
        ]

    def __str__(self):
        location = ""
        if self.country:
            location = f" ({self.get_country_display()})"
        elif self.region:
            location = f" ({self.get_region_display()})"
        return f"{self.sector.name}{location} — {self.label}"

    def get_country_display(self):
        """Get country display name from constants."""
        if self.country:
            return dict(CountryChoice.choices).get(self.country, self.country)
        return None

    def get_region_display(self):
        """Get region display name from constants."""
        if self.region:
            return dict(RegionChoice.choices).get(self.region, self.region)
        return None

    @property
    def display_value(self) -> str:
        """Format for frontend display."""
        if self.unit == "D":
            return f"D{self.value:,.0f}"
        elif self.unit == "XOF":
            return f"CFA{self.value:,.0f}"
        elif self.unit == "GHS":
            return f"₵{self.value:,.0f}"
        elif self.unit == "NGN":
            return f"₦{self.value:,.0f}"
        elif self.unit == "USD":
            return f"${self.value:,.0f}"
        elif self.unit == "%":
            return f"{self.value}%"
        return f"{self.value:,.0f}"