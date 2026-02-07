"""Tests for OSPFConfiguration forms."""

from django.test import TestCase

from nautobot_igp_models.forms import OSPFConfigurationForm
from nautobot_igp_models.tests.fixtures import create_igp_routing_instances, create_statuses


class OSPFConfigurationFormTestCase(TestCase):
    """Test cases for OSPFConfigurationForm."""

    def test_form_with_valid_data(self):
        """Test form with all valid data."""
        igp_instances = create_igp_routing_instances()
        statuses = create_statuses()

        form_data = {
            "name": "Test-OSPF-Form",
            "instance": igp_instances["ospf_router1"].pk,
            "process_id": 1,
            "status": statuses["active"].pk,
        }

        form = OSPFConfigurationForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_form_with_custom_process_id(self):
        """Test form with custom process_id."""
        igp_instances = create_igp_routing_instances()
        statuses = create_statuses()

        form_data = {
            "name": "Custom-Process-Form",
            "instance": igp_instances["ospf_router2"].pk,
            "process_id": 100,
            "status": statuses["active"].pk,
        }

        form = OSPFConfigurationForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_form_with_required_fields_only(self):
        """Test form with only required fields."""
        igp_instances = create_igp_routing_instances()
        statuses = create_statuses()

        form_data = {
            "name": "Minimal-OSPF-Form",
            "instance": igp_instances["ospf_router3"].pk,
            "status": statuses["active"].pk,
            # process_id will use default
        }

        form = OSPFConfigurationForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_form_missing_required_name(self):
        """Test form fails without required name field."""
        igp_instances = create_igp_routing_instances()
        statuses = create_statuses()

        form_data = {
            # name missing
            "instance": igp_instances["ospf_router1"].pk,
            "process_id": 1,
            "status": statuses["active"].pk,
        }

        form = OSPFConfigurationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_form_missing_required_instance(self):
        """Test form fails without required instance field."""
        statuses = create_statuses()

        form_data = {
            "name": "No-Instance",
            # instance missing
            "process_id": 1,
            "status": statuses["active"].pk,
        }

        form = OSPFConfigurationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("instance", form.errors)

    def test_form_with_invalid_instance(self):
        """Test form with invalid instance ID."""
        statuses = create_statuses()

        form_data = {
            "name": "Invalid-Instance",
            "instance": 99999,  # Non-existent ID
            "process_id": 1,
            "status": statuses["active"].pk,
        }

        form = OSPFConfigurationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("instance", form.errors)

    def test_form_saves_correctly(self):
        """Test that form saves correctly and creates model instance."""
        igp_instances = create_igp_routing_instances()
        statuses = create_statuses()

        form_data = {
            "name": "Save-Test-OSPF",
            "instance": igp_instances["ospf_router1"].pk,
            "process_id": 200,
            "status": statuses["planned"].pk,
        }

        form = OSPFConfigurationForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

        ospf_config = form.save()
        self.assertIsNotNone(ospf_config.pk)
        self.assertEqual(ospf_config.name, "Save-Test-OSPF")
        self.assertEqual(ospf_config.process_id, 200)
        self.assertEqual(ospf_config.status, statuses["planned"])
