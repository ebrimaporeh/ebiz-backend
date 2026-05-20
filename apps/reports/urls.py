from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'reports', views.ReportViewSet, basename='report')
router.register(r'purchases', views.ReportPurchaseViewSet, basename='purchase')
router.register(r'bundles', views.ReportBundleViewSet, basename='bundle')
router.register(r'reviews', views.ReportReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
]