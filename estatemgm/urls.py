
from django.contrib import admin
from django.urls import path
from django.contrib import admin
from django.conf import settings
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="Estate Management API",
        default_version='v1',
        description="Estate Management API",
        contact=openapi.Contact(email="vVqXf@example.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

admin.site.site_header = "Estate Management"
admin.site.site_title = "Estate Management"
admin.site.index_title = "Estate Management"