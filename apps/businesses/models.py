"""
apps/businesses/models.py

The intelligence core of GAMBIH.

Model hierarchy
---------------
Business                    ← one canonical entity (e.g. "Poultry Farming – Broilers")
└─ BusinessScale            ← three operational tiers: small / medium / large (WITH YEAR)
   ├─ CapitalItem           ← itemised startup costs (WITH YEAR)
   ├─ OperatingCost         ← periodic running costs (WITH YEAR, choice-based categories)
   ├─ RevenueProjection     ← cycle-by-cycle revenue model (WITH YEAR, auto cumulative)
   ├─ FinancialMetric       ← summary KPIs (WITH YEAR)
   ├─ Risk                  ← risk register entry (WITH YEAR)
   └─ FeasibilityFactor     ← rated factor (WITH YEAR)

Supporting entities
-------------------
IntelligenceSnapshot       ← DENORMALIZED - single document for frontend/API (FAST)
TimeSeriesMetric           ← time-series tracking for trends
BusinessProfile            ← interviewed / featured real businesses
OperationsChecklist        ← daily / weekly / monthly task lists

Relationship path:
    Business ← BusinessScale ← (CapitalItem | OperatingCost | RevenueProjection | 
                                 FinancialMetric | Risk | FeasibilityFactor)
    
All metrics can be traced back to their Business via scale.business.

Design decisions (updated)
--------------------------
1. EVERY intelligence model has a `year` field for time-series support.
2. NumericValue is GONE. Direct fields with source FK where needed.
3. OperatingCost.category uses choices, not free text.
4. RevenueProjection.cumulative_cash_flow is auto-calculated.
5. period_label is a property (derived, not stored).
6. IntelligenceSnapshot is the PRIMARY read model for frontend/API.
7. TimeSeriesMetric enables fast year-over-year queries.
8. Reporting models moved to apps/reporting (not here).
"""

import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from django.utils import timezone
from django.db.models import F, Avg, Sum

from apps.core.models import (
    BaseModel, Status, ScaleType, Priority, RiskCategory, FeasibilityCategory,
    Source, APIKey
)
from apps.sectors.models import Sector


# ============================================================
# IMAGE UPLOAD PATHS
# ============================================================

def business_image_path(instance, filename: str) -> str:
    ext = filename.rsplit(".", 1)[-1] if "." in filename else "jpg"
    return f"businesses/{instance.slug}/{timezone.now().strftime('%Y%m%d%H%M%S')}.{ext}"


def profile_logo_path(instance, filename: str) -> str:
    ext = filename.rsplit(".", 1)[-1] if "." in filename else "jpg"
    return f"business-profiles/logos/{instance.slug}/{timezone.now().strftime('%Y%m%d%H%M%S')}.{ext}"


def profile_cover_path(instance, filename: str) -> str:
    ext = filename.rsplit(".", 1)[-1] if "." in filename else "jpg"
    return f"business-profiles/covers/{instance.slug}/{timezone.now().strftime('%Y%m%d%H%M%S')}.{ext}"


# ============================================================
# BUSINESS
# ============================================================

class Business(BaseModel):
    """
    Canonical business entity — the top-level intelligence object.

    A Business represents a *type* of business (e.g. "Poultry Farming –
    Broilers"), not a specific real company.  Real companies go in
    BusinessProfile.

    All metrics (costs, revenues, risks, feasibility) flow through
    BusinessScale children, which link back to this Business.
    """

    sector = models.ForeignKey(
        Sector,
        on_delete=models.CASCADE,
        related_name="businesses",
    )
    name = models.CharField(
        max_length=200,
        help_text="e.g. 'Poultry Farming – Broilers', 'Solar Panel Installation'",
    )
    short_description = models.CharField(
        max_length=200,
        blank=True,
        help_text="One-line tagline for cards and listings",
    )
    overview = models.TextField(
        help_text="2–3 paragraphs explaining what this business does day-to-day",
    )
    opportunity_thesis = models.TextField(
        help_text="Why this business makes sense in The Gambia today",
    )
    featured_image = models.ImageField(
        upload_to=business_image_path,
        blank=True,
        null=True,
    )
    has_scales = models.BooleanField(
        default=True,
        help_text="Does this business have small/medium/large variants?",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        db_index=True,
    )
    is_featured = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Pin to homepage and featured sections",
    )
    view_count = models.PositiveIntegerField(
        default=0,
        help_text="Lifetime page views (incremented via increment_view_count())",
    )

    # AI / search support
    summary_for_ai = models.TextField(
        blank=True,
        help_text="Short plain-language summary injected into LLM context. Target: < 200 words.",
    )

    class Meta:
        db_table = "businesses"
        verbose_name = "Business"
        verbose_name_plural = "Businesses"
        ordering = ["-is_featured", "name"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["sector", "status"]),
            models.Index(fields=["is_featured"]),
            models.Index(fields=["status"]),
            models.Index(fields=["has_scales"]),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = self._generate_slug("name")
        super().save(*args, **kwargs)

    def increment_view_count(self):
        self.view_count = F("view_count") + 1
        self.save(update_fields=["view_count"])

    @property
    def all_scales(self):
        """Return all scales for this business, ordered by year desc, then scale_type."""
        return self.scales.all().order_by("-year", "scale_type")

    @property
    def latest_snapshot(self):
        """Return the most recent published snapshot for this business."""
        return self.snapshots.filter(status="published", is_latest=True).order_by("-year").first()


