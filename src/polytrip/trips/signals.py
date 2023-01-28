from django.contrib.gis.geos import LineString

from .models import Trip


def create_trip(sender, **kwargs):
    instance = kwargs.get("instance")
    if instance.is_team and instance.school is not None:
        school_point = instance.school.coordinates
        Trip.objects.get_or_create(
            team=instance, defaults={"trip": LineString(school_point, (school_point.x + 0.01, school_point.y))}
        )
