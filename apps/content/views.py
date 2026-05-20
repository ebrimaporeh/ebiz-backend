from rest_framework import viewsets, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from apps.core.pagination import StandardPagination
from apps.core.permissions import IsAdminOrReadOnly, IsPremiumUser
from .models import Article, Video, CaseStudy, Tag, Comment
from .serializers import (
    ArticleSerializer, ArticleListSerializer, ArticleDetailSerializer,
    VideoSerializer, VideoListSerializer, VideoDetailSerializer,
    CaseStudyListSerializer, CaseStudyDetailSerializer,
    TagSerializer, CommentSerializer
)


class ArticleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Article model.
    
    Provides CRUD operations for blog articles.
    Public: Read-only access to free content
    Premium users: Full content access
    Admin: Full CRUD access
    """
    
    queryset = Article.objects.filter(is_deleted=False).select_related('sector', 'business')
    serializer_class = ArticleSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'excerpt', 'content', 'author']
    filterset_fields = ['sector', 'status', 'is_premium', 'is_featured']
    ordering_fields = ['view_count', 'published_at', 'created_at']
    ordering = ['-published_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleListSerializer
        elif self.action == 'retrieve':
            return ArticleDetailSerializer
        return ArticleSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Non-admin users only see published articles
        if not self.request.user.is_staff:
            queryset = queryset.filter(status='published')
        
        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        """Get article with premium content filtering"""
        instance = self.get_object()
        
        # Check if user has access to premium content
        if instance.is_premium and not request.user.has_premium_access:
            # Return article without premium content
            serializer = ArticleDetailSerializer(instance)
            data = serializer.data
            data['premium_content'] = None
            data['premium_locked'] = True
            return Response(data)
        
        # Increment view count
        instance.increment_view_count()
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """Like an article"""
        article = self.get_object()
        article.like_count += 1
        article.save(update_fields=['like_count'])
        return Response({'like_count': article.like_count})
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured articles"""
        featured = self.get_queryset().filter(is_featured=True)[:6]
        serializer = ArticleListSerializer(featured, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def add_comment(self, request):
        """Add a comment to an article"""
        article_id = request.data.get('article_id')
        user_name = request.data.get('user_name')
        user_email = request.data.get('user_email')
        content = request.data.get('content')
        
        if not all([article_id, user_name, user_email, content]):
            return Response(
                {'error': 'All fields are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            return Response(
                {'error': 'Article not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        comment = Comment.objects.create(
            article=article,
            user_name=user_name,
            user_email=user_email,
            content=content
        )
        
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VideoViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Video model.
    """
    
    queryset = Video.objects.filter(is_deleted=False).select_related('sector', 'business')
    serializer_class = VideoSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    filterset_fields = ['sector', 'platform', 'status', 'is_premium', 'is_featured']
    ordering_fields = ['view_count', 'published_at', 'created_at']
    ordering = ['-published_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return VideoListSerializer
        elif self.action == 'retrieve':
            return VideoDetailSerializer
        return VideoSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        if not self.request.user.is_staff:
            queryset = queryset.filter(status='published')
        
        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        """Get video with access control"""
        instance = self.get_object()
        
        if instance.is_premium and not request.user.has_premium_access:
            return Response(
                {'error': 'Premium subscription required', 'premium_locked': True},
                status=status.HTTP_403_FORBIDDEN
            )
        
        instance.increment_view_count()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured videos"""
        featured = self.get_queryset().filter(is_featured=True)[:6]
        serializer = VideoListSerializer(featured, many=True)
        return Response(serializer.data)


class CaseStudyViewSet(viewsets.ModelViewSet):
    """
    ViewSet for CaseStudy model.
    """
    
    queryset = CaseStudy.objects.filter(is_deleted=False).select_related('sector')
    serializer_class = CaseStudyListSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'business_name', 'content', 'key_lessons']
    filterset_fields = ['sector', 'is_success', 'status', 'is_featured']
    ordering_fields = ['view_count', 'published_at']
    ordering = ['-published_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CaseStudyListSerializer
        elif self.action == 'retrieve':
            return CaseStudyDetailSerializer
        return CaseStudyListSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        if not self.request.user.is_staff:
            queryset = queryset.filter(status='published')
        
        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        """Get case study with view count increment"""
        instance = self.get_object()
        instance.increment_view_count()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def success_stories(self, request):
        """Get only success stories"""
        success_stories = self.get_queryset().filter(is_success=True)[:10]
        serializer = CaseStudyListSerializer(success_stories, many=True)
        return Response(serializer.data)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only ViewSet for Tag model"""
    
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = StandardPagination
    search_fields = ['name']
    ordering = ['name']
    
    @action(detail=True, methods=['get'])
    def articles(self, request, pk=None):
        """Get articles with this tag"""
        tag = self.get_object()
        articles = tag.articles.filter(status='published')
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def videos(self, request, pk=None):
        """Get videos with this tag"""
        tag = self.get_object()
        videos = tag.videos.filter(status='published')
        serializer = VideoListSerializer(videos, many=True)
        return Response(serializer.data)