# ============================================================
# BUSINESS SCALE (WITH YEAR)
# ============================================================

class BusinessScale(models.Model):
    """
    Operational tier for a business: small, medium, or large.

    Each scale has its own capital requirements, cost structures, revenue
    projections, risk profile, and feasibility rating — allowing users to
    compare investment sizes side-by-side.

    `year` enables time-series analysis and annual updates.

    Relationship path to Business:
        scale.business → returns the parent Business
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name="scales",
    )
    scale_type = models.CharField(
        max_length=20,
        choices=ScaleType.choices,
        db_index=True,
    )
    year = models.IntegerField(
        db_index=True,
        default=2024,
        help_text="Year this scale data applies to",
    )

    # Scale definition
    capacity_definition = models.CharField(
        max_length=200,
        help_text="e.g. '100–300 birds', '1–3 vehicles', '50–100 students'",
    )
    target_market = models.TextField(
        help_text="Who buys from this scale — local households, restaurants, exporters, etc.",
    )
    location_type = models.CharField(
        max_length=100,
        help_text="e.g. 'backyard', 'peri-urban commercial', 'high-street retail'",
    )
    labor_needed = models.CharField(
        max_length=100,
        help_text="e.g. '1 part-time owner', '3 employees + 1 supervisor'",
    )

    # Aggregate feasibility (recomputed from FeasibilityFactor children)
    overall_feasibility_score = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
        help_text="Aggregate feasibility score 1.0–10.0, derived from FeasibilityFactor rows",
    )

    # Source for this scale's overall data
    primary_source = models.ForeignKey(
        Source,
        on_delete=models.PROTECT,
        related_name="business_scales",
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "business_scales"
        verbose_name = "Business scale"
        verbose_name_plural = "Business scales"
        unique_together = ["business", "scale_type", "year"]
        ordering = ["business", "scale_type", "-year"]
        indexes = [
            models.Index(fields=["business", "year", "scale_type"]),
            models.Index(fields=["year", "scale_type"]),
        ]

    def __str__(self):
        return f"{self.business.name} — {self.get_scale_type_display()} ({self.year})"

    def update_feasibility_score(self):
        """Recompute overall_feasibility_score as the mean of all FeasibilityFactor ratings."""
        result = self.feasibility_factors.aggregate(avg=Avg("rating"))
        self.overall_feasibility_score = result["avg"]
        self.save(update_fields=["overall_feasibility_score"])

    @property
    def total_startup_cost(self):
        """Calculate total startup cost from all capital items."""
        return self.capital_items.aggregate(total=Sum("total_cost"))["total"] or 0


# ============================================================
# CAPITAL ITEMS (WITH YEAR - NO NumericValue)
# ============================================================

class CapitalItem(models.Model):
    """
    Itemised startup cost for a specific business scale and year.

    Relationship path to Business:
        capital_item.scale.business → returns the parent Business
    """

    class Category(models.TextChoices):
        REGISTRATION = "registration", "Registration & legal"
        PREMISES = "premises", "Premises & housing"
        EQUIPMENT = "equipment", "Equipment & tools"
        INVENTORY = "inventory", "Initial inventory"
        WORKING_CAP = "working_cap", "Working capital"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    scale = models.ForeignKey(BusinessScale, on_delete=models.CASCADE, related_name="capital_items")

    category = models.CharField(max_length=30, choices=Category.choices)
    item_name = models.CharField(
        max_length=200,
        help_text="e.g. 'Day-old chicks', 'Poultry house', 'Generator'",
    )
    quantity = models.PositiveIntegerField(default=1)
    unit_cost = models.PositiveIntegerField(help_text="Cost per unit in Dalasi")
    total_cost = models.PositiveIntegerField(
        editable=False,
        help_text="quantity × unit_cost (auto-calculated)",
    )
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.ESSENTIAL)
    notes = models.TextField(blank=True, help_text="Where to buy, typical suppliers, etc.")

    source = models.ForeignKey(
        Source,
        on_delete=models.PROTECT,
        related_name="capital_items",
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "capital_items"
        verbose_name = "Capital item"
        verbose_name_plural = "Capital items"
        ordering = ["scale", "category", "priority", "item_name"]
        indexes = [
            models.Index(fields=["scale", "category"]),
        ]

    def __str__(self):
        return f"{self.item_name} — D{self.total_cost:,}"

    def save(self, *args, **kwargs):
        self.total_cost = self.quantity * self.unit_cost
        super().save(*args, **kwargs)


# ============================================================
# OPERATING COSTS (WITH YEAR, CHOICE-BASED CATEGORIES)
# ============================================================

class OperatingCostCategory(models.TextChoices):
    # Agriculture-specific
    FEED_STARTER = "feed_starter", "Feed - Starter"
    FEED_GROWER = "feed_grower", "Feed - Grower"
    FEED_FINISHER = "feed_finisher", "Feed - Finisher"
    MEDICATION = "medication", "Medication / Vaccines"
    LITTER = "litter", "Bedding / Litter"
    
    # General operations
    LABOR = "labor", "Labor / Wages"
    UTILITIES = "utilities", "Utilities (Elec/Water)"
    RENT = "rent", "Rent / Lease"
    FUEL = "fuel", "Fuel / Transport"
    MAINTENANCE = "maintenance", "Maintenance / Repairs"
    INSURANCE = "insurance", "Insurance"
    MARKETING = "marketing", "Marketing / Advertising"
    LICENSING = "licensing", "Licensing / Permits"
    
    # Retail/Service
    COST_OF_GOODS = "cogs", "Cost of goods sold"
    RESTOCKING = "restocking", "Restocking / Inventory"
    
    # Other
    OTHER = "other", "Other"


class OperatingCost(models.Model):
    """
    Generic periodic operating cost entry for a business scale and year.

    Uses choice-based categories for clean data and easy aggregation.

    Relationship path to Business:
        operating_cost.scale.business → returns the parent Business
    """

    class PeriodType(models.TextChoices):
        CYCLE = "cycle", "Production cycle"
        MONTH = "month", "Month"
        QUARTER = "quarter", "Quarter"
        YEAR = "year", "Year"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    scale = models.ForeignKey(BusinessScale, on_delete=models.CASCADE, related_name="operating_costs")

    period_number = models.PositiveSmallIntegerField(help_text="Sequence: 1, 2, 3…")
    period_type = models.CharField(max_length=20, choices=PeriodType.choices, default=PeriodType.CYCLE)
    cost_category = models.CharField(
        max_length=30,
        choices=OperatingCostCategory.choices,
        db_index=True,
    )
    amount_dalasi = models.PositiveIntegerField(help_text="Cost in Dalasi for this period")
    notes = models.TextField(blank=True)

    source = models.ForeignKey(
        Source,
        on_delete=models.PROTECT,
        related_name="operating_costs",
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "operating_costs"
        verbose_name = "Operating cost"
        verbose_name_plural = "Operating costs"
        ordering = ["scale", "period_number", "cost_category"]
        unique_together = ["scale", "period_number", "period_type", "cost_category"]
        indexes = [
            models.Index(fields=["scale", "period_number", "period_type"]),
            models.Index(fields=["cost_category"]),
        ]

    def __str__(self):
        return f"{self.scale} — {self.period_label} / {self.get_cost_category_display()} — D{self.amount_dalasi:,}"

    @property
    def period_label(self) -> str:
        """Derived period label - not stored."""
        if self.period_type == "cycle":
            return f"Cycle {self.period_number}"
        elif self.period_type == "month":
            return f"Month {self.period_number}"
        elif self.period_type == "quarter":
            return f"Quarter {self.period_number}"
        return f"Period {self.period_number}"


# ============================================================
# REVENUE PROJECTIONS (WITH YEAR, AUTO CUMULATIVE)
# ============================================================

class RevenueProjection(models.Model):
    """
    Period-by-period revenue model for a business scale and year.

    cumulative_cash_flow is auto-calculated when saving.

    Relationship path to Business:
        revenue_projection.scale.business → returns the parent Business
    """

    class PeriodType(models.TextChoices):
        CYCLE = "cycle", "Production cycle"
        MONTH = "month", "Month"
        QUARTER = "quarter", "Quarter"
        YEAR = "year", "Year"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    scale = models.ForeignKey(BusinessScale, on_delete=models.CASCADE, related_name="revenue_projections")

    period_number = models.PositiveSmallIntegerField(help_text="Sequence: 1, 2, 3…")
    period_type = models.CharField(max_length=20, choices=PeriodType.choices, default=PeriodType.CYCLE)

    unit_sales = models.PositiveIntegerField(help_text="Units / birds / jobs sold this period")
    price_per_unit = models.PositiveIntegerField(help_text="Average selling price per unit in Dalasi")

    total_revenue = models.PositiveIntegerField(
        editable=False,
        help_text="unit_sales × price_per_unit (auto-calculated)",
    )

    cost_of_goods = models.PositiveIntegerField(help_text="Direct COGS for this period in Dalasi")

    gross_profit = models.IntegerField(
        editable=False,
        help_text="total_revenue − cost_of_goods (auto-calculated)",
    )

    operating_expenses = models.PositiveIntegerField(help_text="Fixed overheads allocated to this period")

    net_profit = models.IntegerField(
        editable=False,
        help_text="gross_profit − operating_expenses (auto-calculated)",
    )

    cumulative_cash_flow = models.IntegerField(
        default=0,
        help_text="Running total of net profits (auto-calculated on save)",
    )

    source = models.ForeignKey(
        Source,
        on_delete=models.PROTECT,
        related_name="revenue_projections",
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "revenue_projections"
        verbose_name = "Revenue projection"
        verbose_name_plural = "Revenue projections"
        unique_together = ["scale", "period_number", "period_type"]
        ordering = ["scale", "period_number"]
        indexes = [
            models.Index(fields=["scale", "period_number", "period_type"]),
        ]

    def __str__(self):
        return f"{self.scale} — {self.period_label}"

    def save(self, *args, **kwargs):
        # Calculate basic financials
        self.total_revenue = self.unit_sales * self.price_per_unit
        self.gross_profit = self.total_revenue - self.cost_of_goods
        self.net_profit = self.gross_profit - self.operating_expenses
        
        # Save first to get an ID if needed
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # Recalculate cumulative cash flow for ALL periods in this scale
        if not is_new or self.pk:
            self._update_cumulative_for_scale()

    def _update_cumulative_for_scale(self):
        """Recalculate cumulative cash flow for all periods of this scale."""
        projections = RevenueProjection.objects.filter(
            scale=self.scale,
            period_type=self.period_type
        ).order_by("period_number")
        
        cumulative = 0
        for proj in projections:
            cumulative += proj.net_profit
            if proj.cumulative_cash_flow != cumulative:
                proj.cumulative_cash_flow = cumulative
                proj.save(update_fields=["cumulative_cash_flow"])

    @property
    def period_label(self) -> str:
        """Derived period label - not stored."""
        if self.period_type == "cycle":
            return f"Cycle {self.period_number}"
        elif self.period_type == "month":
            return f"Month {self.period_number}"
        elif self.period_type == "quarter":
            return f"Quarter {self.period_number}"
        return f"Period {self.period_number}"


# ============================================================
# FINANCIAL METRICS (WITH YEAR)
# ============================================================

class FinancialMetric(models.Model):
    """
    Summary KPIs for a business scale, year, and source.

    Relationship path to Business:
        financial_metric.scale.business → returns the parent Business
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    scale = models.ForeignKey(BusinessScale, on_delete=models.CASCADE, related_name="financial_metrics")

    breakeven_cycles = models.DecimalField(max_digits=4, decimal_places=1, help_text="Cycles to break even")
    gross_margin_pct = models.DecimalField(max_digits=5, decimal_places=2, help_text="Gross margin %")
    net_margin_pct = models.DecimalField(max_digits=5, decimal_places=2, help_text="Net margin %")
    roi_pct = models.DecimalField(max_digits=6, decimal_places=2, help_text="Return on investment %")
    payback_months = models.DecimalField(max_digits=4, decimal_places=1, help_text="Payback period in months")

    is_primary = models.BooleanField(
        default=True,
        help_text="Mark the canonical / most-current metric row for this scale",
    )

    source = models.ForeignKey(
        Source,
        on_delete=models.PROTECT,
        related_name="financial_metrics",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "financial_metrics"
        verbose_name = "Financial metric"
        verbose_name_plural = "Financial metrics"
        ordering = ["scale", "-is_primary", "-created_at"]
        indexes = [
            models.Index(fields=["scale", "is_primary"]),
        ]

    def __str__(self):
        return f"{self.scale} — ROI {self.roi_pct}%"


# ============================================================
# RISK REGISTER (WITH YEAR)
# ============================================================

class Risk(models.Model):
    """
    Individual risk entry for a business scale and year.

    Relationship path to Business:
        risk.scale.business → returns the parent Business
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    scale = models.ForeignKey(BusinessScale, on_delete=models.CASCADE, related_name="risks")

    category = models.CharField(max_length=30, choices=RiskCategory.choices)
    specific_risk = models.CharField(max_length=200, help_text="What exactly could go wrong")

    likelihood = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="1 = very unlikely, 10 = near-certain",
    )
    impact = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="1 = negligible impact, 10 = business-ending",
    )
    risk_score = models.PositiveSmallIntegerField(
        editable=False,
        help_text="likelihood × impact (auto-calculated, max 100)",
    )

    mitigation_strategy = models.TextField(help_text="Concrete steps to reduce this risk")

    source = models.ForeignKey(
        Source,
        on_delete=models.PROTECT,
        related_name="risks",
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "risks"
        verbose_name = "Risk"
        verbose_name_plural = "Risks"
        ordering = ["scale", "-risk_score"]
        indexes = [
            models.Index(fields=["scale", "risk_score"]),
        ]

    def __str__(self):
        return f"{self.specific_risk} (score {self.risk_score})"

    def save(self, *args, **kwargs):
        self.risk_score = self.likelihood * self.impact
        super().save(*args, **kwargs)

    @property
    def severity_label(self) -> str:
        if self.risk_score <= 33:
            return "Low"
        if self.risk_score <= 66:
            return "Medium"
        return "High"


# ============================================================
# FEASIBILITY FACTORS (WITH YEAR)
# ============================================================

class FeasibilityFactor(models.Model):
    """
    Individual rated factor contributing to the overall feasibility score.

    Relationship path to Business:
        feasibility_factor.scale.business → returns the parent Business
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    scale = models.ForeignKey(BusinessScale, on_delete=models.CASCADE, related_name="feasibility_factors")

    category = models.CharField(max_length=30, choices=FeasibilityCategory.choices)
    sub_category = models.CharField(
        max_length=100,
        help_text="e.g. 'Market size', 'Capital accessibility', 'Skilled labor availability'",
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="1 = very poor, 10 = excellent",
    )
    notes = models.TextField(blank=True, help_text="Context / evidence for this rating")

    source = models.ForeignKey(
        Source,
        on_delete=models.PROTECT,
        related_name="feasibility_factors",
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "feasibility_factors"
        verbose_name = "Feasibility factor"
        verbose_name_plural = "Feasibility factors"
        unique_together = ["scale", "category", "sub_category"]
        ordering = ["scale", "category", "sub_category"]

    def __str__(self):
        return f"{self.sub_category}: {self.rating}/10"


# ============================================================
# TIME SERIES METRIC (for year-over-year trends)
# ============================================================

class TimeSeriesMetric(models.Model):
    """
    Track metrics across years for fast trend analysis.
    Populated by ETL from IntelligenceSnapshot.

    Relationship path to Business:
        time_series_metric.business → direct to Business (denormalized for speed)
    """

    class MetricName(models.TextChoices):
        STARTUP_COST = "startup_cost", "Startup Cost"
        GROSS_MARGIN = "gross_margin", "Gross Margin %"
        NET_MARGIN = "net_margin", "Net Margin %"
        PAYBACK_MONTHS = "payback_months", "Payback Period (months)"
        ROI = "roi", "ROI %"
        FEASIBILITY = "feasibility", "Feasibility Score"
        RISK = "risk", "Risk Score"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="time_series")
    scale_type = models.CharField(max_length=20, choices=ScaleType.choices, null=True, blank=True, db_index=True)
    metric_name = models.CharField(max_length=30, choices=MetricName.choices, db_index=True)
    year = models.IntegerField(db_index=True)
    value_numeric = models.DecimalField(max_digits=20, decimal_places=2)
    source = models.ForeignKey(Source, on_delete=models.PROTECT, related_name="time_series")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "time_series_metrics"
        verbose_name = "Time series metric"
        verbose_name_plural = "Time series metrics"
        unique_together = ["business", "scale_type", "metric_name", "year"]
        indexes = [
            models.Index(fields=["business", "metric_name", "year"]),
            models.Index(fields=["year", "scale_type", "metric_name"]),
        ]

    def __str__(self):
        scale_part = f" ({self.scale_type})" if self.scale_type else ""
        return f"{self.business.name}{scale_part} - {self.get_metric_name_display()} {self.year}: {self.value_numeric}"


# ============================================================
# INTELLIGENCE SNAPSHOT (DENORMALIZED - PRIMARY READ MODEL)
# ============================================================

class IntelligenceSnapshot(models.Model):
    """
    SINGLE SOURCE OF TRUTH for frontend and API responses.

    This is the ONLY model that frontend and API clients query directly.
    All researcher input models feed into this via ETL process.

    Benefits:
    - 1 query per page instead of 15
    - Fast comparisons (denormalized columns with indexes)
    - AI-ready with embedding field
    - Versioning support

    Relationship path to Business:
        snapshot.business → direct to Business (denormalized for speed)
    """

    class SnapshotStatus(models.TextChoices):
        DRAFT = "draft", "Draft"
        REVIEW = "review", "Under Review"
        PUBLISHED = "published", "Published"
        ARCHIVED = "archived", "Archived"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Identity
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="snapshots")
    scale_type = models.CharField(max_length=20, choices=ScaleType.choices, null=True, blank=True, db_index=True)
    year = models.IntegerField(db_index=True)

    # Versioning
    version = models.IntegerField(default=1)
    is_latest = models.BooleanField(default=True, db_index=True)
    previous_version = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)

    # Status
    status = models.CharField(max_length=20, choices=SnapshotStatus.choices, default=SnapshotStatus.DRAFT, db_index=True)
    published_at = models.DateTimeField(null=True, blank=True)

    # THE COMPLETE DATA (matches frontend expected format)
    data = models.JSONField(help_text="Complete business intelligence document")

    # Denormalized columns for FAST queries (extracted from data on save)
    startup_cost = models.IntegerField(null=True, blank=True, db_index=True)
    gross_margin_pct = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, db_index=True)
    net_margin_pct = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    payback_months = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, db_index=True)
    feasibility_score = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True, db_index=True)
    risk_score = models.IntegerField(null=True, blank=True, db_index=True)
    min_investment = models.IntegerField(null=True, blank=True, db_index=True)
    max_investment = models.IntegerField(null=True, blank=True, db_index=True)

    # Denormalized from business for fast filtering
    sector_id = models.UUIDField(db_index=True)
    business_name = models.CharField(max_length=200, db_index=True)
    business_slug = models.CharField(max_length=200)

    # AI readiness
    embedding = models.JSONField(null=True, blank=True, help_text="Vector embedding for semantic search")
    summary_text = models.TextField(blank=True, help_text="Natural language summary for AI context")

    # Source
    primary_source = models.ForeignKey(Source, on_delete=models.PROTECT, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "intelligence_snapshots"
        verbose_name = "Intelligence snapshot"
        verbose_name_plural = "Intelligence snapshots"
        unique_together = ["business", "scale_type", "year", "version"]
        indexes = [
            models.Index(fields=["year", "scale_type", "status", "is_latest"]),
            models.Index(fields=["sector_id", "year", "status"]),
            models.Index(fields=["startup_cost", "payback_months"]),
            models.Index(fields=["gross_margin_pct", "feasibility_score"]),
            models.Index(fields=["min_investment", "max_investment"]),
            models.Index(fields=["is_latest", "status", "published_at"]),
        ]

    def __str__(self):
        scale_part = f" ({self.scale_type})" if self.scale_type else ""
        return f"{self.business_name} {self.year}{scale_part} v{self.version}"

    def save(self, *args, **kwargs):
        # Denormalize from business
        if self.business_id:
            self.business_name = self.business.name
            self.business_slug = self.business.slug
            self.sector_id = self.business.sector_id

        # Extract denormalized fields from data JSON
        if self.data:
            metrics = self.data.get("metrics", {})
            
            startup = metrics.get("startup_cost", {})
            self.startup_cost = startup.get("value") or startup.get("min")
            
            inv_range = self.data.get("investment_range", {})
            self.min_investment = inv_range.get("min")
            self.max_investment = inv_range.get("max")
            
            self.gross_margin_pct = metrics.get("gross_margin", {}).get("value")
            self.net_margin_pct = metrics.get("net_margin", {}).get("value")
            
            payback = metrics.get("payback_period", {})
            if payback.get("unit") == "months":
                self.payback_months = payback.get("value") or payback.get("min")
            elif payback.get("unit") == "weeks":
                val = payback.get("value") or payback.get("min")
                if val:
                    self.payback_months = val / 4.33
            
            feasibility = self.data.get("feasibility_overall", {})
            self.feasibility_score = feasibility.get("score")
            
            risks = self.data.get("risks", [])
            if risks:
                scores = [r.get("score", 0) for r in risks if r.get("score")]
                if scores:
                    self.risk_score = sum(scores) // len(scores)

        # Set published_at when status changes to published
        if self.status == self.SnapshotStatus.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()

        # Mark older versions as not latest
        if self.is_latest and self.business_id and self.year:
            IntelligenceSnapshot.objects.filter(
                business=self.business,
                scale_type=self.scale_type,
                year=self.year,
                is_latest=True
            ).exclude(pk=self.pk).update(is_latest=False)

        super().save(*args, **kwargs)

    @property
    def display_data(self):
        """Return data with computed display values."""
        result = self.data.copy() if self.data else {}
        
        if "metrics" not in result:
            result["metrics"] = {}
        
        metrics = result["metrics"]
        if self.startup_cost and "startup_cost" not in metrics:
            metrics["startup_cost"] = {
                "value": self.startup_cost,
                "display": f"D{self.startup_cost:,}"
            }
        
        if self.gross_margin_pct and "gross_margin" not in metrics:
            metrics["gross_margin"] = {
                "value": float(self.gross_margin_pct),
                "display": f"{self.gross_margin_pct}%"
            }
        
        return result


# ============================================================
# OPERATIONS CHECKLIST
# ============================================================

class OperationsChecklist(models.Model):
    """
    Recurring operational tasks for running a business.

    Relationship path to Business:
        checklist.business → direct to Business
    """

    class TaskType(models.TextChoices):
        DAILY = "daily", "Daily"
        WEEKLY = "weekly", "Weekly"
        MONTHLY = "monthly", "Monthly"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="checklists")

    scale_type = models.CharField(
        max_length=20,
        choices=ScaleType.choices,
        blank=True,
        help_text="Leave blank if this task applies to all scales",
    )
    task_type = models.CharField(max_length=20, choices=TaskType.choices)
    task_name = models.CharField(max_length=200)
    description = models.TextField(blank=True, help_text="How to perform this task")
    time_of_day = models.CharField(max_length=50, blank=True, help_text="e.g. 'Morning', 'Evening'")
    responsible = models.CharField(max_length=100, blank=True, help_text="Who performs this task")
    duration_minutes = models.PositiveSmallIntegerField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "operations_checklists"
        verbose_name = "Operations checklist"
        verbose_name_plural = "Operations checklists"
        ordering = ["business", "scale_type", "task_type", "order"]

    def __str__(self):
        scale = self.get_scale_type_display() if self.scale_type else "All scales"
        return f"{self.business.name} ({scale}) — {self.task_name}"


