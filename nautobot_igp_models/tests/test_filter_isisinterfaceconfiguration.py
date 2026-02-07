"""Tests for ISISInterfaceConfiguration filters."""

from django.test import TestCase

from nautobot_igp_models.filters import ISISInterfaceConfigurationFilterSet
from nautobot_igp_models.models import ISISInterfaceConfiguration
from nautobot_igp_models.tests.fixtures import create_isis_interface_configurations


class ISISInterfaceConfigurationFilterTestCase(TestCase):
    """Test cases for ISISInterfaceConfigurationFilterSet."""

    def test_filter_by_name(self):
        """Test filtering ISIS interface configurations by name."""
        isis_int_configs = create_isis_interface_configurations()

        filterset = ISISInterfaceConfigurationFilterSet(
            data={"name": isis_int_configs["router1_ge1"].name},
            queryset=ISISInterfaceConfiguration.objects.all(),
        )

        self.assertTrue(filterset.is_valid())
        self.assertEqual(filterset.qs.count(), 1)
        self.assertIn(isis_int_configs["router1_ge1"], filterset.qs)

    def test_filter_by_q_search(self):
        """Test Q search across multiple fields."""
        create_isis_interface_configurations()

        filterset = ISISInterfaceConfigurationFilterSet(
            data={"q": "ISIS-R1-GE1"},
            queryset=ISISInterfaceConfiguration.objects.all(),
        )

        self.assertTrue(filterset.is_valid())
        self.assertGreaterEqual(filterset.qs.count(), 1)

    def test_filter_by_isis_config(self):
        """Test filtering by ISIS configuration."""
        isis_int_configs = create_isis_interface_configurations()

        filterset = ISISInterfaceConfigurationFilterSet(
            data={"isis_config": [isis_int_configs["router1_ge1"].isis_config.pk]},
            queryset=ISISInterfaceConfiguration.objects.all(),
        )

        self.assertTrue(filterset.is_valid())
        self.assertGreaterEqual(filterset.qs.count(), 1)

    def test_filter_by_interface(self):
        """Test filtering by interface."""
        isis_int_configs = create_isis_interface_configurations()

        filterset = ISISInterfaceConfigurationFilterSet(
            data={"interface": [isis_int_configs["router1_ge1"].interface.pk]},
            queryset=ISISInterfaceConfiguration.objects.all(),
        )

        self.assertTrue(filterset.is_valid())
        self.assertEqual(filterset.qs.count(), 1)

    def test_filter_by_circuit_type(self):
        """Test filtering by circuit type."""
        create_isis_interface_configurations()

        filterset = ISISInterfaceConfigurationFilterSet(
            data={"circuit_type": "L2"},
            queryset=ISISInterfaceConfiguration.objects.all(),
        )

        self.assertTrue(filterset.is_valid())
        # All test fixtures use L2
        self.assertGreaterEqual(filterset.qs.count(), 1)

    def test_filter_by_metric(self):
        """Test filtering by metric."""
        create_isis_interface_configurations()

        filterset = ISISInterfaceConfigurationFilterSet(
            data={"metric": 10},
            queryset=ISISInterfaceConfiguration.objects.all(),
        )

        self.assertTrue(filterset.is_valid())
        # All test fixtures use metric 10
        self.assertGreaterEqual(filterset.qs.count(), 1)

    def test_filter_by_status(self):
        """Test filtering by status."""
        isis_int_configs = create_isis_interface_configurations()

        filterset = ISISInterfaceConfigurationFilterSet(
            data={"status": [isis_int_configs["router1_ge1"].status.pk]},
            queryset=ISISInterfaceConfiguration.objects.all(),
        )

        self.assertTrue(filterset.is_valid())
        self.assertGreaterEqual(filterset.qs.count(), 1)

    def test_filter_by_device(self):
        """Test filtering by device."""
        isis_int_configs = create_isis_interface_configurations()

        filterset = ISISInterfaceConfigurationFilterSet(
            data={"device": [isis_int_configs["router1_ge1"].device.pk]},
            queryset=ISISInterfaceConfiguration.objects.all(),
        )

        self.assertTrue(filterset.is_valid())
        self.assertGreaterEqual(filterset.qs.count(), 1)

    def test_filter_invalid_returns_empty(self):
        """Test that filtering with invalid values returns empty queryset."""
        create_isis_interface_configurations()

        filterset = ISISInterfaceConfigurationFilterSet(
            data={"name": "NonExistentInterface"},
            queryset=ISISInterfaceConfiguration.objects.all(),
        )

        self.assertTrue(filterset.is_valid())
        self.assertEqual(filterset.qs.count(), 0)

    def test_filter_no_filters_returns_all(self):
        """Test that no filters returns all objects."""
        create_isis_interface_configurations()

        filterset = ISISInterfaceConfigurationFilterSet(
            data={},
            queryset=ISISInterfaceConfiguration.objects.all(),
        )

        self.assertTrue(filterset.is_valid())
        self.assertEqual(filterset.qs.count(), ISISInterfaceConfiguration.objects.count())
