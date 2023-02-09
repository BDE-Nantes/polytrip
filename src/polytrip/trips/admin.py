from django.contrib import admin
from django.contrib.gis import forms
from django.contrib.gis.db.models import LineStringField
from django.utils.translation import gettext_lazy as _

from .models import Trip


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ("team", "get_school", "get_distance")
    readonly_fields = ("uuid", "get_distance")
    fields = ("uuid", "team", "trip", "get_distance")
    formfield_overrides = {LineStringField: {"widget": forms.OSMWidget}}

    def get_distance(self, obj):
        return round(obj.distance / 1000, 2)

    @admin.display(description=_("School"))
    def get_school(self, obj):
        return obj.team.school

    get_distance.short_description = _("Distance (km)")
