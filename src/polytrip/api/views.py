from rest_framework import mixins, permissions, status, views, viewsets
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


class UserInfoView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        data = {value: getattr(request.user, value, None) for value in ("username", "team_name")}
        school = request.user.school
        if school is not None:
            data["school_name"] = school.name
            data["school_color"] = school.color
        trip = getattr(request.user, "trip", None)
        if trip is not None:
            data["trip"] = TripSerializer(trip).data
        return Response(data)
