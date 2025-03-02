"""Unit tests for nautobot_igp_models."""

from nautobot.apps.testing import APIViewTestCases

from nautobot_igp_models import models
from nautobot_igp_models.tests import fixtures


class IGPRoutingInstanceAPIViewTest(APIViewTestCases.APIViewTestCase):
    # pylint: disable=too-many-ancestors
    """Test the API viewsets for IGPRoutingInstance."""

    model = models.IGPRoutingInstance
    create_data = [
        {
            "name": "Test Model 1",
            "description": "test description",
        },
        {
            "name": "Test Model 2",
        },
    ]
    bulk_update_data = {"description": "Test Bulk Update"}

    @classmethod
    def setUpTestData(cls):
        fixtures.create_igproutinginstance()
