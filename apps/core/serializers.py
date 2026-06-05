"""
apps/core/serializers.py

Serializers for core models (Country, Region, Source, RatingValue, APIKey).
"""

from rest_framework import serializers
from .models import Source, RatingValue, APIKey, Country, Region
from .constants import CURRENCY_SYMBOLS, COUNTRY_FLAGS


# ============================================
# COUNTRY SERIALIZER
# ============================================

class CountrySerializer(serializers.ModelSerializer):
    """Serializer for Country model."""
    
    display_name = serializers.ReadOnlyField()
    currency_symbol_display = serializers.SerializerMethodField()
    flag = serializers.ReadOnlyField(source='flag_emoji')
    
    class Meta:
        model = Country
        fields = [
            'id', 'code', 'name', 'flag_emoji', 'flag', 'display_name',
            'currency', 'currency_symbol', 'currency_symbol_display',
            'population', 'gdp_per_capita_usd', 'is_active', 'order',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_currency_symbol_display(self, obj):
        return CURRENCY_SYMBOLS.get(obj.currency, obj.currency)


class CountryListSerializer(serializers.ModelSerializer):
    """Minimal serializer for country list views."""
    
    display_name = serializers.ReadOnlyField()
    
    class Meta:
        model = Country
        fields = ['id', 'code', 'name', 'flag_emoji', 'display_name', 'is_active', 'order']


# ============================================
# REGION SERIALIZER
# ============================================

class RegionSerializer(serializers.ModelSerializer):
    """Serializer for Region model."""
    
    country_count = serializers.ReadOnlyField()
    countries = CountryListSerializer(many=True, read_only=True)
    country_codes = serializers.SlugRelatedField(
        source='countries',
        many=True,
        read_only=True,
        slug_field='code'
    )
    
    class Meta:
        model = Region
        fields = [
            'id', 'name', 'slug', 'description', 'countries',
            'country_codes', 'country_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']


class RegionListSerializer(serializers.ModelSerializer):
    """Minimal serializer for region list views."""
    
    country_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Region
        fields = ['id', 'name', 'slug', 'description', 'country_count']


# ============================================
# SOURCE SERIALIZER
# ============================================

class SourceSerializer(serializers.ModelSerializer):
    """Serializer for Source model."""
    
    source_type_display = serializers.ReadOnlyField(source='get_source_type_display')
    
    class Meta:
        model = Source
        fields = [
            'id', 'name', 'reference', 'url', 'publication_date',
            'year', 'source_type', 'source_type_display',
            'confidence_rating', 'is_primary_source', 'notes',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


# ============================================
# RATING VALUE SERIALIZER
# ============================================

class RatingValueSerializer(serializers.ModelSerializer):
    """Serializer for RatingValue model."""
    
    source_name = serializers.ReadOnlyField(source='source.name')
    normalized_100 = serializers.ReadOnlyField()
    
    class Meta:
        model = RatingValue
        fields = [
            'id', 'value', 'year', 'source', 'source_name',
            'confidence_score', 'notes', 'normalized_100',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


# ============================================
# API KEY SERIALIZER
# ============================================

class APIKeySerializer(serializers.ModelSerializer):
    """Serializer for APIKey model (read-only for non-admin)."""
    
    tier_display = serializers.ReadOnlyField(source='get_tier_display')
    
    class Meta:
        model = APIKey
        fields = [
            'id', 'organization', 'tier', 'tier_display',
            'is_active', 'expires_at', 'created_at'
        ]
        read_only_fields = ['id', 'key', 'created_at', 'last_used']


class APIKeyCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating API keys (returns the key)."""
    
    class Meta:
        model = APIKey
        fields = ['organization', 'tier', 'contact_name', 'contact_email', 'expires_at']
    
    def create(self, validated_data):
        return APIKey.objects.create(**validated_data)