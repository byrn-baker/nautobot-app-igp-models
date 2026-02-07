"""Test IGPRoutingInstance Filter."""

from django.test import TestCase

from nautobot_igp_models import filters, models
from nautobot_igp_models.tests import fixtures


class IGPRoutingInstanceFilterTestCase(TestCase):
    """IGPRoutingInstance Filter Test Case."""

    queryset = models.IGPRoutingInstance.objects.all()
    filterset = filters.IGPRoutingInstanceFilterSet

    @classmethod
    def setUpTestData(cls):
        """Setup test data for IGPRoutingInstance Model."""
        fixtures.create_igp_routing_instances()

    def test_q_search_name(self):
        """Test using Q search with name of IGPRoutingInstance."""
        params = {"q": "Test One"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_q_invalid(self):
        """Test using invalid Q search for IGPRoutingInstance."""
        params = {"q": "test-five"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 0)
