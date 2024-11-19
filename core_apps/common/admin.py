from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import ContentView
# Register your models here.

@admin.register(ContentView)
class ContentViewAdmin(admin.ModelAdmin):
    list_display = ["user", "content_object","viewer_ip","created_at","last_viewed"]
   

class ContentViewInline(GenericTabularInline):
    model = ContentView
    extra = 0
    readonly_fields = ["user","viewer_ip","created_at"]