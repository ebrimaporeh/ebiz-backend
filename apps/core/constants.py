"""
apps/core/constants.py

Global constants and choices for GAMBIH platform.
Includes country, currency, region, and other shared enums.
"""

from django.db import models


# ============================================
# STATUS CHOICES
# ============================================

class Status(models.TextChoices):
    """Publication status for content and businesses."""
    DRAFT = "draft", "Draft"
    REVIEW = "review", "Under Review"
    PUBLISHED = "published", "Published"
    ARCHIVED = "archived", "Archived"


# ============================================
# BUSINESS SCALE CHOICES
# ============================================

class ScaleType(models.TextChoices):
    """Operational scale for businesses."""
    SMALL = "small", "Small Scale"
    MEDIUM = "medium", "Medium Scale"
    LARGE = "large", "Large Scale"


# ============================================
# PRIORITY CHOICES
# ============================================

class Priority(models.TextChoices):
    """Priority levels for capital items and tasks."""
    ESSENTIAL = "essential", "Essential"
    RECOMMENDED = "recommended", "Recommended"
    OPTIONAL = "optional", "Optional"


# ============================================
# RISK CATEGORY CHOICES
# ============================================

class RiskCategory(models.TextChoices):
    """Risk classification categories."""
    MARKET = "market", "Market Risk"
    OPERATIONAL = "operational", "Operational Risk"
    FINANCIAL = "financial", "Financial Risk"
    REGULATORY = "regulatory", "Regulatory Risk"
    SUPPLY = "supply", "Supply Chain Risk"
    CLIMATE = "climate", "Climate / Environmental Risk"
    COMPETITIVE = "competitive", "Competitive Risk"
    TECHNOLOGICAL = "technological", "Technological Risk"


# ============================================
# FEASIBILITY CATEGORY CHOICES
# ============================================

class FeasibilityCategory(models.TextChoices):
    """Factors affecting business feasibility."""
    MARKET = "market", "Market Analysis"
    FINANCIAL = "financial", "Financial Viability"
    OPERATIONS = "operations", "Operational Capacity"
    REGULATORY = "regulatory", "Regulatory Environment"
    TECHNICAL = "technical", "Technical Requirements"
    COMPETITIVE = "competitive", "Competitive Landscape"


# ============================================
# COUNTRY CHOICES (West Africa Focus)
# ============================================

class Country(models.TextChoices):
    """West African countries for platform expansion."""
    # Primary (Active)
    GAMBIA = "gm", "The Gambia"
    SENEGAL = "sn", "Senegal"
    GHANA = "gh", "Ghana"
    
    # Secondary (Planned)
    NIGERIA = "ng", "Nigeria"
    COTE_DIVOIRE = "ci", "Côte d'Ivoire"
    MALI = "ml", "Mali"
    BURKINA_FASO = "bf", "Burkina Faso"
    GUINEA = "gn", "Guinea"
    GUINEA_BISSAU = "gw", "Guinea-Bissau"
    SIERRA_LEONE = "sl", "Sierra Leone"
    LIBERIA = "lr", "Liberia"
    BENIN = "bj", "Benin"
    TOGO = "tg", "Togo"
    CAPE_VERDE = "cv", "Cape Verde"
    NIGER = "ne", "Niger"
    MAURITANIA = "mr", "Mauritania"


# ============================================
# REGION CHOICES
# ============================================

class Region(models.TextChoices):
    """Regional groupings for cross-country analysis."""
    WEST_AFRICA = "west_africa", "West Africa"
    ECOWAS = "ecowas", "ECOWAS (Economic Community of West African States)"
    COASTAL = "coastal", "Coastal West Africa"
    SAHELIAN = "sahelian", "Sahelian West Africa"
    GAMBIA_RIVER_BASIN = "gambia_river", "Gambia River Basin"
    FRANCOPHONE = "francophone", "Francophone West Africa"
    ANGLOPHONE = "anglophone", "Anglophone West Africa"


# ============================================
# REGION TO COUNTRIES MAPPING (for filtering)
# ============================================

