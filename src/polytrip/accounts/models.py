from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

from polytrip.schools.models import School


class User(AbstractUser):
    is_team = models.BooleanField(_("Is a team"), default=False)
    school = models.ForeignKey(School, verbose_name=_("School"), on_delete=models.SET_NULL, null=True)

    def clean(self):
        if not self.is_team and self.school is not None:
            raise ValidationError(
                {
                    "school": _("User can't be linked to a school if it is not a team."),
                },
                code="invalid_school",
            )
        if self.is_team and self.school is None:
            raise ValidationError(
                {"is_team": _("A user that is not a team can't be linked to a school.")}, code="invalid_is_team"
            )
        super().clean()

    def save(self, *args, **kwargs):
        if not self.is_team and self.school is not None or self.is_team and self.school is None:
            return
        super().save(*args, **kwargs)
