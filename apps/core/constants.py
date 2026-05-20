from django.db import models


# ============================================
# USER TIER CHOICES
# ============================================

class UserTier(models.TextChoices):
    REGULAR = 'regular', 'Regular (Free)'
    PREMIUM = 'premium', 'Premium (Subscription)'
    ONE_TIME = 'one_time', 'One-Time Purchase'


# ============================================
# MODEL CHOICES (Existing)
# ============================================

class Status(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    PUBLISHED = 'published', 'Published'
    ARCHIVED = 'archived', 'Archived'


class ScaleType(models.TextChoices):
    SMALL = 'small', 'Small Scale'
    MEDIUM = 'medium', 'Medium Scale'
    LARGE = 'large', 'Large Scale'


class Priority(models.TextChoices):
    ESSENTIAL = 'essential', 'Essential'
    MEDIUM = 'medium', 'Medium Priority'
    OPTIONAL = 'optional', 'Optional'


class RiskCategory(models.TextChoices):
    MARKET = 'market', 'Market Risk'
    OPERATIONAL = 'operational', 'Operational Risk'
    FINANCIAL = 'financial', 'Financial Risk'
    REGULATORY = 'regulatory', 'Regulatory Risk'
    EXTERNAL = 'external', 'External Risk'


class FeasibilityCategory(models.TextChoices):
    MARKET = 'market', 'Market Analysis'
    CAPITAL = 'capital', 'Capital Requirements'
    PROFITABILITY = 'profitability', 'Profitability'
    REGULATORY = 'regulatory', 'Regulatory'
    RISK = 'risk', 'Risk Assessment'
    SKILLS = 'skills', 'Skills Required'
    SUPPLY_CHAIN = 'supply_chain', 'Supply Chain'


# ============================================
# ERROR MESSAGES
# ============================================

ERROR_MESSAGES = {
    'not_found': 'The requested resource was not found.',
    'permission_denied': 'You do not have permission to perform this action.',
    'invalid_data': 'The provided data is invalid.',
    'subscription_required': 'This content requires a premium subscription.',
    'already_exists': 'A record with this information already exists.',
}