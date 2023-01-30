from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from polytrip.accounts.tests.factories import UserFactory
from polytrip.schools.models import School


class APITestsTrip(APITestCase):
    def test_get_all(self):
        school = School.objects.first()
        team_1 = UserFactory(is_team=True, school=school, team_name="Team 1")
        data = self.client.get(reverse("api:trip-list")).json()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["school"], str(school.uuid))
        self.assertEqual(data[0]["team"], team_1.team_name)

    def test_update_auth(self):
        school = School.objects.first()
        team_1 = UserFactory(is_team=True, school=school)

        trip_uuid = team_1.trip.uuid

        patch_data = {
            "trip": {
                "type": "LineString",
                "coordinates": [
                    [-0.5942667, 47.4805249],
                    [-0.5942667, 47.4805248],
                ],
            }
        }

        patch_resp = self.client.patch(
            reverse("api:trip-detail", kwargs={"uuid": trip_uuid}), data=patch_data, format="json"
        )
        self.assertEqual(patch_resp.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(team_1)
        patch_resp = self.client.patch(
            reverse("api:trip-detail", kwargs={"uuid": trip_uuid}), data=patch_data, format="json"
        )
        self.assertEqual(patch_resp.status_code, status.HTTP_200_OK)

        team_2 = UserFactory(is_team=True, school=school)
        self.client.force_authenticate(team_2)
        patch_resp = self.client.patch(
            reverse("api:trip-detail", kwargs={"uuid": trip_uuid}), data=patch_data, format="json"
        )
        self.assertEqual(patch_resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_bad_request(self):
        school = School.objects.first()
        team_1 = UserFactory(is_team=True, school=school)

        patch_data = {
            "trip": {
                "type": "LineString",
                "coordinates": [
                    [-0.5942667, 47.4805249],
                ],
            }
        }

        self.client.force_authenticate(team_1)
        patch_resp = self.client.patch(
            reverse("api:trip-detail", kwargs={"uuid": team_1.trip.uuid}), data=patch_data, format="json"
        )
        self.assertEqual(
            patch_resp.status_code,
            status.HTTP_400_BAD_REQUEST,
            "The server shouldn't accept coordinates of only one point.",
        )
