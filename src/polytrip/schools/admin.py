from django.contrib import admin
from django.contrib.gis import forms
from django.contrib.gis.db.models import PointField

from .models import School


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ("name", "color")
    list_filter = ("name",)
    readonly_fields = ("uuid",)
    fields = ("uuid", "name", "color", "coordinates")
    search_fields = ("name",)
    formfield_overrides = {PointField: {"widget": forms.OSMWidget}}
