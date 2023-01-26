import uuid

from django.conf import settings
from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _


class Trip(models.Model):
    uuid = models.UUIDField(_("Uuid"), help_text=_("Unique identifier (UUID4)"), default=uuid.uuid4)
    team = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={"is_team": True})
    trip = models.LineStringField(_("Trip"), geography=True)

    class Meta:
        ordering = ["team"]
        verbose_name = _("Trip")
        verbose_name_plural = _("Trips")

    def __str__(self) -> str:
        return str(self.team)
