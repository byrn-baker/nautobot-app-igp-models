"""Test igproutinginstance forms."""

from django.test import TestCase

from nautobot_igp_models import forms
from nautobot_igp_models.tests.fixtures import create_devices, create_ip_addresses, create_statuses, create_vrfs


class IGPRoutingInstanceTest(TestCase):
    """Test IGPRoutingInstance forms."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data."""
        cls.devices = create_devices()
        cls.statuses = create_statuses()
        cls.ip_addresses = create_ip_addresses()
        cls.vrfs = create_vrfs()

    def test_specifying_all_fields_success(self):
        form = forms.IGPRoutingInstanceForm(
            data={
                "name": "Development",
                "description": "Development Testing",
                "device": self.devices["router1"].pk,
                "protocol": "ISIS",
                "router_id": self.ip_addresses["router1"].pk,
                "vrf": self.vrfs["global"].pk,
                "isis_area": "49.0001",
                "status": self.statuses["active"].pk,
            }
        )
        self.assertTrue(form.is_valid(), form.errors)
        self.assertTrue(form.save())

    def test_specifying_only_required_success(self):
        form = forms.IGPRoutingInstanceForm(
            data={
                "name": "Development-Required-Only",
                "device": self.devices["router3"].pk,
                "protocol": "OSPF",
                "status": self.statuses["active"].pk,
            }
        )
        self.assertTrue(form.is_valid(), form.errors)
        self.assertTrue(form.save())

    def test_validate_name_igproutinginstance_is_required(self):
        form = forms.IGPRoutingInstanceForm(
            data={
                "description": "Development Testing",
                "device": self.devices["router1"].pk,
                "protocol": "ISIS",
                "status": self.statuses["active"].pk,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
