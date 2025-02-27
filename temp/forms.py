"""Forms for igp_models."""

from django import forms
from nautobot.apps.forms import NautobotBulkEditForm, NautobotFilterForm, NautobotModelForm, TagsBulkEditFormMixin

from igp_models import models


class IGPProtocolForm(NautobotModelForm):  # pylint: disable=too-many-ancestors
    """IGPProtocol creation/edit form."""

    class Meta:
        """Meta attributes."""

        model = models.IGPProtocol
        fields = [
            "name",
            "device",
            "enabled",
            "process_id",
        ]


class IGPProtocolBulkEditForm(TagsBulkEditFormMixin, NautobotBulkEditForm):  # pylint: disable=too-many-ancestors
    """IGPProtocol bulk edit form."""

    pk = forms.ModelMultipleChoiceField(queryset=models.IGPProtocol.objects.all(), widget=forms.MultipleHiddenInput)
    description = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""


class IGPProtocolFilterForm(NautobotFilterForm):
    """Filter form to filter searches."""

    model = models.IGPProtocol
    field_order = ["q", "name"]

    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Slug.",
    )
    name = forms.CharField(required=False, label="Name")
