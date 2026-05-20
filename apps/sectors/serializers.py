from rest_framework import serializers
from .models import Sector


class SectorSerializer(serializers.ModelSerializer):
    """Serializer for Sector model"""
    
    status_display = serializers.ReadOnlyField(source='get_status_display')
    
    class Meta:
        model = Sector
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'icon',
            'color',
            'featured_image',
            'order',
            'business_count',
            'status',
            'status_display',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'slug', 'business_count', 'created_at', 'updated_at']


class SectorListSerializer(serializers.ModelSerializer):
    """Minimal serializer for list views"""
    
    class Meta:
        model = Sector
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'icon',
            'color',
            'business_count',
        ]


class SectorDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for single sector view"""
    
    status_display = serializers.ReadOnlyField(source='get_status_display')
    
    class Meta:
        model = Sector
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'icon',
            'color',
            'featured_image',
            'order',
            'business_count',
            'status',
            'status_display',
            'created_at',
            'updated_at',
        ]