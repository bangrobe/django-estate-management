from django import forms
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserChangeForm(BaseUserChangeForm):

    class Meta(BaseUserChangeForm.Meta):
        model = User
        fields = ['first_name','last_name','username','email']


class UserCreationForm(admin_forms.UserCreationForm):

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = ['first_name','last_name','username','email']
    
    error_messages = {
        'duplicate_username': _('A user with that username already exists.'),
        'duplicate_email': _('A user with that email already exists.'),
        'password_mismatch': _('The two password fields didn’t match.'),
    }

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                self.error_messages['duplicate_email'],
                code='duplicate_email',
            )
        return email
        # try:
        #     User.objects.get(email=email)
        # except User.DoesNotExist:
        #     return email
        # raise forms.ValidationError(
        #     self.error_messages['duplicate_email'],
        #     code='duplicate_email',
        # )
    
    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                self.error_messages['duplicate_username'],
                code='duplicate_username',
            )
        return username