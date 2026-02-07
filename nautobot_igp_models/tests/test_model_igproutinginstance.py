"""Test IGPRoutingInstance."""

from django.test import TestCase

from nautobot_igp_models import models
from nautobot_igp_models.tests import fixtures


class TestIGPRoutingInstance(TestCase):
    """Test IGPRoutingInstance."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data for IGPRoutingInstance."""
        cls.devices = fixtures.create_devices()
        cls.statuses = fixtures.create_statuses()

    def test_create_igproutinginstance_only_required(self):
        """Create with only required fields, and validate null description and __str__."""
        igproutinginstance = models.IGPRoutingInstance.objects.create(
            name="Development",
            device=self.devices["router1"],
            protocol="ISIS",
            status=self.statuses["active"],
        )
        self.assertEqual(igproutinginstance.name, "Development")
        self.assertEqual(igproutinginstance.description, "")
        self.assertEqual(str(igproutinginstance), "Development")

    def test_create_igproutinginstance_all_fields_success(self):
        """Create IGPRoutingInstance with all fields."""
        ip_addresses = fixtures.create_ip_addresses()
        vrfs = fixtures.create_vrfs()
        igproutinginstance = models.IGPRoutingInstance.objects.create(
            name="Development",
            description="Development Test",
            device=self.devices["router2"],
            protocol="OSPF",
            router_id=ip_addresses["router1"],
            vrf=vrfs["global"],
            status=self.statuses["active"],
        )
        self.assertEqual(igproutinginstance.name, "Development")
        self.assertEqual(igproutinginstance.description, "Development Test")
