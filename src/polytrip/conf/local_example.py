#
# Any machine specific settings when using development settings.
#

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "polytrip",
        "USER": "polytrip",
        "PASSWORD": "polytrip",
        "HOST": "",  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        "PORT": "",  # Set to empty string for default.
    }
}
