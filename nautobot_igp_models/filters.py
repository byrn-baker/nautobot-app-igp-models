"""Filters for the Nautobot IGP Models app."""

import django_filters
from nautobot.apps.filters import NautobotFilterSet
from nautobot.dcim.models import Device
from nautobot.extras.models import Status
from nautobot.ipam.models import VRF, IPAddress

from nautobot_igp_models import models


class IGPInstanceFilterSet(NautobotFilterSet):
    """Filter capabilities for IGPInstance objects."""

    device_id = django_filters.ModelMultipleChoiceFilter(queryset=Device.objects.all(), label="Device (ID)")
    device = django_filters.ModelMultipleChoiceFilter(
        field_name="device__name", queryset=Device.objects.all(), to_field_name="name", label="Device (Name)"
    )
    protocol = django_filters.MultipleChoiceFilter(
        choices=models.IGPInstance._meta.get_field("protocol").choices, label="Protocol"
    )
    router_id = django_filters.ModelMultipleChoiceFilter(queryset=IPAddress.objects.all(), label="Router ID")
    vrf_id = django_filters.ModelMultipleChoiceFilter(queryset=VRF.objects.all(), label="VRF (ID)")
    vrf = django_filters.ModelMultipleChoiceFilter(
        field_name="vrf__name", queryset=VRF.objects.all(), to_field_name="name", label="VRF (Name)"
    )
    isis_area = django_filters.CharFilter(lookup_expr="exact", label="ISIS Area")
    status = django_filters.ModelMultipleChoiceFilter(
        field_name="status__slug", queryset=Status.objects.all(), to_field_name="slug", label="Status (Slug)"
    )

    class Meta:
        model = models.IGPInstance
        fields = [
            "id",
            "device_id",
            "device",
            "protocol",
            "router_id",
            "vrf_id",
            "vrf",
            "isis_area",
            "status",
        ]


class ISISConfigurationFilterSet(NautobotFilterSet):
    """Filter capabilities for ISISConfiguration objects."""

    instance_id = django_filters.ModelMultipleChoiceFilter(
        queryset=models.IGPInstance.objects.filter(protocol="ISIS"), label="IGP Instance (ID)"
    )
    instance = django_filters.ModelMultipleChoiceFilter(
        field_name="instance__device__name",
        queryset=models.IGPInstance.objects.filter(protocol="ISIS"),
        to_field_name="device__name",
        label="IGP Instance (Device Name)",
    )
    system_id = django_filters.CharFilter(lookup_expr="exact", label="System ID")
    status = django_filters.ModelMultipleChoiceFilter(
        field_name="status__slug", queryset=Status.objects.all(), to_field_name="slug", label="Status (Slug)"
    )

    class Meta:
        model = models.ISISConfiguration
        fields = [
            "id",
            "instance_id",
            "instance",
            "system_id",
            "status",
        ]

class ISISInterfaceConfigurationFilterSet(NautobotFilterSet):
    """Filter capabilities for ISISInterfaceConfiguration objects."""

    instance_id = django_filters.ModelMultipleChoiceFilter(
        queryset=models.IGPInstance.objects.filter(protocol="ISIS"), label="IGP Instance (ID)"
    )
    instance = django_filters.ModelMultipleChoiceFilter(
        field_name="instance__device__name",
        queryset=models.IGPInstance.objects.filter(protocol="ISIS"),
        to_field_name="device__name",
        label="IGP Instance (Device Name)",
    )
    interface = django_filters.CharFilter(lookup_expr="exact", label="Interface")
    circuit_type = django_filters.MultipleChoiceFilter(choices=models.ISISInterfaceConfiguration._meta.get_field("circuit_type").choices, label="Circuit Type")
    metric = django_filters.NumberFilter(lookup_expr="exact", label="Metric")
    status = django_filters.ModelMultipleChoiceFilter(
        field_name="status__slug", queryset=Status.objects.all(), to_field_name="slug", label="Status (Slug)"
    )
    
    class Meta:
        model = models.ISISInterfaceConfiguration
        fields = [
            "id",
            "instance_id",
            "instance",
            "interface",
            "circuit_type",
            "metric",
            "status",
        ]


class OSPFConfigurationFilterSet(NautobotFilterSet):
    """Filter capabilities for OSPFConfiguration objects."""

    instance_id = django_filters.ModelMultipleChoiceFilter(
        queryset=models.IGPInstance.objects.filter(protocol="OSPF"), label="IGP Instance (ID)"
    )
    instance = django_filters.ModelMultipleChoiceFilter(
        field_name="instance__device__name",
        queryset=models.IGPInstance.objects.filter(protocol="OSPF"),
        to_field_name="device__name",
        label="IGP Instance (Device Name)",
    )
    area = django_filters.CharFilter(lookup_expr="exact", label="OSPF Area")
    process_id = django_filters.NumberFilter(lookup_expr="exact", label="Process ID")
    status = django_filters.ModelMultipleChoiceFilter(
        field_name="status__slug", queryset=Status.objects.all(), to_field_name="slug", label="Status (Slug)"
    )

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
        queryset=models.IGPInstance.objects.filter(protocol="OSPF"), label="IGP Instance (ID)"
    )
    instance = django_filters.ModelMultipleChoiceFilter(
        field_name="instance__device__name",
        queryset=models.IGPInstance.objects.filter(protocol="OSPF"),
        to_field_name="device__name",
        label="IGP Instance (Device Name)",
    )
    interface = django_filters.CharFilter(lookup_expr="exact", label="Interface")
    area = django_filters.CharFilter(lookup_expr="exact", label="OSPF Area")
    cost = django_filters.NumberFilter(lookup_expr="exact", label="Cost")
    status = django_filters.ModelMultipleChoiceFilter(
        field_name="status__slug", queryset=Status.objects.all(), to_field_name="slug", label="Status (Slug)"
    )
    
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