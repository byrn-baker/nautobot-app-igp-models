"""Tests for ISISInterfaceConfiguration model."""

from django.test import TestCase

from nautobot_igp_models.models import ISISInterfaceConfiguration
from nautobot_igp_models.tests.fixtures import (
    create_devices,
    create_interfaces,
    create_isis_configurations,
    create_isis_interface_configurations,
    create_statuses,
)


class ISISInterfaceConfigurationModelTestCase(TestCase):
    """Test cases for ISISInterfaceConfiguration model."""

    def test_create_isis_interface_configuration(self):
        """Test creating ISISInterfaceConfiguration with required fields."""
        isis_configs = create_isis_configurations()
        devices = create_devices()
        interfaces = create_interfaces()
        statuses = create_statuses()

        isis_int_config = ISISInterfaceConfiguration.objects.create(
            name="Test-ISIS-Interface",
            isis_config=isis_configs["router1"],
            device=devices["router1"],
            interface=interfaces["router1"]["ge2"],
            circuit_type="L1L2",
            metric=20,
            status=statuses["active"],
        )

        self.assertIsNotNone(isis_int_config.pk)
        self.assertEqual(isis_int_config.name, "Test-ISIS-Interface")
        self.assertEqual(isis_int_config.isis_config, isis_configs["router1"])
        self.assertEqual(isis_int_config.interface, interfaces["router1"]["ge2"])
        self.assertEqual(isis_int_config.circuit_type, "L1L2")
        self.assertEqual(isis_int_config.metric, 20)

    def test_isis_interface_circuit_type_l1(self):
        """Test ISIS interface with Level 1 circuit type."""
        isis_configs = create_isis_configurations()
        devices = create_devices()
        interfaces = create_interfaces()
        statuses = create_statuses()

        isis_int_config = ISISInterfaceConfiguration.objects.create(
            name="L1-Interface",
            isis_config=isis_configs["router2"],
            device=devices["router2"],
            interface=interfaces["router2"]["ge2"],
            circuit_type="L1",
            metric=10,
            status=statuses["active"],
        )

        self.assertEqual(isis_int_config.circuit_type, "L1")

    def test_isis_interface_circuit_type_l2(self):
        """Test ISIS interface with Level 2 circuit type."""
        isis_int_configs = create_isis_interface_configurations()

        isis_int_config = isis_int_configs["router1_ge1"]
        self.assertEqual(isis_int_config.circuit_type, "L2")

    def test_isis_interface_circuit_type_l1l2(self):
        """Test ISIS interface with Level 1-2 circuit type."""
        isis_configs = create_isis_configurations()
        devices = create_devices()
        interfaces = create_interfaces()
        statuses = create_statuses()

        isis_int_config = ISISInterfaceConfiguration.objects.create(
            name="L1L2-Interface",
            isis_config=isis_configs["router1"],
            device=devices["router1"],
            interface=interfaces["router1"]["loopback0"],
            circuit_type="L1L2",
            metric=1,
            status=statuses["active"],
        )

        self.assertEqual(isis_int_config.circuit_type, "L1L2")

    def test_isis_interface_unique_together_constraint(self):
        """Test that (isis_config, interface) must be unique."""
        isis_int_configs = create_isis_interface_configurations()

        # Try to create another ISIS interface config with same isis_config and interface
        from django.db import IntegrityError

        with self.assertRaises(IntegrityError):
            ISISInterfaceConfiguration.objects.create(
                name="Duplicate-Interface",
                isis_config=isis_int_configs["router1_ge1"].isis_config,
                device=isis_int_configs["router1_ge1"].device,
                interface=isis_int_configs["router1_ge1"].interface,
                circuit_type="L1",
                metric=50,
            )

    def test_isis_interface_metric_defaults(self):
        """Test default metric value."""
        isis_configs = create_isis_configurations()
        devices = create_devices()
        interfaces = create_interfaces()
        statuses = create_statuses()

        # Create without specifying metric
        isis_int_config = ISISInterfaceConfiguration.objects.create(
            name="Default-Metric",
            isis_config=isis_configs["router2"],
            device=devices["router2"],
            interface=interfaces["router2"]["loopback0"],
            circuit_type="L2",
            status=statuses["active"],
        )

        # Check if metric has a value (depends on model definition)
        self.assertIsNotNone(isis_int_config.metric)

    def test_isis_interface_str_method(self):
        """Test string representation of ISISInterfaceConfiguration."""
        isis_int_configs = create_isis_interface_configurations()

        isis_int_config = isis_int_configs["router1_ge1"]
        str_repr = str(isis_int_config)

        # Should contain the name
        self.assertIn(isis_int_config.name, str_repr)

    def test_isis_interface_device_consistency(self):
        """Test that interface belongs to the correct device."""
        isis_int_configs = create_isis_interface_configurations()

        isis_int_config = isis_int_configs["router1_ge1"]

        # Interface device should match the device field
        self.assertEqual(isis_int_config.interface.device, isis_int_config.device)

    def test_isis_interface_update(self):
        """Test updating an existing ISISInterfaceConfiguration."""
        isis_int_configs = create_isis_interface_configurations()

        isis_int_config = isis_int_configs["router1_ge1"]
        original_metric = isis_int_config.metric

        # Update metric
        isis_int_config.metric = 50
        isis_int_config.save()

        isis_int_config.refresh_from_db()
        self.assertEqual(isis_int_config.metric, 50)
        self.assertNotEqual(isis_int_config.metric, original_metric)

    def test_isis_interface_delete(self):
        """Test deleting an ISISInterfaceConfiguration."""
        isis_int_configs = create_isis_interface_configurations()

        isis_int_config = isis_int_configs["router1_ge1"]
        config_pk = isis_int_config.pk

        isis_int_config.delete()

        # Verify it's deleted
        with self.assertRaises(ISISInterfaceConfiguration.DoesNotExist):
            ISISInterfaceConfiguration.objects.get(pk=config_pk)

    def test_isis_interface_different_metrics(self):
        """Test that different interfaces can have different metrics."""
        isis_configs = create_isis_configurations()
        devices = create_devices()
        interfaces = create_interfaces()
        statuses = create_statuses()

        # Create interface with metric 10
        isis_int_1 = ISISInterfaceConfiguration.objects.create(
            name="Low-Metric",
            isis_config=isis_configs["router1"],
            device=devices["router1"],
            interface=interfaces["router1"]["loopback0"],
            circuit_type="L2",
            metric=10,
            status=statuses["active"],
        )

        # Create interface with metric 100
        isis_int_2 = ISISInterfaceConfiguration.objects.create(
            name="High-Metric",
            isis_config=isis_configs["router1"],
            device=devices["router1"],
            interface=interfaces["router1"]["ge2"],
            circuit_type="L2",
            metric=100,
            status=statuses["active"],
        )

        self.assertNotEqual(isis_int_1.metric, isis_int_2.metric)
        self.assertEqual(isis_int_1.metric, 10)
        self.assertEqual(isis_int_2.metric, 100)
