from typing import List
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from core_apps.common.renderers import GenericJsonRenderer
from core_apps.profiles.models import Profile
from core_apps.profiles.serializers import (
    AvatarUploadSerializer,
    ProfileSerializer,
    UpdateProfileSerializer
)
from .tasks import upload_avatar_to_cloudinary

User = get_user_model()
# Create your views here.

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProfileListAPIView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    pagination_class = StandardResultsSetPagination
    renderer_classes = (GenericJsonRenderer,)
    object_label = "profiles"
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("user__username", "user__first_name", "user__last_name")
    filterset_fields = ("occupation", "gender", "country_of_origin", "city_of_origin")

    def get_queryset(self)->List[Profile]:
        tenant = Profile.Occupation.TENANT
        result = Profile.objects.exclude(user__is_staff=True).exclude(user__is_superuser=True).filter(occupation=tenant) #Loai bo staff,superuser
        return result

class ProfileDetailAPIView(generics.RetrieveAPIView):

    serializer_class = ProfileSerializer
    renderer_classes = (GenericJsonRenderer,)
    object_label = "profile"
    
    def get_queryset(self):
        result = Profile.objects.select_related("user").all()
        return result

    def get_object(self):
        try:
            return Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            raise Http404

class UpdateProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UpdateProfileSerializer
    renderer_classes = (GenericJsonRenderer,)
    object_label = "profile"
    
    def get_queryset(self):
        return Profile.objects.none()

    def get_object(self):
        profile,_ = Profile.objects.get_or_create(user=self.request.user)
        return profile
    def perform_update(self, serializer: UpdateProfileSerializer):
        user_data = serializer.validated_data.pop("user", {})
        profile = serializer.save()
        User.objects.filter(id=self.request.user.id).update(**user_data)
        return profile

class AvatarUploadAPIView(APIView):
    renderer_classes = (GenericJsonRenderer,)
    object_label = "profile"

    def patch(self, request, *args, **kwargs):
        return self.upload_avatar(request, *args, **kwargs)
    def upload_avatar(self, request, *args, **kwargs):
        profile = request.user.profile
        serializer = AvatarUploadSerializer(profile, data=request.data)
        if serializer.is_valid():
            image = serializer.validated_data["avatar"]
            image_content = image.read()
            upload_avatar_to_cloudinary(str(profile.id), image_content)
            
            return Response({
                "message": "Avatar uploaded started"
            }, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NonTenantProfileListAPIView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    renderer_classes = (GenericJsonRenderer,)
    pagination_class = StandardResultsSetPagination
    object_label = "non_tenant_profiles"

    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("user__username", "user__first_name", "user__last_name")
    filterset_fields = ("occupation", "gender", "country_of_origin", "city_of_origin")

    def get_queryset(self)->List[Profile]:
        tenant = Profile.Occupation.TENANT
        result = Profile.objects.exclude(user__is_staff=True).exclude(user__is_superuser=True).exclude(occupation=tenant)
        return result