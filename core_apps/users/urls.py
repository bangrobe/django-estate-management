from django.urls import path, re_path

from .views import (CustomObtainPairView, CustomProviderAuthViewView, CustomTokenRefreshView, LogoutAPIView)

urlpatterns = [
    re_path(r'^provider/auth/$', CustomProviderAuthViewView.as_view(), name='provider_auth'),
    path("login/", CustomObtainPairView.as_view(), name="login"),
    path("refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
]