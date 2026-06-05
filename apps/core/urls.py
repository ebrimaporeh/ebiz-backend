# apps/core/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'sources', views.SourceViewSet, basename='source')
router.register(r'ratings', views.RatingValueViewSet, basename='rating')
router.register(r'api-keys', views.APIKeyViewSet, basename='api-key')
router.register(r'countries', views.CountryViewSet, basename='country')
router.register(r'regions', views.RegionViewSet, basename='region')

urlpatterns = [
    path('', include(router.urls)),
]