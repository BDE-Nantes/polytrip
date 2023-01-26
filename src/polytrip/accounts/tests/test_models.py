from django.forms import ValidationError
from django.test import TestCase

from polytrip.accounts.models import User
from polytrip.schools.models import School
from polytrip.trips.models import Trip

from .factories import UserFactory


class TestModelValidation(TestCase):
    def test_is_team_no_school_constraint(self):
        invalid_user = UserFactory.build(is_team=True)
        self.assertRaises(ValidationError, invalid_user.clean)
        invalid_user.save()
        self.assertEqual(User.objects.count(), 0)

    def test_is_not_team_school_constraint(self):
        invalid_user = UserFactory.build(is_team=False, school=School.objects.first())
        self.assertRaises(ValidationError, invalid_user.clean)
        invalid_user.save()
        self.assertEqual(User.objects.count(), 0)

    def test_trip_created_after_save(self):
        valid_user = UserFactory(is_team=True, school=School.objects.first())
        trip = Trip.objects.get(team=valid_user)
        self.assertEqual(str(trip), str(valid_user))
