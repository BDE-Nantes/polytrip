from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

from polytrip.schools.models import School


class User(AbstractUser):
    is_team = models.BooleanField(_("Is a team"), default=False)
    team_name = models.CharField(_("Team name"), max_length=255, blank=True)
    school = models.ForeignKey(School, verbose_name=_("School"), on_delete=models.SET_NULL, null=True)

    def clean(self):
        if not self.is_team and self.school is not None:
            raise ValidationError(
                {
                    "school": _("User can't be linked to a school if it is not a team."),
                },
                code="invalid_school",
            )
        if self.is_team:
            errors = []
            if self.school is None:
                errors.append(
                    ValidationError(
                        {"is_team": _("A user that is a team must be linked to a school.")}, code="invalid_is_team"
                    )
                )
            if not self.team_name:
                errors.append(
                    ValidationError(
                        {"team_name": _("A team name must be provided if the user is a team.")},
                        code="invalid_team_name",
                    )
                )
            if errors:
                raise ValidationError(errors)
        super().clean()

    def save(self, *args, **kwargs):
        if not self.is_team and self.school is not None or self.is_team and self.school is None:
            return
        super().save(*args, **kwargs)