REGION_COUNTRIES = {
    Region.WEST_AFRICA: [
        "gm", "sn", "gw", "gn", "ml", "bf", "ci", "gh", "tg", "bj", 
        "ng", "sl", "lr", "cv", "ne", "mr"
    ],
    Region.ECOWAS: [
        "gm", "sn", "gw", "gn", "ml", "bf", "ci", "gh", "tg", "bj", "ng", "sl", "lr", "cv"
    ],
    Region.COASTAL: [
        "sn", "gw", "gn", "ci", "gh", "tg", "bj", "ng", "sl", "lr"
    ],
    Region.SAHELIAN: [
        "gm", "sn", "ml", "bf", "ng", "ne", "mr"
    ],
    Region.GAMBIA_RIVER_BASIN: [
        "gm", "sn", "gw", "gn"
    ],
    Region.FRANCOPHONE: [
        "sn", "gw", "gn", "ml", "bf", "ci", "ne", "mr", "tg", "bj"
    ],
    Region.ANGLOPHONE: [
        "gm", "gh", "ng", "sl", "lr"
    ],
}


# ============================================
# CURRENCY CHOICES
# ============================================

class Currency(models.TextChoices):
    """Currencies used across West Africa."""
    GMD = "GMD", "Gambian Dalasi"
    XOF = "XOF", "West African CFA Franc"
    GHS = "GHS", "Ghanaian Cedi"
    NGN = "NGN", "Nigerian Naira"
    USD = "USD", "US Dollar"
    GNF = "GNF", "Guinean Franc"
    SLL = "SLL", "Sierra Leonean Leone"
    LRD = "LRD", "Liberian Dollar"
    CVE = "CVE", "Cape Verdean Escudo"
    MRU = "MRU", "Mauritanian Ouguiya"


# ============================================
# CURRENCY SYMBOLS
# ============================================

CURRENCY_SYMBOLS = {
    Currency.GMD: "D",
    Currency.XOF: "CFA",
    Currency.GHS: "₵",
    Currency.NGN: "₦",
    Currency.USD: "$",
    Currency.GNF: "FG",
    Currency.SLL: "Le",
    Currency.LRD: "L$",
    Currency.CVE: "$",
    Currency.MRU: "UM",
}


# ============================================
# COUNTRY TO CURRENCY MAPPING
# ============================================

COUNTRY_CURRENCY = {
    Country.GAMBIA: Currency.GMD,
    Country.SENEGAL: Currency.XOF,
    Country.GHANA: Currency.GHS,
    Country.NIGERIA: Currency.NGN,
    Country.COTE_DIVOIRE: Currency.XOF,
    Country.MALI: Currency.XOF,
    Country.BURKINA_FASO: Currency.XOF,
    Country.GUINEA: Currency.GNF,
    Country.GUINEA_BISSAU: Currency.XOF,
    Country.SIERRA_LEONE: Currency.SLL,
    Country.LIBERIA: Currency.LRD,
    Country.BENIN: Currency.XOF,
    Country.TOGO: Currency.XOF,
    Country.CAPE_VERDE: Currency.CVE,
    Country.NIGER: Currency.XOF,
    Country.MAURITANIA: Currency.MRU,
}


# ============================================
# COUNTRY FLAG EMOJIS
# ============================================

COUNTRY_FLAGS = {
    Country.GAMBIA: "🇬🇲",
    Country.SENEGAL: "🇸🇳",
    Country.GHANA: "🇬🇭",
    Country.NIGERIA: "🇳🇬",
    Country.COTE_DIVOIRE: "🇨🇮",
    Country.MALI: "🇲🇱",
    Country.BURKINA_FASO: "🇧🇫",
    Country.GUINEA: "🇬🇳",
    Country.GUINEA_BISSAU: "🇬🇼",
    Country.SIERRA_LEONE: "🇸🇱",
    Country.LIBERIA: "🇱🇷",
    Country.BENIN: "🇧🇯",
    Country.TOGO: "🇹🇬",
    Country.CAPE_VERDE: "🇨🇻",
    Country.NIGER: "🇳🇪",
    Country.MAURITANIA: "🇲🇷",
}


