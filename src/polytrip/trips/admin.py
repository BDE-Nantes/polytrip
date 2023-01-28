from django.contrib import admin
from django.contrib.gis import forms
from django.contrib.gis.db.models import LineStringField

from .models import Trip


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ("team",)
    readonly_fields = ("uuid",)
    fields = ("uuid", "team", "trip")
    formfield_overrides = {LineStringField: {"widget": forms.OSMWidget}}
