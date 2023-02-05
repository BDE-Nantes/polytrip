from django.apps import AppConfig
from django.db.backends.signals import connection_created


def init_site_config(*args, **kwargs):
    from .models import SiteConfiguration

    SiteConfiguration.get_solo()


class SiteconfigConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "polytrip.siteconfig"

    def ready(self):
        connection_created.connect(init_site_config, sender=self)
