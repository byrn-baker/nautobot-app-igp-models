"""Tests for ISISConfiguration filters."""

from django.test import TestCase

from nautobot_igp_models.filters import ISISConfigurationFilterSet
from nautobot_igp_models.models import ISISConfiguration
from nautobot_igp_models.tests.fixtures import create_isis_configurations


class ISISConfigurationFilterTestCase(TestCase):
    """Test cases for ISISConfigurationFilterSet."""

    def test_filter_by_name(self):
        """Test filtering ISIS configurations by name."""
        isis_configs = create_isis_configurations()

        # Filter by exact name
        filterset = ISISConfigurationFilterSet(
            data={"name": isis_configs["router1"].name},
            queryset=ISISConfiguration.objects.all(),
        )

        self.assertTrue(filterset.is_valid())
        self.assertEqual(filterset.qs.count(), 1)
        self.assertIn(isis_configs["router1"], filterset.qs)

    def test_filter_by_q_search(self):
        """Test Q search across multiple fields."""
        create_isis_configurations()

        # Search by name
        filterset = ISISConfigurationFilterSet(
            data={"q": "ISIS-Config-R1"},
            queryset=ISISConfiguration.objects.all(),
        )

        self.assertTrue(filterset.is_valid())
        self.assertGreaterEqual(filterset.qs.count(), 1)

    def test_filter_by_instance(self):
        """Test filtering by IGP routing instance."""
        isis_configs = create_isis_configurations()

        filterset = ISISConfigurationFilterSet(
            data={"instance": [isis_configs["router1"].instance.pk]},
            queryset=ISISConfiguration.objects.all(),
        )

        self.assertTrue(filterset.is_valid())
        self.assertEqual(filterset.qs.count(), 1)
        self.assertEqual(filterset.qs.first(), isis_configs["router1"])

    def test_filter_by_status(self):
        """Test filtering by status."""
        isis_configs = create_isis_configurations()

        filterset = ISISConfigurationFilterSet(
            data={"status": [isis_configs["router1"].status.pk]},
            queryset=ISISConfiguration.objects.all(),
        )

        self.assertTrue(filterset.is_valid())
        self.assertGreaterEqual(filterset.qs.count(), 1)

    def test_filter_by_system_id(self):
        """Test filtering by system_id (NET)."""
        isis_configs = create_isis_configurations()

        # Get the system_id from router1
        system_id = isis_configs["router1"].system_id

        filterset = ISISConfigurationFilterSet(
            data={"system_id": system_id},
            queryset=ISISConfiguration.objects.all(),
        )

        self.assertTrue(filterset.is_valid())
        if system_id:  # Only test if system_id was generated
            self.assertGreaterEqual(filterset.qs.count(), 1)

    def test_filter_invalid_returns_empty(self):
        """Test that filtering with invalid values returns empty queryset."""
        create_isis_configurations()

        filterset = ISISConfigurationFilterSet(
            data={"name": "NonExistentConfig"},
            queryset=ISISConfiguration.objects.all(),
        )

        self.assertTrue(filterset.is_valid())
        self.assertEqual(filterset.qs.count(), 0)

    def test_filter_multiple_instances(self):
        """Test filtering by multiple IGP instances."""
        isis_configs = create_isis_configurations()

        filterset = ISISConfigurationFilterSet(
            data={
                "instance": [
                    isis_configs["router1"].instance.pk,
                    isis_configs["router2"].instance.pk,
                ]
            },
            queryset=ISISConfiguration.objects.all(),
        )

        self.assertTrue(filterset.is_valid())
        self.assertEqual(filterset.qs.count(), 2)

    def test_filter_no_filters_returns_all(self):
        """Test that no filters returns all objects."""
        create_isis_configurations()

        filterset = ISISConfigurationFilterSet(
            data={},
            queryset=ISISConfiguration.objects.all(),
        )

        self.assertTrue(filterset.is_valid())
        self.assertEqual(filterset.qs.count(), ISISConfiguration.objects.count())
