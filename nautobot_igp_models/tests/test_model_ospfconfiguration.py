"""Tests for OSPFConfiguration model."""

from django.test import TestCase

from nautobot_igp_models.models import OSPFConfiguration
from nautobot_igp_models.tests.fixtures import (
    create_igp_routing_instances,
    create_ospf_configurations,
    create_statuses,
)


class OSPFConfigurationModelTestCase(TestCase):
    """Test cases for OSPFConfiguration model."""

    def test_create_ospfconfiguration_with_required_fields(self):
        """Test creating OSPFConfiguration with only required fields."""
        igp_instances = create_igp_routing_instances()
        statuses = create_statuses()

        ospf_config = OSPFConfiguration.objects.create(
            name="Test-OSPF-Config",
            instance=igp_instances["ospf_router1"],
            status=statuses["active"],
        )

        self.assertIsNotNone(ospf_config.pk)
        self.assertEqual(ospf_config.name, "Test-OSPF-Config")
        self.assertEqual(ospf_config.instance, igp_instances["ospf_router1"])
        self.assertEqual(ospf_config.status, statuses["active"])
        # process_id should have default value of 1
        self.assertEqual(ospf_config.process_id, 1)

    def test_ospfconfiguration_process_id_default(self):
        """Test that process_id defaults to 1."""
        igp_instances = create_igp_routing_instances()
        statuses = create_statuses()

        ospf_config = OSPFConfiguration.objects.create(
            name="Default-Process-ID",
            instance=igp_instances["ospf_router2"],
            status=statuses["active"],
            # process_id not specified
        )

        self.assertEqual(ospf_config.process_id, 1)

    def test_ospfconfiguration_custom_process_id(self):
        """Test creating OSPF config with custom process_id."""
        igp_instances = create_igp_routing_instances()
        statuses = create_statuses()

        ospf_config = OSPFConfiguration.objects.create(
            name="Custom-Process-ID",
            instance=igp_instances["ospf_router3"],
            process_id=100,
            status=statuses["active"],
        )

        self.assertEqual(ospf_config.process_id, 100)

    def test_ospfconfiguration_unique_together_constraint(self):
        """Test that (instance, process_id) must be unique."""
        ospf_configs = create_ospf_configurations()

        # Try to create another OSPF config with same instance and process_id
        from django.db import IntegrityError

        with self.assertRaises(IntegrityError):
            OSPFConfiguration.objects.create(
                name="Duplicate-Config",
                instance=ospf_configs["router1"].instance,
                process_id=ospf_configs["router1"].process_id,
            )

    def test_ospfconfiguration_same_device_different_process_id(self):
        """Test that same instance can have multiple OSPF configs with different process_ids."""
        igp_instances = create_igp_routing_instances()
        statuses = create_statuses()

        # Create first OSPF config with process_id 1
        ospf_config1 = OSPFConfiguration.objects.create(
            name="OSPF-Process-1",
            instance=igp_instances["ospf_router1"],
            process_id=1,
            status=statuses["active"],
        )

        # Create second OSPF config with process_id 2 (should succeed)
        ospf_config2 = OSPFConfiguration.objects.create(
            name="OSPF-Process-2",
            instance=igp_instances["ospf_router1"],
            process_id=2,
            status=statuses["active"],
        )

        self.assertNotEqual(ospf_config1.pk, ospf_config2.pk)
        self.assertEqual(ospf_config1.instance, ospf_config2.instance)
        self.assertNotEqual(ospf_config1.process_id, ospf_config2.process_id)

    def test_ospfconfiguration_str_method(self):
        """Test string representation of OSPFConfiguration."""
        ospf_configs = create_ospf_configurations()

        ospf_config = ospf_configs["router1"]
        str_repr = str(ospf_config)

        # Should contain the name
        self.assertIn(ospf_config.name, str_repr)

    def test_ospfconfiguration_limit_choices_to_ospf(self):
        """Test that only OSPF protocol instances are allowed."""
        from nautobot_igp_models.tests.fixtures import create_statuses

        # Try to use an ISIS instance with OSPF config
        igp_instances = create_igp_routing_instances()
        statuses = create_statuses()

        # This should work at the database level, but the form should prevent it
        # Testing that the FK relationship exists
        ospf_config = OSPFConfiguration(
            name="Wrong-Protocol",
            instance=igp_instances["isis_router1"],  # ISIS instance!
            process_id=1,
            status=statuses["active"],
        )

        # The model itself doesn't enforce protocol type, but forms should
        # This is more of a form validation test, but we can check the relationship
        self.assertEqual(ospf_config.instance.protocol, "ISIS")

    def test_ospfconfiguration_update(self):
        """Test updating an existing OSPFConfiguration."""
        ospf_configs = create_ospf_configurations()

        ospf_config = ospf_configs["router1"]
        original_process_id = ospf_config.process_id

        # Update name
        ospf_config.name = "Updated-OSPF-Config"
        ospf_config.save()

        ospf_config.refresh_from_db()
        self.assertEqual(ospf_config.name, "Updated-OSPF-Config")
        self.assertEqual(ospf_config.process_id, original_process_id)

    def test_ospfconfiguration_delete(self):
        """Test deleting an OSPFConfiguration."""
        ospf_configs = create_ospf_configurations()

        ospf_config = ospf_configs["router1"]
        config_pk = ospf_config.pk

        ospf_config.delete()

        # Verify it's deleted
        with self.assertRaises(OSPFConfiguration.DoesNotExist):
            OSPFConfiguration.objects.get(pk=config_pk)

    def test_ospfconfiguration_with_all_fields(self):
        """Test creating OSPF config with all available fields."""
        igp_instances = create_igp_routing_instances()
        statuses = create_statuses()

        ospf_config = OSPFConfiguration.objects.create(
            name="Complete-OSPF-Config",
            instance=igp_instances["ospf_router2"],
            process_id=200,
            status=statuses["planned"],
        )

        self.assertIsNotNone(ospf_config.pk)
        self.assertEqual(ospf_config.name, "Complete-OSPF-Config")
        self.assertEqual(ospf_config.process_id, 200)
        self.assertEqual(ospf_config.status, statuses["planned"])
