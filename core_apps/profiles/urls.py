from django.urls import path
from .views import (
    ProfileListAPIView,
    ProfileDetailAPIView,
    UpdateProfileAPIView,
    AvatarUploadAPIView,    
    NonTenantProfileListAPIView 
)

urlpatterns = [
    path("all/", ProfileListAPIView.as_view(), name="profiles_list"),
    path("user/my-profile/", ProfileDetailAPIView.as_view(), name="profile_detail"),
    path("user/my-profile/<int:pk>/update/", UpdateProfileAPIView.as_view(), name="profile_update"),
    path("user/my-profile/<int:pk>/avatar/", AvatarUploadAPIView.as_view(), name="avatar_upload"),
    path("non-tenant/", NonTenantProfileListAPIView.as_view(), name="non_tenant_profiles_list"),
]