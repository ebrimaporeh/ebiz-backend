from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.core.models import BaseModel
from apps.core.constants import Status
from apps.sectors.models import Sector
from apps.businesses.models import Business


class ContentType(models.TextChoices):
    ARTICLE = 'article', 'Article'
    VIDEO = 'video', 'Video'
    CASE_STUDY = 'case_study', 'Case Study'
    INTERVIEW = 'interview', 'Interview'


class VideoPlatform(models.TextChoices):
    YOUTUBE = 'youtube', 'YouTube'
    TIKTOK = 'tiktok', 'TikTok'
    VIMEO = 'vimeo', 'Vimeo'


# ============================================
# ARTICLE MODEL
# ============================================

class Article(BaseModel):
    """Blog articles and written content"""
    
    title = models.CharField(
        max_length=200,
        help_text="Article title"
    )
    
    excerpt = models.CharField(
        max_length=300,
        help_text="Short summary displayed in listings"
    )
    
    content = models.TextField(
        help_text="Full article content (HTML or Markdown)"
    )
    
    premium_content = models.TextField(
        blank=True,
        help_text="Premium-only content (shown only to subscribers)"
    )
    
    featured_image = models.ImageField(
        upload_to='articles/',
        blank=True,
        null=True,
        help_text="Main image for the article"
    )
    
    # Relationships
    sector = models.ForeignKey(
        Sector,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='articles',
        help_text="Primary sector this article belongs to"
    )
    
    business = models.ForeignKey(
        Business,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='articles',
        help_text="Specific business this article is about"
    )
    
    # Metadata
    author = models.CharField(
        max_length=100,
        default="GBI Research Team",
        help_text="Author name"
    )
    
    read_time = models.PositiveSmallIntegerField(
        default=5,
        help_text="Estimated read time in minutes"
    )
    
    is_premium = models.BooleanField(
        default=False,
        help_text="Whether this article requires premium subscription"
    )
    
    is_featured = models.BooleanField(
        default=False,
        help_text="Display on homepage and featured sections"
    )
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        help_text="Publication status"
    )
    
    published_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the article was published"
    )
    
    # Stats
    view_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of views"
    )
    
    like_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of likes"
    )
    
    # SEO
    meta_title = models.CharField(
        max_length=150,
        blank=True,
        help_text="SEO title (defaults to article title)"
    )
    
    meta_description = models.CharField(
        max_length=300,
        blank=True,
        help_text="SEO description"
    )
    
    class Meta:
        db_table = 'articles'
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['status', 'published_at']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['sector']),
            models.Index(fields=['business']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Article.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def increment_view_count(self):
        self.view_count += 1
        self.save(update_fields=['view_count'])
    
    @property
    def has_premium_content(self):
        return bool(self.premium_content)


# ============================================
# VIDEO MODEL
# ============================================

class Video(BaseModel):
    """Video content from YouTube, TikTok, etc."""
    
    title = models.CharField(
        max_length=200,
        help_text="Video title"
    )
    
    description = models.TextField(
        blank=True,
        help_text="Video description"
    )
    
    platform = models.CharField(
        max_length=20,
        choices=VideoPlatform.choices,
        default=VideoPlatform.YOUTUBE,
        help_text="Video platform"
    )
    
    platform_video_id = models.CharField(
        max_length=100,
        help_text="Video ID from the platform (e.g., YouTube video ID)"
    )
    
    video_url = models.URLField(
        blank=True,
        help_text="Full video URL (auto-generated from platform and ID)"
    )
    
    thumbnail_url = models.URLField(
        blank=True,
        help_text="Thumbnail image URL"
    )
    
    duration = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="Duration in seconds"
    )
    
    # Relationships
    sector = models.ForeignKey(
        Sector,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='videos',
        help_text="Primary sector this video belongs to"
    )
    
    business = models.ForeignKey(
        Business,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='videos',
        help_text="Specific business this video is about"
    )
    
    # Metadata
    is_premium = models.BooleanField(
        default=False,
        help_text="Whether this video requires premium subscription"
    )
    
    is_featured = models.BooleanField(
        default=False,
        help_text="Display on homepage and featured sections"
    )
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PUBLISHED,
        help_text="Publication status"
    )
    
    published_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the video was published"
    )
    
    # Stats
    view_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of views"
    )
    
    like_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of likes"
    )
    
    comment_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of comments"
    )
    
    class Meta:
        db_table = 'videos'
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['status', 'published_at']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['platform']),
            models.Index(fields=['sector']),
            models.Index(fields=['business']),
        ]
    
    def __str__(self):
        return self.title
   
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Video.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        
        # Auto-generate video URL from platform and ID
        if self.platform == VideoPlatform.YOUTUBE and self.platform_video_id:
            self.video_url = f"https://www.youtube.com/watch?v={self.platform_video_id}"
        elif self.platform == VideoPlatform.TIKTOK and self.platform_video_id:
            self.video_url = f"https://www.tiktok.com/@/video/{self.platform_video_id}"
        elif self.platform == VideoPlatform.VIMEO and self.platform_video_id:
            self.video_url = f"https://vimeo.com/{self.platform_video_id}"
        
        super().save(*args, **kwargs)

    def increment_view_count(self):
        self.view_count += 1
        self.save(update_fields=['view_count'])
    
    @property
    def embed_url(self):
        """Get embed URL for iframe"""
        if self.platform == VideoPlatform.YOUTUBE and self.platform_video_id:
            return f"https://www.youtube.com/embed/{self.platform_video_id}"
        elif self.platform == VideoPlatform.VIMEO and self.platform_video_id:
            return f"https://player.vimeo.com/video/{self.platform_video_id}"
        return None


