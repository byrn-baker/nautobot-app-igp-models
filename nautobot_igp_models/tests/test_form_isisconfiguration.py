"""Tests for ISISConfiguration forms."""

from django.test import TestCase

from nautobot_igp_models.forms import ISISConfigurationForm
from nautobot_igp_models.tests.fixtures import create_igp_routing_instances, create_statuses


class ISISConfigurationFormTestCase(TestCase):
    """Test cases for ISISConfigurationForm."""

    def test_form_with_valid_data(self):
        """Test form with all valid data."""
        igp_instances = create_igp_routing_instances()
        statuses = create_statuses()

        form_data = {
            "name": "Test-ISIS-Form",
            "instance": igp_instances["isis_router1"].pk,
            "system_id": "49.0001.0010.0000.0001.00",
            "status": statuses["active"].pk,
        }

        form = ISISConfigurationForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_form_with_required_fields_only(self):
        """Test form with only required fields."""
        igp_instances = create_igp_routing_instances()
        statuses = create_statuses()

        form_data = {
            "name": "Minimal-ISIS-Form",
            "instance": igp_instances["isis_router2"].pk,
            "status": statuses["active"].pk,
            # system_id is optional (will be auto-generated)
        }

        form = ISISConfigurationForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_form_missing_required_name(self):
        """Test form fails without required name field."""
        igp_instances = create_igp_routing_instances()
        statuses = create_statuses()

        form_data = {
            # name missing
            "instance": igp_instances["isis_router1"].pk,
            "status": statuses["active"].pk,
        }

        form = ISISConfigurationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_form_missing_required_instance(self):
        """Test form fails without required instance field."""
        statuses = create_statuses()

        form_data = {
            "name": "No-Instance",
            # instance missing
            "status": statuses["active"].pk,
        }

        form = ISISConfigurationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("instance", form.errors)

    def test_form_missing_required_status(self):
        """Test form fails without required status field."""
        igp_instances = create_igp_routing_instances()

        form_data = {
            "name": "No-Status",
            "instance": igp_instances["isis_router1"].pk,
            # status missing
        }

        form = ISISConfigurationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("status", form.errors)

    def test_form_net_suggestion_in_help_text(self):
        """Test that NET suggestion appears in help text when instance has router_id and isis_area."""
        igp_instances = create_igp_routing_instances()
        statuses = create_statuses()

        # Create form with instance data (simulating POST)
        form_data = {
            "name": "NET-Suggestion-Test",
            "instance": igp_instances["isis_router1"].pk,
            "status": statuses["active"].pk,
        }

        form = ISISConfigurationForm(data=form_data)

        # Check if help text contains "Suggested NET"
        help_text = form.fields["system_id"].help_text
        # The form should generate a NET suggestion based on router_id and isis_area
        self.assertIn("NET", help_text)

    def test_form_with_invalid_instance(self):
        """Test form with invalid instance ID."""
        statuses = create_statuses()

        form_data = {
            "name": "Invalid-Instance",
            "instance": 99999,  # Non-existent ID
            "status": statuses["active"].pk,
        }

        form = ISISConfigurationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("instance", form.errors)

    def test_form_with_invalid_status(self):
        """Test form with invalid status ID."""
        igp_instances = create_igp_routing_instances()

        form_data = {
            "name": "Invalid-Status",
            "instance": igp_instances["isis_router1"].pk,
            "status": 99999,  # Non-existent ID
        }

        form = ISISConfigurationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("status", form.errors)

    def test_form_saves_correctly(self):
        """Test that form saves correctly and creates model instance."""
        igp_instances = create_igp_routing_instances()
        statuses = create_statuses()

        form_data = {
            "name": "Save-Test-ISIS",
            "instance": igp_instances["isis_router1"].pk,
            "system_id": "49.0001.1234.5678.9012.00",
            "status": statuses["active"].pk,
        }

        form = ISISConfigurationForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

        isis_config = form.save()
        self.assertIsNotNone(isis_config.pk)
        self.assertEqual(isis_config.name, "Save-Test-ISIS")
        self.assertEqual(isis_config.system_id, "49.0001.1234.5678.9012.00")
