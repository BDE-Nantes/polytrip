from io import StringIO
from typing import Any

from django.apps import AppConfig
from django.core.management import call_command
from django.db.models.signals import post_migrate


def update_schools(sender: object, **kwargs: Any) -> None:
    from .models import School

    School.objects.all().delete()

    call_command("loaddata", "default_schools", verbosity=0, stdout=StringIO(), stderr=StringIO())


class SchoolsConfig(AppConfig):
    name = "polytrip.schools"

    def ready(self) -> None:
        post_migrate.connect(update_schools, sender=self)
