"""Filtering for nautobot_igp_models."""
import django_filters
from nautobot.apps.filters import NameSearchFilterSet, NautobotFilterSet, StatusModelFilterSetMixin

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

    instance_id = django_filters.ModelMultipleChoiceFilter(
        queryset=models.IGPRoutingInstance.objects.filter(protocol="ISIS"), label="IGP Instance (ID)"
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
        fields = ["id", "instance_id", "instance", "system_id", "status"]

class ISISInterfaceConfigurationFilterSet(NautobotFilterSet, StatusModelFilterSetMixin):
    """Filter capabilities for ISISInterfaceConfiguration objects."""

    instance_id = django_filters.ModelMultipleChoiceFilter(
        queryset=models.IGPRoutingInstance.objects.filter(protocol="ISIS"), label="IGP Instance (ID)"
    )
    instance = django_filters.ModelMultipleChoiceFilter(
        field_name="instance__device__name",
        queryset=models.IGPRoutingInstance.objects.filter(protocol="ISIS"),
        to_field_name="device__name",
        label="IGP Instance (Device Name)",
    )
    interface = django_filters.CharFilter(lookup_expr="exact", label="Interface")
    circuit_type = django_filters.MultipleChoiceFilter(choices=models.ISISInterfaceConfiguration._meta.get_field("circuit_type").choices, label="Circuit Type")
    metric = django_filters.NumberFilter(lookup_expr="exact", label="Metric")
    
    class Meta:
        model = models.ISISInterfaceConfiguration
        fields = ["id", "instance_id", "instance", "interface", "circuit_type", "metric", "status"]

class OSPFConfigurationFilterSet(NautobotFilterSet):
    """Filter capabilities for OSPFConfiguration objects."""

    instance_id = django_filters.ModelMultipleChoiceFilter(
        queryset=models.IGPRoutingInstance.objects.filter(protocol="OSPF"), label="IGP Instance (ID)"
    )
    instance = django_filters.ModelMultipleChoiceFilter(
        field_name="instance__device__name",
        queryset=models.IGPRoutingInstance.objects.filter(protocol="OSPF"),
        to_field_name="device__name",
        label="IGP Instance (Device Name)",
    )
    area = django_filters.CharFilter(lookup_expr="exact", label="OSPF Area")
    process_id = django_filters.NumberFilter(lookup_expr="exact", label="Process ID")

    class Meta:
        model = models.OSPFConfiguration
        fields = [
            "id",
            "instance_id",
            "instance",
            "area",
            "process_id",
            "status",
        ]

class OSPFInterfaceConfigurationFilterSet(NautobotFilterSet):
    instance_id = django_filters.ModelMultipleChoiceFilter(
        queryset=models.IGPRoutingInstance.objects.filter(protocol="OSPF"), label="IGP Instance (ID)"
    )
    instance = django_filters.ModelMultipleChoiceFilter(
        field_name="instance__device__name",
        queryset=models.IGPRoutingInstance.objects.filter(protocol="OSPF"),
        to_field_name="device__name",
        label="IGP Instance (Device Name)",
    )
    interface = django_filters.CharFilter(lookup_expr="exact", label="Interface")
    area = django_filters.CharFilter(lookup_expr="exact", label="OSPF Area")
    cost = django_filters.NumberFilter(lookup_expr="exact", label="Cost")
    
    class meta:
        model = models.OSPFInterfaceConfiguration
        fields = [
            "id",
            "instance_id",
            "instance",
            "interface",
            "area",
            "cost",
            "status",
        ]