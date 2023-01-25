from django.apps import AppConfig


class UtilsConfig(AppConfig):
    name = "polytrip.utils"

    def ready(self):
        from . import checks  # noqa
