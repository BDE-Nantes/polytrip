from rest_framework import mixins, permissions, viewsets

from polytrip.schools.models import School
from polytrip.trips.models import Trip

from .permissions import IsTripOwnerOrReadOnly
from .serializers import SchoolSerializer, TripSerializer


class SchoolViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = "uuid"
    queryset = School.objects.all()
    serializer_class = SchoolSerializer


class TripViewSet(mixins.UpdateModelMixin, viewsets.ReadOnlyModelViewSet):
    lookup_field = "uuid"
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsTripOwnerOrReadOnly]
