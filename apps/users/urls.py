from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# ============================================
# ROUTER SETUP
# ============================================

router = DefaultRouter()
router.register(r'subscriptions', views.SubscriptionViewSet, basename='subscription')
router.register(r'purchases', views.OneTimePurchaseViewSet, basename='purchase')

# ============================================
# URL PATTERNS
# ============================================

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('auth/logout/', views.LogoutView.as_view(), name='logout'),
    path('auth/me/', views.MeView.as_view(), name='me'),
    path('auth/change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('auth/forgot-password/', views.ForgotPasswordView.as_view(), name='forgot-password'),
    path('auth/reset-password/', views.ResetPasswordView.as_view(), name='reset-password'),
    
    # User profile endpoints
    path('users/profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('users/preferences/', views.UserPreferencesView.as_view(), name='user-preferences'),
    path('users/public/<int:id>/', views.PublicUserView.as_view(), name='public-user'),
    
    # Router endpoints
    path('', include(router.urls)),
]