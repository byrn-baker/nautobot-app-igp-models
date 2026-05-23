"""Filtering for nautobot_igp_models."""

import django_filters
from nautobot.apps.filters import NameSearchFilterSet, NautobotFilterSet, SearchFilter, StatusModelFilterSetMixin
from nautobot.dcim.models import Device, Interface

from nautobot_igp_models import models


class IGPRoutingInstanceFilterSet(NautobotFilterSet, NameSearchFilterSet, StatusModelFilterSetMixin):
    """Filter for IGPRoutingInstance."""

    q = SearchFilter(
        filter_predicates={
            "name": "icontains",
            "description": "icontains",
        },
    )

    class Meta:
        """Meta attributes for filter."""

        model = models.IGPRoutingInstance
        fields = ["id", "name", "description", "device", "protocol", "router_id", "vrf", "isis_area", "status"]


class ISISConfigurationFilterSet(NautobotFilterSet, StatusModelFilterSetMixin):
    """Filter capabilities for ISISConfiguration objects."""

    q = SearchFilter(
        filter_predicates={
            "name": "icontains",
            "system_id": "icontains",
        },
    )

    name = django_filters.CharFilter(lookup_expr="exact", label="Name")
    instance = django_filters.ModelMultipleChoiceFilter(
        queryset=models.IGPRoutingInstance.objects.filter(protocol="ISIS"),
        label="IGP Instance",
    )
    system_id = django_filters.CharFilter(lookup_expr="exact", label="System ID")

    class Meta:
        model = models.ISISConfiguration
        fields = ["id", "name", "instance", "system_id", "status"]


class ISISInterfaceConfigurationFilterSet(NautobotFilterSet, StatusModelFilterSetMixin):
    """Filter capabilities for ISISInterfaceConfiguration objects."""

    q = SearchFilter(
        filter_predicates={
            "name": "icontains",
        },
    )

    name = django_filters.CharFilter(lookup_expr="exact", label="Name")
    isis_config = django_filters.ModelChoiceFilter(
        queryset=models.ISISConfiguration.objects.all(),
        label="ISIS Configuration",
    )
    device = django_filters.ModelChoiceFilter(
        queryset=Device.objects.all(),
        label="Device",
    )
    interface = django_filters.ModelChoiceFilter(
        queryset=Interface.objects.all(),
        label="Interface",
    )
    circuit_type = django_filters.CharFilter(lookup_expr="exact", label="Circuit Type")

    class Meta:
        model = models.ISISInterfaceConfiguration
        fields = [
            "id",
            "name",
            "isis_config",
            "device",
            "interface",
            "circuit_type",
            "network_type",
            "metric",
            "status",
        ]


class OSPFConfigurationFilterSet(NautobotFilterSet, StatusModelFilterSetMixin):
    """Filter capabilities for OSPFConfiguration objects."""

    q = SearchFilter(
        filter_predicates={
            "name": "icontains",
        },
    )

    name = django_filters.CharFilter(lookup_expr="exact", label="Name")
    instance = django_filters.ModelMultipleChoiceFilter(
        queryset=models.IGPRoutingInstance.objects.filter(protocol="OSPF"),
        label="IGP Instance",
    )
    process_id = django_filters.NumberFilter(lookup_expr="exact", label="Process ID")

    class Meta:
        model = models.OSPFConfiguration
        fields = ["id", "name", "instance", "process_id", "status"]


class OSPFInterfaceConfigurationFilterSet(NautobotFilterSet, StatusModelFilterSetMixin):
    """Filter capabilities for OSPFInterfaceConfiguration objects."""

    q = SearchFilter(
        filter_predicates={
            "name": "icontains",
        },
    )

    name = django_filters.CharFilter(lookup_expr="exact", label="Name")
    ospf_config = django_filters.ModelChoiceFilter(
        queryset=models.OSPFConfiguration.objects.all(),
        label="OSPF Configuration",
    )
    interface = django_filters.ModelChoiceFilter(
        queryset=Interface.objects.all(),
        label="Interface",
    )
    area = django_filters.CharFilter(lookup_expr="exact", label="OSPF Area")
    network_type = django_filters.CharFilter(lookup_expr="exact", label="Network Type")
    cost = django_filters.NumberFilter(lookup_expr="exact", label="Cost")

    class Meta:
        model = models.OSPFInterfaceConfiguration
        fields = ["id", "name", "ospf_config", "interface", "area", "network_type", "cost", "status"]
