from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from solo.models import SingletonModel


class SiteConfiguration(SingletonModel):
    start_date = models.DateTimeField(
        _("Start date"), help_text=_("Start date of the Polytrip event"), default=timezone.now
    )

    class Meta:
        verbose_name = _("Site configuration")

    def __str__(self) -> str:
        return "Site configuration"
