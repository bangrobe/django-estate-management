import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.utils.translation import gettext_lazy as _
from core_apps.users.managers import UserManage

# Create your models here.
class UsernameValidator(validators.RegexValidator):
    regex = r'^[\w.@+-]+\Z'
    message = _(
        'Enter a valid username. This value may contain only letters, '
        'numbers, and @/./+/-/_ characters.'
    )
    flags = 0


class User(AbstractUser):
    #Pseudo Primary Key, using for sorting
    pkid = models.BigAutoField(primary_key=True, editable=False)
    # Using UUID as primary key
    id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'), unique=True, db_index=True)
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[UsernameValidator()],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    
    first_name = models.CharField(_('First Name'), max_length=150, blank=True)
    last_name = models.CharField(_('Last Name'), max_length=150, blank=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    #Cac field yeu cau khi tao super user
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    # Override the default manager
    objects = UserManage()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ('-date_joined',)

    @property
    # Khi dung property thi se goi la user.get_full_name chu ko phai la method user.get_full_name()
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'.strip()