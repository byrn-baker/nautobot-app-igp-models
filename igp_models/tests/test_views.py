"""Unit tests for views."""

from nautobot.apps.testing import ViewTestCases

from igp_models import models
from igp_models.tests import fixtures


class IGPProtocolViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    # pylint: disable=too-many-ancestors
    """Test the IGPProtocol views."""

    model = models.IGPProtocol
    bulk_edit_data = {"description": "Bulk edit views"}
    form_data = {
        "name": "Test 1",
        "description": "Initial model",
    }
    csv_data = (
        "name",
        "Test csv1",
        "Test csv2",
        "Test csv3",
    )

    @classmethod
    def setUpTestData(cls):
        fixtures.create_igpprotocol()
