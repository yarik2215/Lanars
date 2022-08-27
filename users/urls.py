
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from django.urls import path
from users.views import RegisterView, ChangePasswordView, ProfileView


urlpatterns = [
    path('profile/', ProfileView.as_view(), name="profile"),
    path('register/', RegisterView.as_view(), name='register'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]