# ============================================
# COUNTRY DISPLAY NAMES (Full names with flags)
# ============================================

def get_country_display_with_flag(code: str) -> str:
    """Get country display name with flag emoji."""
    flag = COUNTRY_FLAGS.get(code, "")
    country_name = dict(Country.choices).get(code, code)
    return f"{flag} {country_name}"


# ============================================
# USER TIER CHOICES
# ============================================

class UserTier(models.TextChoices):
    """Subscription tiers for user access."""
    REGULAR = "regular", "Regular (Free)"
    PREMIUM = "premium", "Premium (Subscription)"
    ONE_TIME = "one_time", "One-Time Purchase"
    PRO = "pro", "Pro"
    ENTERPRISE = "enterprise", "Enterprise"


# ============================================
# REPORT TYPES
# ============================================

class ReportType(models.TextChoices):
    """Types of reports available for purchase."""
    SINGLE_BUSINESS = "single_business", "Single Business Report"
    SECTOR = "sector", "Sector Analysis Report"
    MARKET = "market", "Market Intelligence Report"
    INVESTMENT = "investment", "Investment Opportunity Report"
    CUSTOM = "custom", "Custom Research Report"


# ============================================
# CONTENT TYPES
# ============================================

class ContentType(models.TextChoices):
    """Types of content in the platform."""
    ARTICLE = "article", "Article"
    VIDEO = "video", "Video"
    CASE_STUDY = "case_study", "Case Study"
    INTERVIEW = "interview", "Interview"
    REPORT = "report", "Report"


# ============================================
# VIDEO PLATFORMS
# ============================================

class VideoPlatform(models.TextChoices):
    """Supported video hosting platforms."""
    YOUTUBE = "youtube", "YouTube"
    VIMEO = "vimeo", "Vimeo"
    TIKTOK = "tiktok", "TikTok"
    FACEBOOK = "facebook", "Facebook"
    INSTAGRAM = "instagram", "Instagram"


# ============================================
# PAYMENT METHODS
# ============================================

class PaymentMethod(models.TextChoices):
    """Accepted payment methods."""
    CARD = "card", "Credit/Debit Card"
    MOBILE_MONEY = "mobile_money", "Mobile Money"
    BANK_TRANSFER = "bank_transfer", "Bank Transfer"
    WAVE = "wave", "Wave"
    AFRIMONEY = "afrimoney", "Afrimoney"
    ORANGE_MONEY = "orange_money", "Orange Money"


# ============================================
# PAYMENT STATUS
# ============================================

class PaymentStatus(models.TextChoices):
    """Payment transaction status."""
    PENDING = "pending", "Pending"
    COMPLETED = "completed", "Completed"
    FAILED = "failed", "Failed"
    REFUNDED = "refunded", "Refunded"
    CANCELLED = "cancelled", "Cancelled"


# ============================================
# HELPER FUNCTIONS
# ============================================

def get_country_info(code: str) -> dict:
    """Get complete country information."""
    return {
        "code": code,
        "name": dict(Country.choices).get(code, code),
        "flag": COUNTRY_FLAGS.get(code, ""),
        "currency": COUNTRY_CURRENCY.get(code, Currency.USD),
        "currency_symbol": CURRENCY_SYMBOLS.get(COUNTRY_CURRENCY.get(code, Currency.USD), "$"),
    }


def get_currency_for_country(country_code: str) -> str:
    """Get currency code for a country."""
    return COUNTRY_CURRENCY.get(country_code, Currency.USD)


def get_currency_symbol_for_country(country_code: str) -> str:
    """Get currency symbol for a country."""
    currency = get_currency_for_country(country_code)
    return CURRENCY_SYMBOLS.get(currency, "$")


def get_active_countries() -> list:
    """Get list of primary active countries."""
    return [
        Country.GAMBIA,
        Country.SENEGAL,
        Country.GHANA,
    ]


def get_planned_countries() -> list:
    """Get list of planned expansion countries."""
    return [
        Country.NIGERIA,
        Country.COTE_DIVOIRE,
        Country.MALI,
        Country.BURKINA_FASO,
    ]