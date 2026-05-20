from rest_framework import viewsets, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.http import FileResponse, Http404

from apps.core.pagination import StandardPagination
from apps.core.permissions import IsAdminOrReadOnly, IsPremiumUser
from .models import Report, ReportPurchase, ReportBundle, ReportReview
from .serializers import (
    ReportSerializer, ReportListSerializer, ReportDetailSerializer,
    ReportPurchaseSerializer, CreateReportPurchaseSerializer,
    ReportBundleListSerializer, ReportBundleDetailSerializer,
    ReportReviewSerializer, CreateReportReviewSerializer
)


class ReportViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Report model.
    
    Provides CRUD operations for premium reports.
    Public: Read-only access to report info
    Admin: Full CRUD access
    """
    
    queryset = Report.objects.filter(is_deleted=False).select_related('sector', 'business')
    serializer_class = ReportSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'subtitle', 'description', 'author']
    filterset_fields = ['report_type', 'format', 'status', 'is_featured', 'is_bestseller', 'sector']
    ordering_fields = ['price', 'download_count', 'rating', 'published_at', 'created_at']
    ordering = ['-is_featured', '-published_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ReportListSerializer
        elif self.action == 'retrieve':
            return ReportDetailSerializer
        return ReportSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Non-admin users only see published reports
        if not self.request.user.is_staff:
            queryset = queryset.filter(status='published')
        
        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        """Get report with access control"""
        instance = self.get_object()
        
        # Increment view count
        instance.increment_view_count()
        
        serializer = self.get_serializer(instance, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """Download report file (requires purchase or premium)"""
        report = self.get_object()
        user = request.user
        
        # Check if user has access
        has_access = False
        
        if report.is_free:
            has_access = True
        elif user.is_authenticated:
            # Check if user has purchased this report
            has_purchased = ReportPurchase.objects.filter(
                user=user, report=report, is_paid=True
            ).exists()
            
            # Check if user has premium subscription
            has_premium = user.has_premium_access
            
            has_access = has_purchased or has_premium
        
        if not has_access:
            return Response(
                {'error': 'You must purchase this report to download it'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Record download
        if user.is_authenticated:
            purchase = ReportPurchase.objects.filter(user=user, report=report).first()
            if purchase:
                purchase.record_download()
            elif not report.is_free:
                # Create purchase record for premium user downloading
                ReportPurchase.objects.create(
                    user=user,
                    report=report,
                    amount_paid=0,
                    payment_method='premium_subscription',
                    is_paid=True
                )
        
        # Serve the file
        if report.file and report.file.path:
            response = FileResponse(
                open(report.file.path, 'rb'),
                content_type='application/pdf'
            )
            response['Content-Disposition'] = f'attachment; filename="{report.slug}.pdf"'
            return response
        
        raise Http404("File not found")
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured reports"""
        featured = self.get_queryset().filter(is_featured=True)[:6]
        serializer = ReportListSerializer(featured, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def bestsellers(self, request):
        """Get bestseller reports"""
        bestsellers = self.get_queryset().filter(is_bestseller=True)[:6]
        serializer = ReportListSerializer(bestsellers, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def free(self, request):
        """Get free reports"""
        free_reports = self.get_queryset().filter(is_free=True)[:12]
        serializer = ReportListSerializer(free_reports, many=True)
        return Response(serializer.data)


class ReportPurchaseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for ReportPurchase model.
    Users can view their own purchases.
    """
    
    serializer_class = ReportPurchaseSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination
    
    def get_queryset(self):
        """Users can only see their own purchases"""
        return ReportPurchase.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def create_purchase(self, request):
        """Create a new report purchase"""
        serializer = CreateReportPurchaseSerializer(
            data=request.data,
            context={'user': request.user}
        )
        serializer.is_valid(raise_exception=True)
        
        report_id = serializer.validated_data['report_id']
        report = Report.objects.get(id=report_id)
        
        purchase = ReportPurchase.objects.create(
            user=request.user,
            report=report,
            amount_paid=report.price,
            payment_method=serializer.validated_data.get('payment_method', ''),
            transaction_reference=serializer.validated_data.get('transaction_reference', ''),
        )
        
        # Return purchase data
        purchase_serializer = ReportPurchaseSerializer(purchase)
        return Response(purchase_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def record_download(self, request, pk=None):
        """Record a download for a purchased report"""
        purchase = self.get_object()
        purchase.record_download()
        return Response({'message': 'Download recorded', 'download_count': purchase.download_count})


class ReportBundleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for ReportBundle model.
    Read-only for public users.
    """
    
    queryset = ReportBundle.objects.filter(is_deleted=False, status='published')
    serializer_class = ReportBundleListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'description']
    filterset_fields = ['is_featured']
    ordering = ['-is_featured', '-created_at']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ReportBundleDetailSerializer
        return ReportBundleListSerializer
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured bundles"""
        featured = self.get_queryset().filter(is_featured=True)[:3]
        serializer = ReportBundleListSerializer(featured, many=True)
        return Response(serializer.data)


class ReportReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for ReportReview model.
    """
    
    serializer_class = ReportReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['report', 'rating', 'is_approved']
    ordering_fields = ['rating', 'created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Only show approved reviews to non-admin users"""
        queryset = ReportReview.objects.all()
        
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_approved=True)
        
        return queryset
    
    @action(detail=False, methods=['post'])
    def create_review(self, request):
        """Create a new review for a report"""
        serializer = CreateReportReviewSerializer(
            data=request.data,
            context={'user': request.user}
        )
        serializer.is_valid(raise_exception=True)
        
        report = Report.objects.get(id=serializer.validated_data['report_id'])
        
        review = ReportReview.objects.create(
            report=report,
            user=request.user,
            rating=serializer.validated_data['rating'],
            title=serializer.validated_data['title'],
            content=serializer.validated_data['content'],
            is_verified_purchase=ReportPurchase.objects.filter(
                user=request.user, report=report, is_paid=True
            ).exists()
        )
        
        # Auto-approve reviews from verified purchases or staff
        if review.is_verified_purchase or request.user.is_staff:
            review.approve()
        
        review_serializer = ReportReviewSerializer(review)
        return Response(review_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def mark_helpful(self, request, pk=None):
        """Mark a review as helpful"""
        review = self.get_object()
        review.helpful_count += 1
        review.save(update_fields=['helpful_count'])
        return Response({'helpful_count': review.helpful_count})