# ============================================
# CASE STUDY MODEL
# ============================================

class CaseStudy(BaseModel):
    """Real-world success/failure stories of Gambian businesses"""
    
    title = models.CharField(
        max_length=200,
        help_text="Case study title"
    )
    
    excerpt = models.CharField(
        max_length=300,
        help_text="Short summary"
    )
    
    content = models.TextField(
        help_text="Full case study content"
    )
    
    featured_image = models.ImageField(
        upload_to='case-studies/',
        blank=True,
        null=True,
        help_text="Main image"
    )
    
    # Business details
    business_name = models.CharField(
        max_length=200,
        help_text="Name of the business being studied"
    )
    
    business_type = models.CharField(
        max_length=100,
        help_text="Type of business (e.g., Poultry Farm, Taxi Service)"
    )
    
    sector = models.ForeignKey(
        Sector,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='case_studies',
        help_text="Sector this case study belongs to"
    )
    
    # Key metrics
    initial_investment = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Initial investment amount in Dalasi"
    )
    
    revenue_generated = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Revenue generated in Dalasi"
    )
    
    roi_percent = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Return on investment percentage"
    )
    
    timeline_months = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="Timeline in months to achieve results"
    )
    
    # Outcome
    is_success = models.BooleanField(
        default=True,
        help_text="Whether this is a success story (True) or failure (False)"
    )
    
    key_lessons = models.TextField(
        help_text="Key takeaways and lessons learned"
    )
    
    # Metadata
    author = models.CharField(
        max_length=100,
        default="GBI Research Team",
        help_text="Author name"
    )
    
    is_featured = models.BooleanField(
        default=False,
        help_text="Display on homepage and featured sections"
    )
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        help_text="Publication status"
    )
    
    published_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the case study was published"
    )
    
    view_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of views"
    )
    
    class Meta:
        db_table = 'case_studies'
        verbose_name = 'Case Study'
        verbose_name_plural = 'Case Studies'
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['status', 'published_at']),
            models.Index(fields=['sector']),
            models.Index(fields=['is_success']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while CaseStudy.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def increment_view_count(self):
        self.view_count += 1
        self.save(update_fields=['view_count'])


# ============================================
# TAG MODEL
# ============================================

class Tag(BaseModel):
    """Tags for categorizing content"""
    
    name = models.CharField(
        max_length=50,
        unique=True,
        help_text="Tag name (e.g., 'Startup Tips', 'Investment')"
    )
    
    articles = models.ManyToManyField(
        Article,
        blank=True,
        related_name='tags',
        help_text="Articles with this tag"
    )
    
    videos = models.ManyToManyField(
        Video,
        blank=True,
        related_name='tags',
        help_text="Videos with this tag"
    )
    
    case_studies = models.ManyToManyField(
        CaseStudy,
        blank=True,
        related_name='tags',
        help_text="Case studies with this tag"
    )
    
    usage_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of times this tag is used (auto-updated)"
    )
    
    class Meta:
        db_table = 'tags'
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['usage_count']),
        ]
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def update_usage_count(self):
        """Update usage count based on relationships"""
        count = self.articles.count() + self.videos.count() + self.case_studies.count()
        self.usage_count = count
        self.save(update_fields=['usage_count'])


# ============================================
# COMMENT MODEL (for articles)
# ============================================


class Comment(models.Model):
    """User comments on articles"""
    
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text="Article this comment belongs to"
    )
    
    user_name = models.CharField(
        max_length=100,
        help_text="Commenter's name"
    )
    
    user_email = models.EmailField(
        help_text="Commenter's email"
    )
    
    content = models.TextField(
        help_text="Comment content"
    )
    
    is_approved = models.BooleanField(
        default=False,
        help_text="Whether the comment is approved for display"
    )
    
    like_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of likes"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'comments'
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['article', 'is_approved']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"Comment by {self.user_name} on {self.article.title}"
    
    def approve(self):
        self.is_approved = True
        self.save(update_fields=['is_approved'])