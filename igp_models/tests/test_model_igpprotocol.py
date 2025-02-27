"""Test IGPProtocol."""

from django.test import TestCase

from igp_models import models


class TestIGPProtocol(TestCase):
    """Test IGPProtocol."""

    def test_create_igpprotocol_only_required(self):
        """Create with only required fields, and validate null description and __str__."""
        igpprotocol = models.IGPProtocol.objects.create(name="Development")
        self.assertEqual(igpprotocol.name, "Development")
        self.assertEqual(igpprotocol.description, "")
        self.assertEqual(str(igpprotocol), "Development")

    def test_create_igpprotocol_all_fields_success(self):
        """Create IGPProtocol with all fields."""
        igpprotocol = models.IGPProtocol.objects.create(name="Development", description="Development Test")
        self.assertEqual(igpprotocol.name, "Development")
        self.assertEqual(igpprotocol.description, "Development Test")
