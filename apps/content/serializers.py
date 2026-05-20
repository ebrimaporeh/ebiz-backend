from rest_framework import serializers
from .models import Article, Video, CaseStudy, Tag, Comment


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag model"""
    
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'usage_count']


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model"""
    
    class Meta:
        model = Comment
        fields = ['id', 'user_name', 'content', 'like_count', 'created_at', 'is_approved']
        read_only_fields = ['like_count', 'created_at', 'is_approved']


class ArticleListSerializer(serializers.ModelSerializer):
    """Minimal serializer for article list views"""
    
    sector_name = serializers.ReadOnlyField(source='sector.name')
    business_name = serializers.ReadOnlyField(source='business.name')
    
    class Meta:
        model = Article
        fields = [
            'id', 'title', 'slug', 'excerpt', 'featured_image',
            'author', 'read_time', 'is_premium', 'is_featured',
            'view_count', 'published_at', 'sector_name', 'business_name'
        ]


class ArticleDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for single article view"""
    
    sector_name = serializers.ReadOnlyField(source='sector.name')
    business_name = serializers.ReadOnlyField(source='business.name')
    tags = TagSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    status_display = serializers.ReadOnlyField(source='get_status_display')
    has_premium_content = serializers.ReadOnlyField()
    
    class Meta:
        model = Article
        fields = [
            'id', 'title', 'slug', 'excerpt', 'content', 'premium_content',
            'featured_image', 'author', 'read_time', 'is_premium',
            'is_featured', 'status', 'status_display', 'published_at',
            'view_count', 'like_count', 'sector', 'sector_name',
            'business', 'business_name', 'tags', 'comments',
            'meta_title', 'meta_description', 'has_premium_content',
            'created_at', 'updated_at'
        ]


class ArticleSerializer(serializers.ModelSerializer):
    """Base serializer for CRUD operations"""
    
    class Meta:
        model = Article
        fields = '__all__'


class VideoListSerializer(serializers.ModelSerializer):
    """Minimal serializer for video list views"""
    
    sector_name = serializers.ReadOnlyField(source='sector.name')
    
    class Meta:
        model = Video
        fields = [
            'id', 'title', 'slug', 'description', 'thumbnail_url',
            'platform', 'duration', 'is_premium', 'is_featured',
            'view_count', 'published_at', 'sector_name'
        ]


class VideoDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for single video view"""
    
    sector_name = serializers.ReadOnlyField(source='sector.name')
    business_name = serializers.ReadOnlyField(source='business.name')
    tags = TagSerializer(many=True, read_only=True)
    embed_url = serializers.ReadOnlyField()
    
    class Meta:
        model = Video
        fields = [
            'id', 'title', 'slug', 'description', 'platform',
            'platform_video_id', 'video_url', 'embed_url', 'thumbnail_url',
            'duration', 'is_premium', 'is_featured', 'published_at',
            'view_count', 'like_count', 'comment_count',
            'sector', 'sector_name', 'business', 'business_name',
            'tags', 'created_at', 'updated_at'
        ]


class VideoSerializer(serializers.ModelSerializer):
    """Base serializer for CRUD operations"""
    
    class Meta:
        model = Video
        fields = '__all__'


class CaseStudyListSerializer(serializers.ModelSerializer):
    """Minimal serializer for case study list views"""
    
    sector_name = serializers.ReadOnlyField(source='sector.name')
    
    class Meta:
        model = CaseStudy
        fields = [
            'id', 'title', 'slug', 'excerpt', 'featured_image',
            'business_name', 'business_type', 'is_success',
            'is_featured', 'view_count', 'published_at', 'sector_name'
        ]


class CaseStudyDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for single case study view"""
    
    sector_name = serializers.ReadOnlyField(source='sector.name')
    tags = TagSerializer(many=True, read_only=True)
    
    class Meta:
        model = CaseStudy
        fields = [
            'id', 'title', 'slug', 'excerpt', 'content', 'featured_image',
            'business_name', 'business_type', 'sector', 'sector_name',
            'initial_investment', 'revenue_generated', 'roi_percent',
            'timeline_months', 'is_success', 'key_lessons',
            'author', 'is_featured', 'published_at', 'view_count',
            'tags', 'created_at', 'updated_at'
        ]