"""
URL configuration for users app.
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'users'

urlpatterns = [
    # Authentication
    path('register/', views.UserRegistrationAPIView.as_view(), name='register'),
    path('login/', views.CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    
    # User management
    path('me/', views.UserMeAPIView.as_view(), name='user-me'),
    path('change-password/', views.UserChangePasswordAPIView.as_view(), name='change-password'),
    path('list/', views.UserListView.as_view(), name='user-list'),
]
