from django.apps import AppConfig
from django.db.models.signals import post_save


class TripsConfig(AppConfig):
    name = "polytrip.trips"

    def ready(self) -> None:
        from .signals import create_trip

        post_save.connect(create_trip, sender="accounts.User", dispatch_uid="unique_identifier")
