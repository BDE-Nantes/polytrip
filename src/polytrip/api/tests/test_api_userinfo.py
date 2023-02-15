from rest_framework import status
from rest_framework.test import APITestCase

from polytrip.accounts.models import User
from polytrip.accounts.tests.factories import UserFactory
from polytrip.schools.models import School


class APITestsUserInfo(APITestCase):
    def test_get_forbidden_no_auth(self):
        school = School.objects.first()
        UserFactory(is_team=True, school=school, team_name="Team 1")
        request = self.client.get("/api/users/me/")

        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_auth(self):
        school = School.objects.first()
        team_1 = UserFactory(is_team=True, school=school)

        self.client.force_authenticate(team_1)
        request = self.client.get("/api/users/me/")
        self.assertEqual(request.status_code, status.HTTP_200_OK)

        admin = User.objects.create_superuser(username="admin", email="admin@example.com", password="admin")

        self.client.force_authenticate(admin)
        request = self.client.get("/api/users/me/")
        self.assertEqual(request.status_code, status.HTTP_200_OK)
