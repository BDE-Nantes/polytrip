from datetime import timedelta

from django.db import models
from django.forms import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from solo.models import SingletonModel


def get_default_end_date():
    return timezone.now() + timedelta(days=2)


class SiteConfiguration(SingletonModel):
    start_date = models.DateTimeField(
        _("Start date"), help_text=_("Start date of the Polytrip event"), default=timezone.now
    )
    end_date = models.DateTimeField(
        _("End date"), help_text=_("End date of the Polytrip event"), default=get_default_end_date
    )

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError({"start_date": _("Start date can't be after end date.")}, code="invalid_start_date")
        super().clean()

    def save(self, *args, **kwargs):
        if self.start_date >= self.end_date:
            return
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Site configuration")

    def __str__(self) -> str:
        return "Site configuration"
