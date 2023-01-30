from django.contrib.admin.sites import AdminSite
from django.contrib.gis.geos import LineString
from django.test import TestCase

from polytrip.accounts.tests.factories import UserFactory
from polytrip.schools.models import School
from polytrip.trips.admin import TripAdmin
from polytrip.trips.models import Trip


class TripAdminTest(TestCase):
    def test_get_distance(self):
        user = UserFactory(is_team=True, school=School.objects.first())
        trip = Trip.objects.get(team=user)
        trip.trip = LineString((0, 0), (10, 10))
        trip.save()
        ta = TripAdmin(Trip, AdminSite())
        self.assertAlmostEqual(ta.get_distance(trip), 1555.3, places=1)
