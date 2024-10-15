from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import UserChangeForm, UserCreationForm
# Register your models here.

User = get_user_model()

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        (_('Login Credentials'), {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'username')}),
        (_('Permissions and Groups'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name','last_name','password1', 'password2'),
        }),
    )
    list_display = ('pkid', 'id', 'username', 'first_name', 'last_name', 'email', 'is_superuser')
    list_display_links = ('pkid', 'id', 'email',  'username')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('pkid',)