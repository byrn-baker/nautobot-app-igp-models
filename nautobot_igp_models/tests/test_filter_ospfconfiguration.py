"""Tests for OSPFConfiguration filters."""

from django.test import TestCase

from nautobot_igp_models.filters import OSPFConfigurationFilterSet
from nautobot_igp_models.models import OSPFConfiguration
from nautobot_igp_models.tests.fixtures import create_ospf_configurations


class OSPFConfigurationFilterTestCase(TestCase):
    """Test cases for OSPFConfigurationFilterSet."""

    def test_filter_by_name(self):
        """Test filtering OSPF configurations by name."""
        ospf_configs = create_ospf_configurations()

        filterset = OSPFConfigurationFilterSet(
            data={"name": ospf_configs["router1"].name},
            queryset=OSPFConfiguration.objects.all(),
        )

        self.assertTrue(filterset.is_valid())
        self.assertEqual(filterset.qs.count(), 1)
        self.assertIn(ospf_configs["router1"], filterset.qs)

    def test_filter_by_q_search(self):
        """Test Q search across multiple fields."""
        create_ospf_configurations()

        filterset = OSPFConfigurationFilterSet(
            data={"q": "OSPF-Config-R1"},
            queryset=OSPFConfiguration.objects.all(),
        )

        self.assertTrue(filterset.is_valid())
        self.assertGreaterEqual(filterset.qs.count(), 1)

    def test_filter_by_instance(self):
        """Test filtering by IGP routing instance."""
        ospf_configs = create_ospf_configurations()

        filterset = OSPFConfigurationFilterSet(
            data={"instance": [ospf_configs["router1"].instance.pk]},
            queryset=OSPFConfiguration.objects.all(),
        )

        self.assertTrue(filterset.is_valid())
        self.assertEqual(filterset.qs.count(), 1)
        self.assertEqual(filterset.qs.first(), ospf_configs["router1"])

    def test_filter_by_process_id(self):
        """Test filtering by process_id."""
        create_ospf_configurations()

        filterset = OSPFConfigurationFilterSet(
            data={"process_id": 1},
            queryset=OSPFConfiguration.objects.all(),
        )

        self.assertTrue(filterset.is_valid())
        # All test fixtures use process_id 1
        self.assertGreaterEqual(filterset.qs.count(), 1)

    def test_filter_by_status(self):
        """Test filtering by status."""
        ospf_configs = create_ospf_configurations()

        filterset = OSPFConfigurationFilterSet(
            data={"status": [ospf_configs["router1"].status.pk]},
            queryset=OSPFConfiguration.objects.all(),
        )

        self.assertTrue(filterset.is_valid())
        self.assertGreaterEqual(filterset.qs.count(), 1)

    def test_filter_invalid_returns_empty(self):
        """Test that filtering with invalid values returns empty queryset."""
        create_ospf_configurations()

        filterset = OSPFConfigurationFilterSet(
            data={"name": "NonExistentConfig"},
            queryset=OSPFConfiguration.objects.all(),
        )

        self.assertTrue(filterset.is_valid())
        self.assertEqual(filterset.qs.count(), 0)

    def test_filter_multiple_instances(self):
        """Test filtering by multiple IGP instances."""
        ospf_configs = create_ospf_configurations()

        filterset = OSPFConfigurationFilterSet(
            data={
                "instance": [
                    ospf_configs["router1"].instance.pk,
                    ospf_configs["router2"].instance.pk,
                ]
            },
            queryset=OSPFConfiguration.objects.all(),
        )

        self.assertTrue(filterset.is_valid())
        self.assertEqual(filterset.qs.count(), 2)

    def test_filter_by_process_id_range(self):
        """Test filtering by different process_ids."""
        from nautobot_igp_models.tests.fixtures import create_igp_routing_instances, create_statuses

        igp_instances = create_igp_routing_instances()
        statuses = create_statuses()

        # Create OSPF configs with different process_ids
        OSPFConfiguration.objects.create(
            name="OSPF-Process-100",
            instance=igp_instances["ospf_router3"],
            process_id=100,
            status=statuses["active"],
        )

        filterset = OSPFConfigurationFilterSet(
            data={"process_id": 100},
            queryset=OSPFConfiguration.objects.all(),
        )

        self.assertTrue(filterset.is_valid())
        self.assertEqual(filterset.qs.count(), 1)
        self.assertEqual(filterset.qs.first().process_id, 100)

    def test_filter_no_filters_returns_all(self):
        """Test that no filters returns all objects."""
        create_ospf_configurations()

        filterset = OSPFConfigurationFilterSet(
            data={},
            queryset=OSPFConfiguration.objects.all(),
        )

        self.assertTrue(filterset.is_valid())
        self.assertEqual(filterset.qs.count(), OSPFConfiguration.objects.count())
