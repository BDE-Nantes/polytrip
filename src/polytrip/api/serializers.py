from rest_framework import serializers

from polytrip.schools.models import School
from polytrip.siteconfig.models import SiteConfiguration
from polytrip.trips.models import Trip


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = [
            "uuid",
            "name",
            "color",
            "coordinates",
        ]


class TripSerializer(serializers.ModelSerializer):
    team = serializers.SlugRelatedField(read_only=True, slug_field="team_name")
    school = serializers.SerializerMethodField("get_school")

    def get_school(self, obj):
        return getattr(obj.team.school, "uuid", None)

    class Meta:
        model = Trip
        fields = [
            "uuid",
            "team",
            "school",
            "trip",
            "distance",
        ]
        read_only_fields = ["uuid", "team", "school", "distance"]


class SiteConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteConfiguration
        fields = ["start_date"]