# ============================================================
# BUSINESS PROFILE (real businesses - renamed related_business)
# ============================================================

class BusinessProfile(BaseModel):
    """
    A real company that has been interviewed, featured, or verified.

    `business_type` links to the canonical Business type this company represents.

    Relationship path to canonical Business:
        profile.business_type → Business (optional, can be null)
    """

    # Identity
    name = models.CharField(max_length=200)
    owner_name = models.CharField(max_length=200, blank=True)
    owner_position = models.CharField(max_length=100, blank=True, help_text="e.g. 'Founder', 'CEO'")
    description = models.TextField()
    short_description = models.CharField(max_length=200, blank=True)

    # Media
    logo = models.ImageField(upload_to=profile_logo_path, blank=True, null=True)
    cover_image = models.ImageField(upload_to=profile_cover_path, blank=True, null=True)

    # Contact
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    website = models.URLField(blank=True)
    address = models.TextField(blank=True)
    location = models.CharField(
        max_length=200,
        blank=True,
        help_text="City or region, e.g. 'Banjul', 'Serekunda', 'Brikama'",
    )

    # Social media
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    tiktok = models.URLField(blank=True)
    whatsapp = models.CharField(max_length=50, blank=True)

    # Business details
    founded_year = models.PositiveSmallIntegerField(null=True, blank=True)
    employee_count = models.CharField(max_length=50, blank=True, help_text="e.g. '1–5', '10–50'")
    business_type_legal = models.CharField(
        max_length=100, 
        blank=True, 
        help_text="Legal structure: e.g. 'Sole proprietorship', 'LLC'"
    )

    # Relationships (RENAMED from related_business to business_type)
    sector = models.ForeignKey(
        Sector,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="profiles",
    )
    business_type = models.ForeignKey(
        Business,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="profiles",
        help_text="The canonical Business type this company represents (e.g., 'Poultry Farming – Broilers')",
    )
    user = models.OneToOneField(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="business_profile",
        help_text="Linked user account for future self-service profile management",
    )

    # Classification
    is_partner = models.BooleanField(default=False, help_text="Trusted partner / service provider", db_index=True)
    is_featured = models.BooleanField(default=False, db_index=True)
    is_verified = models.BooleanField(default=False, help_text="Verified by GAMBIH team", db_index=True)
    partner_type = models.CharField(
        max_length=50,
        blank=True,
        help_text="e.g. 'consultant', 'supplier', 'legal', 'financial', 'training'",
    )

    # Interview metadata
    interview_date = models.DateField(null=True, blank=True)
    interviewed_by = models.CharField(max_length=100, default="Ebrima Barry")
    interview_notes = models.TextField(blank=True, help_text="Internal notes — not published")

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PUBLISHED, db_index=True)
    view_count = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "business_profiles"
        verbose_name = "Business profile"
        verbose_name_plural = "Business profiles"
        ordering = ["-is_featured", "-is_verified", "name"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["is_partner", "is_verified"]),
            models.Index(fields=["sector"]),
            models.Index(fields=["location"]),
            models.Index(fields=["status"]),
            models.Index(fields=["business_type"]),  # Index for filtering by canonical business
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = self._generate_slug("name")
        super().save(*args, **kwargs)

    def increment_view_count(self):
        self.view_count = F("view_count") + 1
        self.save(update_fields=["view_count"])

    @property
    def partner_type_display(self) -> str:
        labels = {
            "consultant": "Business consultant",
            "supplier": "Equipment / supplier",
            "legal": "Legal services",
            "financial": "Financial services",
            "marketing": "Marketing agency",
            "tech": "Technology provider",
            "training": "Training provider",
        }
        return labels.get(self.partner_type, self.partner_type)


class BusinessProfileFeature(models.Model):
    """Headline achievement or metric for a BusinessProfile page."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business_profile = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name="features")

    title = models.CharField(max_length=200, help_text="e.g. '25% revenue growth in year one'")
    description = models.TextField()
    icon = models.CharField(max_length=50, blank=True, help_text="Lucide React icon name")
    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "business_profile_features"
        verbose_name = "Business profile feature"
        verbose_name_plural = "Business profile features"
        ordering = ["order"]


class BusinessProfileTestimonial(models.Model):
    """Owner or client quote for a BusinessProfile page."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business_profile = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name="testimonials")

    quote = models.TextField()
    author_name = models.CharField(max_length=100)
    author_position = models.CharField(max_length=100, blank=True)
    is_featured = models.BooleanField(default=False, help_text="Display on homepage")
    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "business_profile_testimonials"
        verbose_name = "Business profile testimonial"
        verbose_name_plural = "Business profile testimonials"
        ordering = ["order"]