"""Views for nautobot_igp_models."""

from nautobot.apps.views import NautobotUIViewSet

from nautobot_igp_models import filters, forms, models, tables
from nautobot_igp_models.api import serializers


class IGPRoutingInstanceUIViewSet(NautobotUIViewSet):
    """ViewSet for IGPRoutingInstance views."""

    bulk_update_form_class = forms.IGPRoutingInstanceBulkEditForm
    filterset_class = filters.IGPRoutingInstanceFilterSet
    filterset_form_class = forms.IGPRoutingInstanceFilterForm
    form_class = forms.IGPRoutingInstanceForm
    lookup_field = "pk"
    queryset = models.IGPRoutingInstance.objects.all()
    serializer_class = serializers.IGPRoutingInstanceSerializer
    table_class = tables.IGPRoutingInstanceTable


class ISISConfigurationUIViewSet(NautobotUIViewSet):
    """UIViewset for ISISConfiguration model."""

    bulk_update_form_class = forms.ISISConfigurationBulkEditForm
    filterset_class = filters.ISISConfigurationFilterSet
    filterset_form_class = forms.ISISConfigurationFilterForm
    form_class = forms.ISISConfigurationForm
    lookup_field = "pk"
    queryset = models.ISISConfiguration.objects.all()
    serializer_class = serializers.ISISConfigurationSerializer
    table_class = tables.ISISConfigurationTable


class ISISInterfaceConfigurationUIViewSet(NautobotUIViewSet):
    """UIViewset for ISISInterfaceConfiguration model."""

    bulk_update_form_class = forms.ISISInterfaceConfigurationBulkEditForm
    filterset_class = filters.ISISInterfaceConfigurationFilterSet
    filterset_form_class = forms.ISISInterfaceConfigurationFilterForm
    form_class = forms.ISISInterfaceConfigurationForm
    lookup_field = "pk"
    queryset = models.ISISInterfaceConfiguration.objects.all()
    serializer_class = serializers.ISISInterfaceConfigurationSerializer
    table_class = tables.ISISInterfaceConfigurationTable


class OSPFConfigurationUIViewSet(NautobotUIViewSet):
    """UIViewset for OSPFConfiguration model."""

    bulk_update_form_class = forms.OSPFConfigurationBulkEditForm
    filterset_class = filters.OSPFConfigurationFilterSet
    filterset_form_class = forms.OSPFConfigurationFilterForm
    form_class = forms.OSPFConfigurationForm
    lookup_field = "pk"
    queryset = models.OSPFConfiguration.objects.all()
    serializer_class = serializers.OSPFConfigurationSerializer
    table_class = tables.OSPFConfigurationTable


class OSPFInterfaceConfigurationUIViewSet(NautobotUIViewSet):
    """UIViewset for OSPFInterfaceConfiguration model."""

    bulk_update_form_class = forms.OSPFInterfaceConfigurationBulkEditForm
    filterset_class = filters.OSPFInterfaceConfigurationFilterSet
    filterset_form_class = forms.OSPFInterfaceConfigurationFilterForm
    form_class = forms.OSPFInterfaceConfigurationForm
    lookup_field = "pk"
    queryset = models.OSPFInterfaceConfiguration.objects.all()
    serializer_class = serializers.OSPFInterfaceConfigurationSerializer
    table_class = tables.OSPFInterfaceConfigurationTable
