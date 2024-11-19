import uuid
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.db import IntegrityError
User = get_user_model()
# Create your models here.

class TimeStampedModel(models.Model):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at", "-updated_at"]

class ContentView(TimeStampedModel):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name=_("Content Type"))
    object_id = models.PositiveIntegerField(_("Object ID"))
    content_object = GenericForeignKey("content_type", "object_id")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name=_("User"), related_name="content_view", null=True,blank=True)

    viewer_ip = models.GenericIPAddressField(_("Viewer IP"), null=True, blank=True)
    last_viewed = models.DateTimeField(_("Last Viewed"))

    class Meta:
        verbose_name = _("Content View")
        verbose_name_plural = _("Content Views")
        unique_together = ["content_type", "object_id", "user", "viewer_ip"]
        ordering = ["-last_viewed"]
    
    def __str__(self):
        return f"{self.user.get_full_name if self.user else "Anonymous"} viewed {self.content_object} from {self.viewer_ip}"
    
    @classmethod
    def record_view(cls, content_object, user, viewed_ip):
        ct = ContentType.objects.get_for_model(content_object)
        try:
            view, created = cls.objects.get_or_create(content_type=ct, object_id=content_object.pkid, defaults={"user": user, "viewer_ip": viewed_ip})
            if not created:
                pass
        except IntegrityError:
            return