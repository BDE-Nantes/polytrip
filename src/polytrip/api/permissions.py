from django.utils import timezone

from rest_framework import permissions

from polytrip.siteconfig.models import SiteConfiguration


class EventOpened(permissions.BasePermission):
    def has_permission(self, request, view):
        site_configuration = SiteConfiguration.get_solo()
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_superuser
            or site_configuration.start_date < timezone.now() < site_configuration.end_date
        )


class IsTripOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or request.user == obj.team or request.user.is_superuser
