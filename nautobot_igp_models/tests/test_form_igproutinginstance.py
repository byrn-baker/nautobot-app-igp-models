"""Test igproutinginstance forms."""

from django.test import TestCase

from nautobot_igp_models import forms


class IGPRoutingInstanceTest(TestCase):
    """Test IGPRoutingInstance forms."""

    def test_specifying_all_fields_success(self):
        form = forms.IGPRoutingInstanceForm(
            data={
                "name": "Development",
                "description": "Development Testing",
            }
        )
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def test_specifying_only_required_success(self):
        form = forms.IGPRoutingInstanceForm(
            data={
                "name": "Development",
            }
        )
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def test_validate_name_igproutinginstance_is_required(self):
        form = forms.IGPRoutingInstanceForm(data={"description": "Development Testing"})
        self.assertFalse(form.is_valid())
        self.assertIn("This field is required.", form.errors["name"])
