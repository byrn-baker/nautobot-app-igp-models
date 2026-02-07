"""Tests for OSPFInterfaceConfiguration model."""

from django.test import TestCase

from nautobot_igp_models.models import OSPFInterfaceConfiguration
from nautobot_igp_models.tests.fixtures import (
    create_interfaces,
    create_ospf_configurations,
    create_ospf_interface_configurations,
    create_statuses,
)


class OSPFInterfaceConfigurationModelTestCase(TestCase):
    """Test cases for OSPFInterfaceConfiguration model."""

    def test_create_ospf_interface_configuration(self):
        """Test creating OSPFInterfaceConfiguration with required fields."""
        ospf_configs = create_ospf_configurations()
        interfaces = create_interfaces()
        statuses = create_statuses()

        ospf_int_config = OSPFInterfaceConfiguration.objects.create(
            name="Test-OSPF-Interface",
            ospf_config=ospf_configs["router1"],
            interface=interfaces["router1"]["ge2"],
            area="0.0.0.1",
            cost=10,
            status=statuses["active"],
        )

        self.assertIsNotNone(ospf_int_config.pk)
        self.assertEqual(ospf_int_config.name, "Test-OSPF-Interface")
        self.assertEqual(ospf_int_config.ospf_config, ospf_configs["router1"])
        self.assertEqual(ospf_int_config.interface, interfaces["router1"]["ge2"])
        self.assertEqual(ospf_int_config.area, "0.0.0.1")
        self.assertEqual(ospf_int_config.cost, 10)

    def test_ospf_interface_area_formats_dotted_decimal(self):
        """Test OSPF interface with dotted decimal area format."""
        ospf_int_configs = create_ospf_interface_configurations()

        ospf_int_config = ospf_int_configs["router1_ge1"]
        self.assertEqual(ospf_int_config.area, "0.0.0.0")

    def test_ospf_interface_area_formats_integer(self):
        """Test OSPF interface with integer area format."""
        ospf_configs = create_ospf_configurations()
        interfaces = create_interfaces()
        statuses = create_statuses()

        ospf_int_config = OSPFInterfaceConfiguration.objects.create(
            name="Integer-Area",
            ospf_config=ospf_configs["router2"],
            interface=interfaces["router2"]["ge2"],
            area="1",
            cost=10,
            status=statuses["active"],
        )

        self.assertEqual(ospf_int_config.area, "1")

    def test_ospf_interface_area_formats_large_integer(self):
        """Test OSPF interface with large integer area format."""
        ospf_configs = create_ospf_configurations()
        interfaces = create_interfaces()
        statuses = create_statuses()

        ospf_int_config = OSPFInterfaceConfiguration.objects.create(
            name="Large-Area",
            ospf_config=ospf_configs["router3"],
            interface=interfaces["router3"]["ge2"],
            area="4294967295",  # Max 32-bit unsigned integer
            cost=1,
            status=statuses["active"],
        )

        self.assertEqual(ospf_int_config.area, "4294967295")

    def test_ospf_interface_unique_together_constraint(self):
        """Test that (ospf_config, interface) must be unique."""
        ospf_int_configs = create_ospf_interface_configurations()

        # Try to create another OSPF interface config with same ospf_config and interface
        from django.db import IntegrityError

        with self.assertRaises(IntegrityError):
            OSPFInterfaceConfiguration.objects.create(
                name="Duplicate-Interface",
                ospf_config=ospf_int_configs["router1_ge1"].ospf_config,
                interface=ospf_int_configs["router1_ge1"].interface,
                area="0.0.0.2",
                cost=50,
            )

    def test_ospf_interface_cost_default(self):
        """Test default cost value."""
        ospf_configs = create_ospf_configurations()
        interfaces = create_interfaces()
        statuses = create_statuses()

        # Create without specifying cost
        ospf_int_config = OSPFInterfaceConfiguration.objects.create(
            name="Default-Cost",
            ospf_config=ospf_configs["router2"],
            interface=interfaces["router2"]["loopback0"],
            area="0.0.0.0",
            status=statuses["active"],
        )

        # Check if cost has a value (should default to 1 based on model definition)
        self.assertIsNotNone(ospf_int_config.cost)

    def test_ospf_interface_str_method(self):
        """Test string representation of OSPFInterfaceConfiguration."""
        ospf_int_configs = create_ospf_interface_configurations()

        ospf_int_config = ospf_int_configs["router1_ge1"]
        str_repr = str(ospf_int_config)

        # Should contain the name
        self.assertIn(ospf_int_config.name, str_repr)

    def test_ospf_interface_update(self):
        """Test updating an existing OSPFInterfaceConfiguration."""
        ospf_int_configs = create_ospf_interface_configurations()

        ospf_int_config = ospf_int_configs["router1_ge1"]
        original_cost = ospf_int_config.cost

        # Update cost and area
        ospf_int_config.cost = 100
        ospf_int_config.area = "0.0.0.5"
        ospf_int_config.save()

        ospf_int_config.refresh_from_db()
        self.assertEqual(ospf_int_config.cost, 100)
        self.assertEqual(ospf_int_config.area, "0.0.0.5")
        self.assertNotEqual(ospf_int_config.cost, original_cost)

    def test_ospf_interface_delete(self):
        """Test deleting an OSPFInterfaceConfiguration."""
        ospf_int_configs = create_ospf_interface_configurations()

        ospf_int_config = ospf_int_configs["router1_ge1"]
        config_pk = ospf_int_config.pk

        ospf_int_config.delete()

        # Verify it's deleted
        with self.assertRaises(OSPFInterfaceConfiguration.DoesNotExist):
            OSPFInterfaceConfiguration.objects.get(pk=config_pk)

    def test_ospf_interface_different_areas_same_device(self):
        """Test that different interfaces on same device can be in different areas."""
        ospf_configs = create_ospf_configurations()
        interfaces = create_interfaces()
        statuses = create_statuses()

        # Create interface in area 0
        ospf_int_1 = OSPFInterfaceConfiguration.objects.create(
            name="Area-0-Interface",
            ospf_config=ospf_configs["router1"],
            interface=interfaces["router1"]["loopback0"],
            area="0.0.0.0",
            cost=1,
            status=statuses["active"],
        )

        # Create interface in area 1
        ospf_int_2 = OSPFInterfaceConfiguration.objects.create(
            name="Area-1-Interface",
            ospf_config=ospf_configs["router1"],
            interface=interfaces["router1"]["ge2"],
            area="0.0.0.1",
            cost=10,
            status=statuses["active"],
        )

        self.assertNotEqual(ospf_int_1.area, ospf_int_2.area)
        self.assertEqual(ospf_int_1.ospf_config, ospf_int_2.ospf_config)

    def test_ospf_interface_different_costs(self):
        """Test that different interfaces can have different costs."""
        ospf_configs = create_ospf_configurations()
        interfaces = create_interfaces()
        statuses = create_statuses()

        # Create interface with cost 1
        ospf_int_1 = OSPFInterfaceConfiguration.objects.create(
            name="Low-Cost",
            ospf_config=ospf_configs["router2"],
            interface=interfaces["router2"]["loopback0"],
            area="0.0.0.0",
            cost=1,
            status=statuses["active"],
        )

        # Create interface with cost 1000
        ospf_int_2 = OSPFInterfaceConfiguration.objects.create(
            name="High-Cost",
            ospf_config=ospf_configs["router2"],
            interface=interfaces["router2"]["ge2"],
            area="0.0.0.0",
            cost=1000,
            status=statuses["active"],
        )

        self.assertNotEqual(ospf_int_1.cost, ospf_int_2.cost)
        self.assertEqual(ospf_int_1.cost, 1)
        self.assertEqual(ospf_int_2.cost, 1000)

    def test_ospf_interface_backbone_area(self):
        """Test OSPF interface configured for backbone area."""
        ospf_int_configs = create_ospf_interface_configurations()

        # All test fixtures use backbone area
        for config in ospf_int_configs.values():
            self.assertEqual(config.area, "0.0.0.0")
