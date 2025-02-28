"""Test IGPProtocol Filter."""

from django.test import TestCase

from nautobot_igp_models import filters, models
from nautobot_igp_models.tests import fixtures


class IGPProtocolFilterTestCase(TestCase):
    """IGPProtocol Filter Test Case."""

    queryset = models.IGPProtocol.objects.all()
    filterset = filters.IGPProtocolFilterSet

    @classmethod
    def setUpTestData(cls):
        """Setup test data for IGPProtocol Model."""
        fixtures.create_igpprotocol()

    def test_q_search_name(self):
        """Test using Q search with name of IGPProtocol."""
        params = {"q": "Test One"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_q_invalid(self):
        """Test using invalid Q search for IGPProtocol."""
        params = {"q": "test-five"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 0)
