# apps/sectors/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'sectors', views.SectorViewSet, basename='sector')
router.register(r'sector-tags', views.SectorTagViewSet, basename='sector-tag')
router.register(r'sector-stats', views.SectorStatViewSet, basename='sector-stat')

urlpatterns = [
    path('', include(router.urls)),
]