from django.db import models

# ============================================
# BASE MIXINS
# ============================================

class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteMixin(models.Model):
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.save()

    class Meta:
        abstract = True


class SlugMixin(models.Model):
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        abstract = True


class BaseModel(TimeStampMixin, SoftDeleteMixin, SlugMixin):
    """Combined base model for all main entities."""
    
    class Meta:
        abstract = True