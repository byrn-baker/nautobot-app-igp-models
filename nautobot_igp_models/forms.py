"""Forms for the Nautobot IGP Models app."""

from django import forms
from nautobot.apps.forms import (
    DynamicModelChoiceField,
    NautobotBulkEditForm,
    NautobotFilterForm,
    NautobotModelForm,
    StaticSelect2,
)
from nautobot.dcim.models import Interface
from nautobot.extras.models import Status

from nautobot_igp_models import models


# IGPInstance Forms
class IGPInstanceForm(NautobotModelForm):
    """Form for creating and editing IGPInstance objects."""

    device = DynamicModelChoiceField(queryset=models.Device.objects.all(), label="Device")
    router_id = DynamicModelChoiceField(queryset=models.IPAddress.objects.all(), label="Router ID", query_params={"device_id": "$device"})
    vrf = DynamicModelChoiceField(queryset=models.VRF.objects.all(), required=False, label="VRF")

    class Meta:
        model = models.IGPInstance
        fields = ("device", "protocol", "router_id", "vrf", "isis_area", "status")
        widgets = {
            "protocol": StaticSelect2(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make isis_area required only if protocol is ISIS
        if self.instance and self.instance.protocol == "ISIS":
            self.fields["isis_area"].required = True
        elif self.data.get("protocol") == "ISIS":
            self.fields["isis_area"].required = True
        else:
            self.fields["isis_area"].required = False


class IGPInstanceFilterForm(NautobotFilterForm):
    """Form for filtering IGPInstance objects."""

    model = models.IGPInstance
    device = DynamicModelChoiceField(queryset=models.Device.objects.all(), required=False, label="Device")
    protocol = forms.ChoiceField(
        choices=models.IGPInstance._meta.get_field("protocol").choices, required=False, widget=StaticSelect2()
    )
    router_id = DynamicModelChoiceField(queryset=models.IPAddress.objects.all(), required=False, label="Router ID", query_params={"device_id": "$device"})
    vrf = DynamicModelChoiceField(queryset=models.VRF.objects.all(), required=False, label="VRF")
    isis_area = forms.CharField(required=False, label="ISIS Area")


class IGPInstanceBulkEditForm(NautobotBulkEditForm):
    """Form for bulk editing IGPInstance objects."""

    protocol = forms.ChoiceField(
        choices=models.IGPInstance._meta.get_field("protocol").choices, required=False, widget=StaticSelect2()
    )
    router_id = DynamicModelChoiceField(queryset=models.IPAddress.objects.all(), required=False, label="Router ID", query_params={"device_id": "$device"})
    vrf = DynamicModelChoiceField(queryset=models.VRF.objects.all(), required=False, label="VRF")
    isis_area = forms.CharField(required=False, label="ISIS Area")

    class Meta:
        nullable_fields = ("vrf", "isis_area")


# ISISConfiguration Forms
class ISISConfigurationForm(NautobotModelForm):
    """Form for creating and editing ISISConfiguration objects."""

    instance = DynamicModelChoiceField(
        queryset=models.IGPInstance.objects.filter(protocol="ISIS"), label="IGP Instance"
    )

    class Meta:
        model = models.ISISConfiguration
        fields = ("instance", "system_id", "status")
        help_texts = {"system_id": "Leave blank to auto-generate based on Router ID and ISIS Area."}


class ISISConfigurationFilterForm(NautobotFilterForm):
    """Form for filtering ISISConfiguration objects."""

    model = models.ISISConfiguration
    instance = DynamicModelChoiceField(
        queryset=models.IGPInstance.objects.filter(protocol="ISIS"), required=False, label="IGP Instance"
    )
    system_id = forms.CharField(required=False, label="System ID")


class ISISConfigurationBulkEditForm(NautobotBulkEditForm):
    """Form for bulk editing ISISConfiguration objects."""

    instance = DynamicModelChoiceField(
        queryset=models.IGPInstance.objects.filter(protocol="ISIS"), required=False, label="IGP Instance"
    )

    class Meta:
        nullable_fields = ()

class ISISInterfaceConfigurationForm(NautobotModelForm):
    isis_config = DynamicModelChoiceField(
        queryset=models.ISISConfiguration.objects.all(),
        label="ISIS Configuration"
    )
    interface = DynamicModelChoiceField(
        queryset=models.Interface.objects.all(),
        label="Interface",
        query_params={"device_id": "$isis_config__instance__device"}
    )

    class Meta:
        model = models.ISISInterfaceConfiguration
        fields = ("isis_config", "interface", "circuit_type", "metric", "status")
        widgets = {"circuit_type": StaticSelect2()}

class ISISInterfaceConfigurationFilterForm(NautobotFilterForm):
    model = models.ISISInterfaceConfiguration
    isis_config = DynamicModelChoiceField(
        queryset=models.ISISConfiguration.objects.all(),
        required=False,
        label="ISIS Configuration"
    )
    interface = DynamicModelChoiceField(
        queryset=models.Interface.objects.all(),
        required=False,
        label="Interface",
        query_params={"device_id": "$isis_config__instance__device"}
    )
    circuit_type = forms.ChoiceField(
        choices=models.ISISInterfaceConfiguration._meta.get_field("circuit_type").choices,
        required=False,
        widget=StaticSelect2(),
        label="Circuit Type"
    )
    metric = forms.IntegerField(
        required=False,
        label="Metric"
    )

class ISISInterfaceConfigurationBulkEditForm(NautobotBulkEditForm):
    isis_config = DynamicModelChoiceField(
        queryset=models.ISISConfiguration.objects.all(),
        required=False,
        label="ISIS Configuration"
    )
    interface = DynamicModelChoiceField(
        queryset=models.Interface.objects.all(),
        required=False,
        label="Interface",
        query_params={"device_id": "$isis_config__instance__device"}
    )
    circuit_type = forms.ChoiceField(
        choices=models.ISISInterfaceConfiguration._meta.get_field("circuit_type").choices,
        required=False,
        widget=StaticSelect2(),
        label="Circuit Type"
    )
    metric = forms.IntegerField(
        required=False,
        label="Metric"
    )

    class Meta:
        nullable_fields = ("metric", "status")

# OSPFConfiguration Forms
class OSPFConfigurationForm(NautobotModelForm):
    """Form for creating and editing OSPFConfiguration objects."""

    instance = DynamicModelChoiceField(
        queryset=models.IGPInstance.objects.filter(protocol="OSPF"), label="IGP Instance"
    )

    class Meta:
        model = models.OSPFConfiguration
        fields = ("instance", "process_id", "status")


class OSPFConfigurationFilterForm(NautobotFilterForm):
    """Form for filtering OSPFConfiguration objects."""

    model = models.OSPFConfiguration
    instance = DynamicModelChoiceField(
        queryset=models.IGPInstance.objects.filter(protocol="OSPF"), required=False, label="IGP Instance"
    )
    process_id = forms.IntegerField(required=False, label="Process ID")


class OSPFConfigurationBulkEditForm(NautobotBulkEditForm):
    """Form for bulk editing OSPFConfiguration objects."""

    instance = DynamicModelChoiceField(
        queryset=models.IGPInstance.objects.filter(protocol="OSPF"), required=False, label="IGP Instance"
    )
    process_id = forms.IntegerField(required=False, label="Process ID")

class OSPFInterfaceConfigurationForm(NautobotModelForm):
    ospf_config = DynamicModelChoiceField(
        queryset=models.OSPFConfiguration.objects.all(),
        label="OSPF Configuration"
    )
    interface = DynamicModelChoiceField(
        queryset=Interface.objects.all(),
        label="Interface",
        query_params={"device_id": "$device"},
    )
    area = forms.CharField(label="Area")
    cost = forms.IntegerField(label="Cost")

    class Meta:
        model = models.OSPFInterfaceConfiguration
        fields = ("ospf_config", "interface", "area", "cost", "status")

class OSPFInterfaceConfigurationFilterForm(NautobotFilterForm):
    model = models.OSPFInterfaceConfiguration
    ospf_config = DynamicModelChoiceField(
        queryset=models.OSPFConfiguration.objects.all(),
        required=False,
        label="OSPF Configuration"
    )
    interface = DynamicModelChoiceField(
        queryset=models.Interface.objects.all(),
        required=False,
        label="Interface",
        query_params={"device_id": "$ospf_config__instance__device"}
    )
    area = forms.CharField(
        required=False,
        label="Area"
    )
    cost = forms.IntegerField(
        required=False,
        label="Cost"
    )


class OSPFInterfaceConfigurationBulkEditForm(NautobotBulkEditForm):
    ospf_config = DynamicModelChoiceField(
        queryset=models.OSPFConfiguration.objects.all(),
        required=False,
        label="OSPF Configuration"
    )
    interface = DynamicModelChoiceField(
        queryset=models.Interface.objects.all(),
        required=False,
        label="Interface",
        query_params={"device_id": "$ospf_config__instance__device"}
    )
    area = forms.CharField(
        required=False,
        label="Area"
    )
    cost = forms.IntegerField(
        required=False,
        label="Cost"
    )
    class Meta:
        nullable_fields = ("area", "cost", "status")