from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from core_apps.common.models import TimeStampedModel
# Create your models here.

User = get_user_model()

class Apartment(TimeStampedModel):
    unit_number = models.CharField(_("Unit Number"), max_length=100, unique=True)
    building = models.CharField(_("Building"), max_length=100)
    floor = models.PositiveIntegerField(_("Floor"))
    tenant = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Tenant"), related_name="apartment")

    def __str__(self):
        return f"{self.unit_number} - {self.building} - {self.floor}"