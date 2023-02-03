from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase


class APITestsSchool(APITestCase):
    def test_get_all(self):
        data = self.client.get(reverse("api:school-list")).json()

        self.assertEqual(len(data), 16)

    def test_unsafe_forbidden(self):
        data = {"name": "New school", "color": "#FFFFFF", "coordinates": {"type": "Point", "coordinates": [0, 0]}}
        post_resp = self.client.post(reverse("api:school-list"), data=data, format="json")
        self.assertEqual(post_resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
