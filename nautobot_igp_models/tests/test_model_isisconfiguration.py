"""Tests for ISISConfiguration model."""

from django.test import TestCase

from nautobot_igp_models.models import ISISConfiguration
from nautobot_igp_models.tests.fixtures import (
    create_igp_routing_instances,
    create_isis_configurations,
    create_statuses,
)


class ISISConfigurationModelTestCase(TestCase):
    """Test cases for ISISConfiguration model."""

    def test_create_isisconfiguration_with_required_fields(self):
        """Test creating ISISConfiguration with only required fields."""
        igp_instances = create_igp_routing_instances()
        statuses = create_statuses()

        isis_config = ISISConfiguration.objects.create(
            name="Test-ISIS-Config",
            instance=igp_instances["isis_router1"],
            status=statuses["active"],
        )

        self.assertIsNotNone(isis_config.pk)
        self.assertEqual(isis_config.name, "Test-ISIS-Config")
        self.assertEqual(isis_config.instance, igp_instances["isis_router1"])
        self.assertEqual(isis_config.status, statuses["active"])
        # system_id should be auto-generated
        self.assertIsNotNone(isis_config.system_id)

    def test_isisconfiguration_auto_generate_net(self):
        """Test that ISIS NET is auto-generated from router_id and isis_area."""
        igp_instances = create_igp_routing_instances()
        statuses = create_statuses()

        # Create ISIS config without system_id
        isis_config = ISISConfiguration.objects.create(
            name="Auto-NET-Config",
            instance=igp_instances["isis_router1"],
            status=statuses["active"],
        )

        # Verify NET was auto-generated
        self.assertIsNotNone(isis_config.system_id)
        # Format should be: area.system_id.00 (e.g., 49.0001.0010.0000.0001.00)
        self.assertIn("49.0001", isis_config.system_id)
        self.assertTrue(isis_config.system_id.endswith(".00"))

    def test_isisconfiguration_net_generation_formats(self):
        """Test NET generation with various IP/area combinations."""
        igp_instances = create_igp_routing_instances()
        statuses = create_statuses()

        isis_config = ISISConfiguration.objects.create(
            name="NET-Format-Test",
            instance=igp_instances["isis_router1"],  # router_id: 10.0.0.1/32, isis_area: 49.0001
            status=statuses["active"],
        )

        # Expected format for 10.0.0.1 in area 49.0001:
        # 49.0001.0010.0000.0001.00
        net_parts = isis_config.system_id.split(".")

        self.assertEqual(len(net_parts), 5)
        self.assertEqual(net_parts[0], "49")
        self.assertEqual(net_parts[1], "0001")
        self.assertEqual(net_parts[-1], "00")  # NSEL

    def test_isisconfiguration_unique_together_constraint(self):
        """Test that (instance, name) must be unique."""
        isis_configs = create_isis_configurations()

        # Try to create another ISIS config with same instance and name
        from django.db import IntegrityError

        with self.assertRaises(IntegrityError):
            ISISConfiguration.objects.create(
                name=isis_configs["router1"].name,
                instance=isis_configs["router1"].instance,
                system_id="49.0001.0010.0000.0001.00",
            )

    def test_isisconfiguration_str_method(self):
        """Test string representation of ISISConfiguration."""
        isis_configs = create_isis_configurations()

        isis_config = isis_configs["router1"]
        str_repr = str(isis_config)

        # Should contain the name
        self.assertIn(isis_config.name, str_repr)

    def test_isisconfiguration_manual_system_id(self):
        """Test creating ISIS config with manually specified system_id."""
        igp_instances = create_igp_routing_instances()
        statuses = create_statuses()

        manual_net = "49.0001.1234.5678.9012.00"
        isis_config = ISISConfiguration.objects.create(
            name="Manual-NET-Config",
            instance=igp_instances["isis_router2"],
            system_id=manual_net,
            status=statuses["active"],
        )

        # Manual system_id should be preserved (not overwritten)
        isis_config.refresh_from_db()
        self.assertEqual(isis_config.system_id, manual_net)

    def test_isisconfiguration_generate_full_net_method(self):
        """Test the generate_full_net() method directly."""
        igp_instances = create_igp_routing_instances()
        statuses = create_statuses()

        isis_config = ISISConfiguration(
            name="NET-Method-Test",
            instance=igp_instances["isis_router1"],
            status=statuses["active"],
        )

        # Call generate_full_net() directly
        generated_net = isis_config.generate_full_net()

        # Should return proper format
        self.assertIsNotNone(generated_net)
        self.assertIn("49.0001", generated_net)
        self.assertTrue(generated_net.endswith(".00"))
        # Should have 5 parts separated by dots
        self.assertEqual(len(generated_net.split(".")), 5)

    def test_isisconfiguration_net_generation_without_router_id(self):
        """Test NET generation fails gracefully without router_id."""
        from nautobot_igp_models.tests.fixtures import create_devices, create_statuses, create_vrfs

        devices = create_devices()
        statuses = create_statuses()
        vrfs = create_vrfs()

        # Create IGP instance without router_id
        from nautobot_igp_models.models import IGPRoutingInstance

        igp_no_router_id = IGPRoutingInstance.objects.create(
            name="ISIS-No-Router-ID",
            device=devices["router3"],
            protocol="ISIS",
            vrf=vrfs["global"],
            isis_area="49.0002",
            status=statuses["active"],
            # router_id intentionally omitted
        )

        isis_config = ISISConfiguration(
            name="No-Router-ID-Config",
            instance=igp_no_router_id,
            status=statuses["active"],
        )

        # Should raise ValueError when trying to generate NET
        with self.assertRaises(ValueError) as context:
            isis_config.generate_full_net()

        self.assertIn("router_id", str(context.exception).lower())

    def test_isisconfiguration_net_generation_without_isis_area(self):
        """Test NET generation fails gracefully without isis_area."""
        from nautobot_igp_models.tests.fixtures import (
            create_devices,
            create_ip_addresses,
            create_statuses,
            create_vrfs,
        )

        devices = create_devices()
        ip_addresses = create_ip_addresses()
        statuses = create_statuses()
        vrfs = create_vrfs()

        # Create IGP instance without isis_area (will fail validation but testing the method)
        from nautobot_igp_models.models import IGPRoutingInstance

        igp_no_area = IGPRoutingInstance.objects.create(
            name="ISIS-No-Area",
            device=devices["router3"],
            protocol="ISIS",
            router_id=ip_addresses["router3"],
            vrf=vrfs["global"],
            status=statuses["active"],
            # isis_area intentionally omitted
        )

        isis_config = ISISConfiguration(
            name="No-Area-Config",
            instance=igp_no_area,
            status=statuses["active"],
        )

        # Should raise ValueError when trying to generate NET
        with self.assertRaises(ValueError) as context:
            isis_config.generate_full_net()

        self.assertIn("isis_area", str(context.exception).lower())

    def test_isisconfiguration_update(self):
        """Test updating an existing ISISConfiguration."""
        isis_configs = create_isis_configurations()

        isis_config = isis_configs["router1"]
        original_system_id = isis_config.system_id

        # Update name
        isis_config.name = "Updated-ISIS-Config"
        isis_config.save()

        isis_config.refresh_from_db()
        self.assertEqual(isis_config.name, "Updated-ISIS-Config")
        # system_id should remain unchanged
        self.assertEqual(isis_config.system_id, original_system_id)
