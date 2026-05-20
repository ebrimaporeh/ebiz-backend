import re
from django.utils.text import slugify


def generate_unique_slug(instance, field='name'):
    """Generate unique slug for a model instance."""
    base_slug = slugify(getattr(instance, field))
    slug = base_slug
    ModelClass = instance.__class__
    counter = 1
    
    while ModelClass.objects.filter(slug=slug).exclude(pk=instance.pk).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    
    return slug


def format_currency(amount):
    """Format amount in Gambian Dalasi."""
    return f"D{amount:,.0f}"


def calculate_risk_score(likelihood, impact):
    """Calculate risk score from likelihood and impact."""
    return likelihood * impact