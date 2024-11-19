from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _

def validate_email_address(value):
    try:
        validate_email(value)
    except ValidationError:
        raise ValidationError(_('Enter a valid email address.'))
    

# UserManager

class UserManage(DjangoUserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The given email must be set'))
        if not username:
            raise ValueError(_('The given username must be set'))
        # Normalize the email
        email = self.normalize_email(email)
        validate_email_address(email)
        # Ky thuat kiem tra username bi trung
        global_user_modal = apps.get_model(self.model._meta.app_label, self.model._meta.object_name)
        username = global_user_modal.normalize_username(username)

        # Create the user
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)


    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self._create_user(username, email, password, **extra_fields)  