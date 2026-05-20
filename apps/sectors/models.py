from django.db import models
from django.utils.text import slugify

from apps.core.models import BaseModel
from apps.core.constants import Status


class Sector(BaseModel):
    """Business sector/category (e.g., Agriculture, Transportation, Technology)"""
    
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Sector name (e.g., Agriculture, Transportation)"
    )
    
    description = models.TextField(
        blank=True,
        help_text="Detailed description of the sector"
    )
    
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Icon name from Lucide React (e.g., 'Truck', 'Leaf')"
    )
    
    color = models.CharField(
        max_length=20,
        blank=True,
        help_text="Color code for the sector (e.g., 'blue', 'green')"
    )
    
    featured_image = models.ImageField(
        upload_to='sectors/',
        blank=True,
        null=True,
        help_text="Featured image for the sector"
    )
    
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order on the website"
    )
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PUBLISHED,
        help_text="Publication status"
    )
    
    # Metadata
    business_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of businesses in this sector (automatically updated)"
    )
    
    class Meta:
        db_table = 'sectors'
        verbose_name = 'Sector'
        verbose_name_plural = 'Sectors'
        ordering = ['order', 'name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['status']),
            models.Index(fields=['order']),
        ]
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)