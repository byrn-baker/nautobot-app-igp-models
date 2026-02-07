"""Filtering for nautobot_igp_models."""

import django_filters
from nautobot.apps.filters import NameSearchFilterSet, NautobotFilterSet, SearchFilter, StatusModelFilterSetMixin
from nautobot.dcim.models import Interface

from nautobot_igp_models import models


class IGPRoutingInstanceFilterSet(NautobotFilterSet, NameSearchFilterSet, StatusModelFilterSetMixin):  # pylint: disable=too-many-ancestors
    """Filter for IGPRoutingInstance."""

    class Meta:
        """Meta attributes for filter."""

        model = models.IGPRoutingInstance

        # add any fields from the model that you would like to filter your searches by using those
        fields = ["id", "name", "description", "device", "protocol", "router_id", "vrf", "isis_area", "status"]


class ISISConfigurationFilterSet(NautobotFilterSet, StatusModelFilterSetMixin):
    """Filter capabilities for ISISConfiguration objects."""

    q = SearchFilter(
        filter_predicates={
            "name": "icontains",
        },
    )

    instance = django_filters.ModelMultipleChoiceFilter(
        field_name="instance__device__name",
        queryset=models.IGPRoutingInstance.objects.filter(protocol="ISIS"),
        to_field_name="device__name",
        label="IGP Instance (Device Name)",
    )
    system_id = django_filters.CharFilter(lookup_expr="exact", label="System ID")

    class Meta:
        model = models.ISISConfiguration
        fields = ["id", "instance", "system_id", "status"]


class ISISInterfaceConfigurationFilterSet(NautobotFilterSet, StatusModelFilterSetMixin):
    """Filter capabilities for ISISInterfaceConfiguration objects."""

    isis_config = django_filters.ModelChoiceFilter(
        queryset=models.ISISConfiguration.objects.all(),
        label="ISIS Configuration",
    )

    interface = django_filters.ModelChoiceFilter(
        queryset=Interface.objects.all(),
        label="Interface",
        method="filter_interface_by_device",
    )

    def filter_interface_by_device(self, queryset, name, value):
        if value:
            return queryset.filter(device=value.device)
        return queryset

    class Meta:
        model = models.ISISInterfaceConfiguration
        fields = ["isis_config", "interface", "circuit_type", "metric", "status"]


class OSPFConfigurationFilterSet(NautobotFilterSet):
    """Filter capabilities for OSPFConfiguration objects."""

    instance = django_filters.ModelMultipleChoiceFilter(
        field_name="instance__device__name",
        queryset=models.IGPRoutingInstance.objects.filter(protocol="OSPF"),
        to_field_name="device__name",
        label="IGP Instance (Device Name)",
    )
    process_id = django_filters.NumberFilter(lookup_expr="exact", label="Process ID")

    class Meta:
        model = models.OSPFConfiguration
        fields = ["id", "instance", "process_id", "status"]


class OSPFInterfaceConfigurationFilterSet(NautobotFilterSet):
    ospf_config_name = django_filters.CharFilter(lookup_expr="exact", label="OSPF Configuration")
    interface = django_filters.CharFilter(lookup_expr="exact", label="Interface")
    area = django_filters.CharFilter(lookup_expr="exact", label="OSPF Area")
    cost = django_filters.NumberFilter(lookup_expr="exact", label="Cost")

    class Meta:
        model = models.OSPFInterfaceConfiguration
        fields = ["id", "ospf_config_name", "interface", "area", "cost", "status"]
