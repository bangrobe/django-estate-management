from django.db import models
from autoslug  import AutoSlugField
from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from core_apps.common.models import TimeStampedModel
User = get_user_model()
# Create your models here.
def get_user_username(instance: "Profile") -> str:
    return instance.user.username


class Profile(TimeStampedModel):
    class Gender(models.TextChoices):
        MALE = "M", _("Male")
        FEMALE = "F", _("Female")
        OTHER = "O", _("Other")
    
    class Occupation(models.TextChoices):
        STUDENT = "student", _("Student")
        EMPLOYED = "employed", _("Employed")
        UNEMPLOYED = "unemployed", _("Unemployed")
        RETIRED = "retired", _("Retired")
        TENANT = "tenant", _("Tenant")
        FREELANCER = "freelancer", _("Freelancer")
        OTHER = "other", _("Other")

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("User"), related_name="profile")
    gender = models.CharField(_("Gender"), max_length=1, choices=Gender.choices, blank=True)
    occupation = models.CharField(_("Occupation"), max_length=100, choices=Occupation.choices, blank=True, default=Occupation.TENANT)
    avatar = CloudinaryField(_("Avatar"), null=True, blank=True)
    first_name = models.CharField(_("First Name"), max_length=100)
    bio = models.TextField(_("Bio"), blank=True)
    phone_number = PhoneNumberField(_("Phone Number"), blank=True)
    country_of_origin = CountryField(_("Country"), blank=True, default="VN")
    city_of_origin = models.CharField(_("City"), max_length=100, blank=True)
    report_count = models.PositiveIntegerField(_("Report Count"), default=0)
    reputation = models.IntegerField(_("Reputation"), default=100)
    slug = AutoSlugField(populate_from=get_user_username, unique=True)

    @property
    def is_banned(self)->bool:
        return self.report_count >= 5
    
    def update_reputation(self):
        self.reputation = max(0, 100 - self.report_count * 10)
    
    def save(self, *args, **kwargs):
        self.update_reputation()
        super().save(*args, **kwargs)