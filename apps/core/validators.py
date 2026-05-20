from django.core.exceptions import ValidationError


def validate_positive_number(value):
    """Ensure value is greater than zero."""
    if value <= 0:
        raise ValidationError('Value must be greater than zero.')


def validate_rating(value):
    """Ensure rating is between 1 and 10."""
    if value < 1 or value > 10:
        raise ValidationError('Rating must be between 1 and 10.')