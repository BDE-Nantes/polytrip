from rest_framework import mixins, permissions, viewsets

from polytrip.trips.models import Trip

from .permissions import IsTripOwnerOrReadOnly
from .serializers import TripSerializer


class TripViewSet(mixins.UpdateModelMixin, viewsets.ReadOnlyModelViewSet):
    lookup_field = "uuid"
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsTripOwnerOrReadOnly]
