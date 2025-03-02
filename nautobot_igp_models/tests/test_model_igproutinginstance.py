"""Test IGPRoutingInstance."""

from django.test import TestCase

from nautobot_igp_models import models


class TestIGPRoutingInstance(TestCase):
    """Test IGPRoutingInstance."""

    def test_create_igproutinginstance_only_required(self):
        """Create with only required fields, and validate null description and __str__."""
        igproutinginstance = models.IGPRoutingInstance.objects.create(name="Development")
        self.assertEqual(igproutinginstance.name, "Development")
        self.assertEqual(igproutinginstance.description, "")
        self.assertEqual(str(igproutinginstance), "Development")

    def test_create_igproutinginstance_all_fields_success(self):
        """Create IGPRoutingInstance with all fields."""
        igproutinginstance = models.IGPRoutingInstance.objects.create(
            name="Development", description="Development Test"
        )
        self.assertEqual(igproutinginstance.name, "Development")
        self.assertEqual(igproutinginstance.description, "Development Test")
