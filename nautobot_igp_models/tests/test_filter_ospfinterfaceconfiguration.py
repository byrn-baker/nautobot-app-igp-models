"""Tests for OSPFInterfaceConfiguration filters."""

from django.test import TestCase

from nautobot_igp_models.filters import OSPFInterfaceConfigurationFilterSet
from nautobot_igp_models.models import OSPFInterfaceConfiguration
from nautobot_igp_models.tests.fixtures import create_ospf_interface_configurations


class OSPFInterfaceConfigurationFilterTestCase(TestCase):
    """Test cases for OSPFInterfaceConfigurationFilterSet."""

    def test_filter_by_name(self):
        """Test filtering OSPF interface configurations by name."""
        ospf_int_configs = create_ospf_interface_configurations()

        filterset = OSPFInterfaceConfigurationFilterSet(
            data={"name": ospf_int_configs["router1_ge1"].name},
            queryset=OSPFInterfaceConfiguration.objects.all(),
        )

        self.assertTrue(filterset.is_valid())
        self.assertEqual(filterset.qs.count(), 1)
        self.assertIn(ospf_int_configs["router1_ge1"], filterset.qs)

    def test_filter_by_q_search(self):
        """Test Q search across multiple fields."""
        create_ospf_interface_configurations()

        filterset = OSPFInterfaceConfigurationFilterSet(
            data={"q": "OSPF-R1-GE1"},
            queryset=OSPFInterfaceConfiguration.objects.all(),
        )

        self.assertTrue(filterset.is_valid())
        self.assertGreaterEqual(filterset.qs.count(), 1)

    def test_filter_by_ospf_config(self):
        """Test filtering by OSPF configuration."""
        ospf_int_configs = create_ospf_interface_configurations()

        filterset = OSPFInterfaceConfigurationFilterSet(
            data={"ospf_config": [ospf_int_configs["router1_ge1"].ospf_config.pk]},
            queryset=OSPFInterfaceConfiguration.objects.all(),
        )

        self.assertTrue(filterset.is_valid())
        self.assertGreaterEqual(filterset.qs.count(), 1)

    def test_filter_by_interface(self):
        """Test filtering by interface."""
        ospf_int_configs = create_ospf_interface_configurations()

        filterset = OSPFInterfaceConfigurationFilterSet(
            data={"interface": [ospf_int_configs["router1_ge1"].interface.pk]},
            queryset=OSPFInterfaceConfiguration.objects.all(),
        )

        self.assertTrue(filterset.is_valid())
        self.assertEqual(filterset.qs.count(), 1)

    def test_filter_by_area(self):
        """Test filtering by OSPF area."""
        create_ospf_interface_configurations()

        filterset = OSPFInterfaceConfigurationFilterSet(
            data={"area": "0.0.0.0"},
            queryset=OSPFInterfaceConfiguration.objects.all(),
        )

        self.assertTrue(filterset.is_valid())
        # All test fixtures use area 0.0.0.0
        self.assertGreaterEqual(filterset.qs.count(), 1)

    def test_filter_by_cost(self):
        """Test filtering by cost."""
        create_ospf_interface_configurations()

        filterset = OSPFInterfaceConfigurationFilterSet(
            data={"cost": 1},
            queryset=OSPFInterfaceConfiguration.objects.all(),
        )

        self.assertTrue(filterset.is_valid())
        # All test fixtures use cost 1
        self.assertGreaterEqual(filterset.qs.count(), 1)

    def test_filter_by_status(self):
        """Test filtering by status."""
        ospf_int_configs = create_ospf_interface_configurations()

        filterset = OSPFInterfaceConfigurationFilterSet(
            data={"status": [ospf_int_configs["router1_ge1"].status.pk]},
            queryset=OSPFInterfaceConfiguration.objects.all(),
        )

        self.assertTrue(filterset.is_valid())
        self.assertGreaterEqual(filterset.qs.count(), 1)

    def test_filter_invalid_returns_empty(self):
        """Test that filtering with invalid values returns empty queryset."""
        create_ospf_interface_configurations()

        filterset = OSPFInterfaceConfigurationFilterSet(
            data={"name": "NonExistentInterface"},
            queryset=OSPFInterfaceConfiguration.objects.all(),
        )

        self.assertTrue(filterset.is_valid())
        self.assertEqual(filterset.qs.count(), 0)

    def test_filter_by_area_different_formats(self):
        """Test filtering by area in different formats."""
        from nautobot_igp_models.tests.fixtures import create_interfaces, create_ospf_configurations, create_statuses

        ospf_configs = create_ospf_configurations()
        interfaces = create_interfaces()
        statuses = create_statuses()

        # Create interface with integer area format
        OSPFInterfaceConfiguration.objects.create(
            name="Area-1-Interface",
            ospf_config=ospf_configs["router2"],
            interface=interfaces["router2"]["loopback0"],
            area="1",
            cost=10,
            status=statuses["active"],
        )

        filterset = OSPFInterfaceConfigurationFilterSet(
            data={"area": "1"},
            queryset=OSPFInterfaceConfiguration.objects.all(),
        )

        self.assertTrue(filterset.is_valid())
        self.assertEqual(filterset.qs.count(), 1)
        self.assertEqual(filterset.qs.first().area, "1")

    def test_filter_no_filters_returns_all(self):
        """Test that no filters returns all objects."""
        create_ospf_interface_configurations()

        filterset = OSPFInterfaceConfigurationFilterSet(
            data={},
            queryset=OSPFInterfaceConfiguration.objects.all(),
        )

        self.assertTrue(filterset.is_valid())
        self.assertEqual(filterset.qs.count(), OSPFInterfaceConfiguration.objects.count())
