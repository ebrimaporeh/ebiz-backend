"""
apps/sectors/serializers.py

Serializers for Sector taxonomy models.
"""

from rest_framework import serializers
from .models import Sector, SectorTag, SectorStat
from apps.core.constants import Country as CountryChoice, Region as RegionChoice, CURRENCY_SYMBOLS, COUNTRY_FLAGS
from apps.core.models import Source


# ============================================
# SECTOR TAG SERIALIZER
# ============================================

class SectorTagSerializer(serializers.ModelSerializer):
    """Serializer for SectorTag"""
    
    class Meta:
        model = SectorTag
        fields = ['id', 'label', 'slug', 'description']
        read_only_fields = ['id', 'slug']


# ============================================
# SECTOR STAT SERIALIZER
# ============================================

# apps/sectors/serializers.py - Simpler version

class SectorStatSerializer(serializers.ModelSerializer):
    """Serializer for SectorStat with country/region"""
    
    display_value = serializers.ReadOnlyField()
    unit_display = serializers.SerializerMethodField()
    country_display = serializers.SerializerMethodField()
    region_display = serializers.SerializerMethodField()
    
    # Use SlugRelatedField to accept UUID strings
    sector = serializers.SlugRelatedField(
        slug_field='id',
        queryset=Sector.objects.all(),
        required=True
    )
    source = serializers.SlugRelatedField(
        slug_field='id',
        queryset=Source.objects.all(),
        required=True
    )
    
    class Meta:
        model = SectorStat
        fields = [
            'id', 'label', 'value', 'unit', 'unit_display',
            'display_value', 'display_order', 'is_headline',
            'year', 'country', 'country_display', 'region',
            'region_display', 'sector', 'source', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_unit_display(self, obj):
        return obj.get_unit_display()
    
    def get_country_display(self, obj):
        if obj.country:
            return dict(CountryChoice.choices).get(obj.country, obj.country)
        return None
    
    def get_region_display(self, obj):
        if obj.region:
            return dict(RegionChoice.choices).get(obj.region, obj.region)
        return None

# class SectorStatSerializer(serializers.ModelSerializer):
#     """Serializer for SectorStat with country/region"""
    
#     display_value = serializers.ReadOnlyField()
#     unit_display = serializers.SerializerMethodField()
#     country_display = serializers.SerializerMethodField()
#     region_display = serializers.SerializerMethodField()

#     sector = serializers.SlugRelatedField(
#         slug_field='id',
#         queryset=Sector.objects.all(),
#         required=True
#     )
#     source = serializers.SlugRelatedField(
#         slug_field='id',
#         queryset=Source.objects.all(),
#         required=True
#     )
    
#     class Meta:
#         model = SectorStat
#         fields = [
#             'id', 'label', 'value', 'unit', 'unit_display',
#             'display_value', 'display_order', 'is_headline',
#             'year', 'country', 'country_display', 'region',
#             'region_display', 'source', 'created_at', 'updated_at'
#         ]
#         read_only_fields = ['id', 'created_at', 'updated_at']
    
#     def get_unit_display(self, obj):
#         return obj.get_unit_display()
    
#     def get_country_display(self, obj):
#         if obj.country:
#             return dict(CountryChoice.choices).get(obj.country, obj.country)
#         return None
    
#     def get_region_display(self, obj):
#         if obj.region:
#             return dict(RegionChoice.choices).get(obj.region, obj.region)
#         return None


# ============================================
# SECTOR LIST SERIALIZER
# ============================================

class SectorListSerializer(serializers.ModelSerializer):
    """Minimal serializer for sector list views"""
    
    country_display = serializers.SerializerMethodField()
    currency_symbol = serializers.SerializerMethodField()
    flag_emoji = serializers.SerializerMethodField()
    
    class Meta:
        model = Sector
        fields = [
            'id', 'name', 'slug', 'description', 'icon',
            'color', 'business_count', 'order', 'country',
            'country_display', 'flag_emoji', 'currency', 'currency_symbol'
        ]
    
    def get_country_display(self, obj):
        return dict(CountryChoice.choices).get(obj.country, obj.country)
    
    def get_currency_symbol(self, obj):
        return CURRENCY_SYMBOLS.get(obj.currency, "D")
    
    def get_flag_emoji(self, obj):
        return COUNTRY_FLAGS.get(obj.country, "")


# ============================================
# SECTOR DETAIL SERIALIZER
# ============================================

class SectorDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for single sector view"""
    
    status_display = serializers.ReadOnlyField(source='get_status_display')
    is_top_level = serializers.ReadOnlyField()
    full_name = serializers.ReadOnlyField()
    children = serializers.SerializerMethodField()
    stats = SectorStatSerializer(many=True, read_only=True)
    tags = serializers.SerializerMethodField()
    country_display = serializers.SerializerMethodField()
    region_display = serializers.SerializerMethodField()
    currency_symbol = serializers.SerializerMethodField()
    flag_emoji = serializers.SerializerMethodField()
    
    class Meta:
        model = Sector
        fields = [
            'id', 'name', 'slug', 'description', 'icon', 'color',
            'featured_image', 'parent', 'order', 'business_count',
            'status', 'status_display', 'summary_for_ai',
            'country', 'country_display', 'flag_emoji', 'region', 'region_display',
            'currency', 'currency_symbol', 'estimated_market_size',
            'estimated_market_size_display', 'is_top_level', 'full_name',
            'children', 'stats', 'tags', 'created_at', 'updated_at'
        ]
    
    def get_children(self, obj):
        """Return child sectors (sub-sectors)"""
        children = obj.children.filter(status='published', is_deleted=False)
        return SectorListSerializer(children, many=True).data
    
    def get_tags(self, obj):
        """Return tags assigned to this sector"""
        tags = obj.tag_assignments.select_related('tag').all()
        return [{'id': t.tag.id, 'label': t.tag.label, 'slug': t.tag.slug} for t in tags]
    
    def get_country_display(self, obj):
        return dict(CountryChoice.choices).get(obj.country, obj.country)
    
    def get_region_display(self, obj):
        if obj.region:
            return dict(RegionChoice.choices).get(obj.region, obj.region)
        return None
    
    def get_currency_symbol(self, obj):
        return CURRENCY_SYMBOLS.get(obj.currency, "D")
    
    def get_flag_emoji(self, obj):
        return COUNTRY_FLAGS.get(obj.country, "")


# ============================================
# SECTOR SERIALIZER (CRUD)
# ============================================

class SectorSerializer(serializers.ModelSerializer):
    """Base serializer for CRUD operations"""
    
    status_display = serializers.ReadOnlyField(source='get_status_display')
    full_name = serializers.ReadOnlyField()
    country_display = serializers.SerializerMethodField()
    currency_symbol = serializers.SerializerMethodField()
    flag_emoji = serializers.SerializerMethodField()
    
    class Meta:
        model = Sector
        fields = [
            'id', 'name', 'slug', 'description', 'icon', 'color',
            'featured_image', 'parent', 'order', 'business_count',
            'status', 'status_display', 'summary_for_ai',
            'country', 'country_display', 'flag_emoji', 'region', 'currency',
            'currency_symbol', 'estimated_market_size',
            'estimated_market_size_display', 'full_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'slug', 'business_count', 'created_at', 'updated_at']
    
    def get_country_display(self, obj):
        return dict(CountryChoice.choices).get(obj.country, obj.country)
    
    def get_currency_symbol(self, obj):
        return CURRENCY_SYMBOLS.get(obj.currency, "D")
    
    def get_flag_emoji(self, obj):
        return COUNTRY_FLAGS.get(obj.country, "")