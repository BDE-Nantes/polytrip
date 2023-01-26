import uuid

from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

from colorfield.fields import ColorField


class School(models.Model):
    uuid = models.UUIDField(_("Uuid"), help_text=_("Unique identifier (UUID4)"), default=uuid.uuid4)
    name = models.CharField(_("School name"), max_length=255, unique=True)
    color = ColorField(_("School color"))
    coordinates = models.PointField(_("School coordinates"))

    class Meta:
        ordering = ["name"]
        verbose_name = _("School")
        verbose_name_plural = _("Schools")

    def __str__(self) -> str:
        return self.name
