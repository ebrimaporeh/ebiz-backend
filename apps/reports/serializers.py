from rest_framework import serializers
from .models import Report, ReportPurchase, ReportBundle, ReportReview
from apps.sectors.serializers import SectorListSerializer
from apps.businesses.serializers import BusinessListSerializer


class ReportListSerializer(serializers.ModelSerializer):
    """Minimal serializer for report list views"""
    
    price_display = serializers.ReadOnlyField()
    file_size_display = serializers.ReadOnlyField()
    sector_name = serializers.ReadOnlyField(source='sector.name')
    
    class Meta:
        model = Report
        fields = [
            'id', 'title', 'slug', 'subtitle', 'short_description',
            'cover_image', 'report_type', 'format', 'price', 'price_display',
            'is_free', 'is_featured', 'is_bestseller', 'download_count',
            'rating', 'review_count', 'file_size_display', 'sector_name',
            'published_at'
        ]


class ReportDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for single report view"""
    
    price_display = serializers.ReadOnlyField()
    file_size_display = serializers.ReadOnlyField()
    sector = SectorListSerializer(read_only=True)
    business = BusinessListSerializer(read_only=True)
    has_user_purchased = serializers.SerializerMethodField()
    
    class Meta:
        model = Report
        fields = [
            'id', 'title', 'slug', 'subtitle', 'description', 'short_description',
            'cover_image', 'file', 'file_size', 'file_size_display',
            'report_type', 'format', 'sector', 'business',
            'table_of_contents', 'key_highlights', 'price', 'price_display',
            'is_free', 'is_featured', 'is_bestseller', 'page_count',
            'version', 'author', 'published_at', 'download_count',
            'view_count', 'rating', 'review_count', 'meta_title',
            'meta_description', 'has_user_purchased'
        ]
    
    def get_has_user_purchased(self, obj):
        """Check if requesting user has purchased this report"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return ReportPurchase.objects.filter(
                user=request.user, 
                report=obj,
                is_paid=True
            ).exists()
        return False


class ReportSerializer(serializers.ModelSerializer):
    """Base serializer for CRUD operations"""
    
    class Meta:
        model = Report
        fields = '__all__'


class ReportPurchaseSerializer(serializers.ModelSerializer):
    """Serializer for report purchases"""
    
    report_title = serializers.ReadOnlyField(source='report.title')
    user_email = serializers.ReadOnlyField(source='user.email')
    amount_paid_display = serializers.SerializerMethodField()
    
    class Meta:
        model = ReportPurchase
        fields = [
            'id', 'user', 'user_email', 'report', 'report_title',
            'amount_paid', 'amount_paid_display', 'payment_method',
            'transaction_reference', 'is_paid', 'paid_at',
            'has_downloaded', 'download_count', 'last_downloaded_at',
            'is_bundle', 'bundle_reference'
        ]
        read_only_fields = ['id', 'paid_at', 'has_downloaded', 'download_count', 'last_downloaded_at']
    
    def get_amount_paid_display(self, obj):
        return f"D{obj.amount_paid:,}"


class CreateReportPurchaseSerializer(serializers.Serializer):
    """Serializer for creating a new report purchase"""
    
    report_id = serializers.IntegerField(required=True)
    payment_method = serializers.CharField(max_length=50, required=False, allow_blank=True)
    transaction_reference = serializers.CharField(max_length=200, required=False, allow_blank=True)
    
    def validate_report_id(self, value):
        """Validate report exists and is not free"""
        try:
            report = Report.objects.get(id=value, status='published')
            if report.is_free:
                raise serializers.ValidationError("This report is free. No purchase needed.")
            return value
        except Report.DoesNotExist:
            raise serializers.ValidationError("Report not found")
    
    def validate(self, attrs):
        """Check if user already purchased this report"""
        user = self.context.get('user')
        report_id = attrs.get('report_id')
        
        if user and report_id:
            if ReportPurchase.objects.filter(user=user, report_id=report_id).exists():
                raise serializers.ValidationError({
                    'report_id': 'You have already purchased this report'
                })
        
        return attrs


class ReportBundleListSerializer(serializers.ModelSerializer):
    """Serializer for report bundle list views"""
    
    price_display = serializers.ReadOnlyField()
    original_price_display = serializers.ReadOnlyField()
    savings_display = serializers.ReadOnlyField()
    
    class Meta:
        model = ReportBundle
        fields = [
            'id', 'name', 'slug', 'description', 'cover_image',
            'price', 'price_display', 'original_price', 'original_price_display',
            'discount_percent', 'savings_display', 'is_featured',
            'purchase_count', 'valid_until'
        ]


class ReportBundleDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for single bundle view"""
    
    price_display = serializers.ReadOnlyField()
    original_price_display = serializers.ReadOnlyField()
    savings_display = serializers.ReadOnlyField()
    reports = ReportListSerializer(many=True, read_only=True)
    
    class Meta:
        model = ReportBundle
        fields = [
            'id', 'name', 'slug', 'description', 'cover_image',
            'reports', 'price', 'price_display', 'original_price',
            'original_price_display', 'discount_percent', 'savings_display',
            'is_featured', 'purchase_count', 'valid_until'
        ]


class ReportReviewSerializer(serializers.ModelSerializer):
    """Serializer for report reviews"""
    
    user_name = serializers.ReadOnlyField(source='user.email')
    
    class Meta:
        model = ReportReview
        fields = [
            'id', 'report', 'user', 'user_name', 'rating',
            'title', 'content', 'is_verified_purchase',
            'is_approved', 'helpful_count', 'created_at'
        ]
        read_only_fields = ['id', 'is_approved', 'helpful_count', 'created_at']


class CreateReportReviewSerializer(serializers.Serializer):
    """Serializer for creating a new review"""
    
    report_id = serializers.IntegerField(required=True)
    rating = serializers.IntegerField(min_value=1, max_value=5, required=True)
    title = serializers.CharField(max_length=200, required=True)
    content = serializers.CharField(required=True)
    
    def validate_report_id(self, value):
        try:
            report = Report.objects.get(id=value, status='published')
            return value
        except Report.DoesNotExist:
            raise serializers.ValidationError("Report not found")
    
    def validate(self, attrs):
        """Check if user has purchased this report"""
        user = self.context.get('user')
        report_id = attrs.get('report_id')
        
        if user and report_id:
            has_purchased = ReportPurchase.objects.filter(
                user=user, report_id=report_id, is_paid=True
            ).exists()
            
            if not has_purchased:
                raise serializers.ValidationError({
                    'report_id': 'You must purchase this report before reviewing it'
                })
            
            # Check if user already reviewed
            already_reviewed = ReportReview.objects.filter(
                user=user, report_id=report_id
            ).exists()
            
            if already_reviewed:
                raise serializers.ValidationError({
                    'report_id': 'You have already reviewed this report'
                })
        
        return attrs