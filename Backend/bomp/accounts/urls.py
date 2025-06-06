from django.urls import path
from .views import UserRegistrationAPIView, LogoutAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'accounts'  # Optional: Add app_name for namespacing

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user_register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # Using 'login/' as specified
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # Default path for refresh
    path('logout/', LogoutAPIView.as_view(), name='user_logout'),
]
