from datetime import datetime

from django.forms import ValidationError
from django.test import TestCase

from polytrip.siteconfig.models import SiteConfiguration


class TestModelValidation(TestCase):
    def test_is_team_no_school_constraint(self):
        site_configuration = SiteConfiguration.get_solo()
        site_configuration.start_date = datetime(2023, 1, 2)
        site_configuration.end_date = datetime(2023, 1, 1)
        self.assertRaises(ValidationError, site_configuration.clean)
