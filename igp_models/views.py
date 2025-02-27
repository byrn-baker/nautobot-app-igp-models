"""Views for igp_models."""

from nautobot.apps.views import NautobotUIViewSet

from igp_models import filters, forms, models, tables
from igp_models.api import serializers


class IGPProtocolUIViewSet(NautobotUIViewSet):
    """ViewSet for IGPProtocol views."""

    bulk_update_form_class = forms.IGPProtocolBulkEditForm
    filterset_class = filters.IGPProtocolFilterSet
    filterset_form_class = forms.IGPProtocolFilterForm
    form_class = forms.IGPProtocolForm
    lookup_field = "pk"
    queryset = models.IGPProtocol.objects.all()
    serializer_class = serializers.IGPProtocolSerializer
    table_class = tables.IGPProtocolTable
