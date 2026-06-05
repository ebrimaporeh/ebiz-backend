# apps/businesses/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'businesses', views.BusinessViewSet, basename='business')
router.register(r'business-scales', views.BusinessScaleViewSet, basename='business-scale')
router.register(r'business-profiles', views.BusinessProfileViewSet, basename='business-profile')
router.register(r'business-features', views.BusinessProfileFeatureViewSet, basename='business-feature')
router.register(r'business-testimonials', views.BusinessProfileTestimonialViewSet, basename='business-testimonial')
# Register IntelligenceSnapshot ViewSet
router.register(r'intelligence', views.IntelligenceSnapshotViewSet, basename='intelligence')

urlpatterns = [
    path('', include(router.urls)),
]