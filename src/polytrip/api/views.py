from rest_framework import mixins, permissions, status, viewsets
from rest_framework.response import Response

from polytrip.schools.models import School
from polytrip.siteconfig.models import SiteConfiguration
from polytrip.trips.models import Trip

from .permissions import EventOpened, IsTripOwnerOrReadOnly
from .serializers import SchoolSerializer, SiteConfigurationSerializer, TripSerializer


class SchoolViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = "uuid"
    queryset = School.objects.all()
    serializer_class = SchoolSerializer


class TripViewSet(mixins.UpdateModelMixin, viewsets.ReadOnlyModelViewSet):
    lookup_field = "uuid"
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, EventOpened, IsTripOwnerOrReadOnly]


class SiteConfigurationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SiteConfiguration.objects.all()
    serializer_class = SiteConfigurationSerializer

    def retrieve(self, requests, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def list(self, requests, *args, **kwargs):
        instance = self.get_queryset().first()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
