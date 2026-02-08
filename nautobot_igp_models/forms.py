"""Forms for nautobot_igp_models."""

import logging

from django import forms
from nautobot.apps.forms import (
    DynamicModelChoiceField,
    NautobotBulkEditForm,
    NautobotFilterForm,
    NautobotModelForm,
    StaticSelect2,
    TagsBulkEditFormMixin,
)
from nautobot.dcim.models import Device, Interface
from nautobot.ipam.models import VRF, IPAddress

from nautobot_igp_models import models

logger = logging.getLogger(__name__)


class IGPRoutingInstanceForm(NautobotModelForm):  # pylint: disable=too-many-ancestors
    """IGPRoutingInstance creation/edit form."""

    device = DynamicModelChoiceField(queryset=Device.objects.all(), label="Device")
    router_id = DynamicModelChoiceField(
        queryset=IPAddress.objects.all(), label="Router ID", query_params={"device_id": "$device"}
    )
    vrf = DynamicModelChoiceField(queryset=VRF.objects.all(), required=False, label="VRF")

    class Meta:
        """Meta attributes."""

        model = models.IGPRoutingInstance
        fields = ("name", "description", "device", "protocol", "router_id", "vrf", "isis_area", "status")
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


class IGPRoutingInstanceBulkEditForm(TagsBulkEditFormMixin, NautobotBulkEditForm):  # pylint: disable=too-many-ancestors
    """IGPRoutingInstance bulk edit form."""

    pk = forms.ModelMultipleChoiceField(
        queryset=models.IGPRoutingInstance.objects.all(), widget=forms.MultipleHiddenInput
    )
    description = forms.CharField(required=False)
    protocol = forms.ChoiceField(
        choices=models.IGPRoutingInstance._meta.get_field("protocol").choices, required=False, widget=StaticSelect2()
    )
    router_id = DynamicModelChoiceField(
        queryset=IPAddress.objects.all(), required=False, label="Router ID", query_params={"device_id": "$device"}
    )
    vrf = DynamicModelChoiceField(queryset=VRF.objects.all(), required=False, label="VRF")
    isis_area = forms.CharField(required=False, label="ISIS Area")

    class Meta:
        """Meta attributes."""

        nullable_fields = ["description", "vrf", "isis_area"]


class IGPRoutingInstanceFilterForm(NautobotFilterForm):
    """Filter form to filter searches."""

    model = models.IGPRoutingInstance
    field_order = ["q", "name"]

    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Slug.",
    )
    name = forms.CharField(required=False, label="Name")


# ISISConfiguration Forms
class ISISConfigurationForm(NautobotModelForm):
    """Form for creating and editing ISISConfiguration objects."""

    instance = DynamicModelChoiceField(
        queryset=models.IGPRoutingInstance.objects.filter(protocol="ISIS"),
        label="IGP Instance",
        required=True,
    )

    class Meta:
        model = models.ISISConfiguration
        fields = (
            "name",
            "instance",
            "system_id",
            "status",
            "default_metric",
            "default_hello_interval",
            "default_hello_multiplier",
            "default_priority",
        )
        help_texts = {
            "system_id": "Enter a value in the format XXXX.XXXX.XXXX (e.g., 0192.0003.0002). A suggestion will be provided based on Router ID and ISIS Area once an IGP Instance is selected.",
            "default_metric": "Default metric inherited by interfaces unless overridden (leave blank for interface-specific values)",
            "default_hello_interval": "Default hello interval inherited by interfaces (leave blank for protocol defaults or config context)",
            "default_hello_multiplier": "Default hello multiplier inherited by interfaces (leave blank for protocol defaults or config context)",
            "default_priority": "Default DIS priority inherited by interfaces (leave blank for protocol defaults or config context)",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        logger.debug("Initializing ISISConfigurationForm")
        logger.debug(f"Self.instance (ISISConfiguration): {self.instance}")
        logger.debug(f"Form data: {self.data}")

        suggested_net = None
        selected_instance = None

        if self.instance and self.instance.pk and hasattr(self.instance, "instance"):
            try:
                selected_instance = self.instance.instance
                logger.debug(f"Selected instance from self.instance: {selected_instance}")
            except models.IGPRoutingInstance.DoesNotExist:
                logger.debug("No related IGPRoutingInstance found on self.instance")
                selected_instance = None

        if not selected_instance and "instance" in self.data:
            instance_id = self.data.get("instance")
            logger.debug(f"Instance ID from form data: {instance_id}")
            if instance_id:
                try:
                    selected_instance = models.IGPRoutingInstance.objects.get(pk=instance_id)
                    logger.debug(f"Selected instance from form data: {selected_instance}")
                except (ValueError, models.IGPRoutingInstance.DoesNotExist):
                    logger.debug(f"Failed to retrieve IGPRoutingInstance with ID: {instance_id}")
                    selected_instance = None

        if selected_instance:
            router_id = getattr(selected_instance, "router_id", None)
            isis_area = getattr(selected_instance, "isis_area", None)
            logger.debug(f"Router ID: {router_id}")
            logger.debug(f"Router ID string representation: {str(router_id) if router_id else None}")
            logger.debug(f"ISIS Area: {isis_area}")

            if router_id and isis_area:
                try:
                    suggested_net = self.generate_full_net(router_id, isis_area)
                    logger.debug(f"Generated full NET suggestion: {suggested_net}")
                except ValueError as e:
                    logger.debug(f"Error generating NET suggestion: {str(e)}")
                    suggested_net = None
            else:
                logger.debug("Cannot generate NET suggestion: router_id or isis_area missing")
        else:
            logger.debug("No selected instance available to generate NET suggestion")

        if suggested_net:
            self.fields["system_id"].help_text = (
                "Enter the full NET in the format AA.BBBB.XXXX.XXXX.XXXX.CC (e.g., 49.0001.0192.0168.0302.00). "
                f"Suggested NET: {suggested_net}"
            )
            logger.debug(f"Updated help text with NET suggestion: {self.fields['system_id'].help_text}")
        else:
            self.fields["system_id"].help_text = (
                "Enter the full NET in the format AA.BBBB.XXXX.XXXX.XXXX.CC (e.g., 49.0001.0192.0168.0302.00). "
                "Select an IGP Instance with a Router ID and ISIS Area to see a suggested NET."
            )
            logger.debug(f"Set default help text: {self.fields['system_id'].help_text}")

    def generate_full_net(self, router_id, isis_area):
        """Generate the full NET (Area ID + System ID + NSEL).

        Based on router_id and isis_area. Returns a string in the format 'AA.BBBB.XXXX.XXXX.XXXX.CC'.
        """
        logger.debug(f"Generating full NET with router_id: {router_id}, isis_area: {isis_area}")

        # Step 1: Get the Area Identifier (e.g., "49.0001")
        area_id = isis_area  # Use the isis_area directly (e.g., "49.0001")
        logger.debug(f"Area Identifier: {area_id}")

        # Step 2: Generate the System ID based on router_id
        router_id_str = str(router_id)  # e.g., "192.168.3.2/24"
        logger.debug(f"Router ID string representation: {router_id_str}")

        # Strip the subnet mask (e.g., "/24") if present
        ip_address = router_id_str.split("/")[0]  # Gets "192.168.3.2"
        logger.debug(f"IP address after stripping subnet: {ip_address}")

        # Split the IP address into octets
        octets = ip_address.split(".")
        if len(octets) != 4:
            raise ValueError("Router ID format invalid; expected IPv4 address.")

        # Convert octets to integers
        octet_values = [int(octet) for octet in octets]
        logger.debug(f"Octet values: {octet_values}")

        # Map octets to three 4-digit segments for System ID
        # First segment: First octet (e.g., 192 -> 0192)
        first_segment = f"{octet_values[0]:04d}"[-4:]  # e.g., "0192"
        # Second segment: Second octet (e.g., 168 -> 0168)
        second_segment = f"{octet_values[1]:04d}"[-4:]  # e.g., "0168"
        # Third segment: Third and fourth octets (e.g., 3, 2 -> 0302)
        third_segment = f"{octet_values[2]:02d}{octet_values[3]:02d}"[-4:]  # e.g., "0302"

        logger.debug(f"System ID segments: {first_segment}, {second_segment}, {third_segment}")

        # Combine System ID
        system_id = f"{first_segment}.{second_segment}.{third_segment}"

        # Step 3: Combine Area ID, System ID, and NSEL
        nsel = "00"  # Fixed NSEL for IS-IS routing
        full_net = f"{area_id}.{system_id}.{nsel}"
        return full_net


class ISISConfigurationFilterForm(NautobotFilterForm):
    """Form for filtering ISISConfiguration objects."""

    model = models.ISISConfiguration
    instance = DynamicModelChoiceField(
        queryset=models.IGPRoutingInstance.objects.filter(protocol="ISIS"), required=False, label="IGP Instance"
    )
    system_id = forms.CharField(required=False, label="System ID")


class ISISConfigurationBulkEditForm(NautobotBulkEditForm):
    """Form for bulk editing ISISConfiguration objects."""

    pk = forms.ModelMultipleChoiceField(
        queryset=models.ISISConfiguration.objects.all(), widget=forms.MultipleHiddenInput
    )
    instance = DynamicModelChoiceField(
        queryset=models.IGPRoutingInstance.objects.filter(protocol="ISIS"), required=False, label="IGP Instance"
    )

    class Meta:
        nullable_fields = ()


# ISISInterfaceConfiguration Forms
class ISISInterfaceConfigurationForm(NautobotModelForm):
    isis_config = DynamicModelChoiceField(
        queryset=models.ISISConfiguration.objects.all(),
        label="ISIS Configuration",
        required=True,
    )

    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        label="Device",
        required=True,
    )

    interface = DynamicModelChoiceField(
        queryset=Interface.objects.none(),
        label="Interface",
        required=True,
        to_field_name="id",
        query_params={"device_id": "$device"},
    )

    class Meta:
        model = models.ISISInterfaceConfiguration
        fields = ("name", "isis_config", "device", "interface", "circuit_type", "metric", "status")
        widgets = {"circuit_type": StaticSelect2()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        device = None

        # If editing an existing ISISInterfaceConfiguration
        if self.instance and self.instance.pk and hasattr(self.instance, "device") and self.instance.device:
            device = self.instance.device

        # If creating a new configuration, get the device from form data
        elif "device" in self.data:
            try:
                device_id = int(self.data.get("device"))
                device = Device.objects.get(pk=device_id)
            except (ValueError, Device.DoesNotExist):
                pass  # Keep device as None

        # Ensure queryset for interface is properly set
        if device:
            self.fields["interface"].queryset = Interface.objects.filter(device=device)
        else:
            self.fields["interface"].queryset = Interface.objects.none()  # Prevents form error


class ISISInterfaceConfigurationFilterForm(NautobotFilterForm):
    model = models.ISISInterfaceConfiguration

    isis_config = DynamicModelChoiceField(
        queryset=models.ISISConfiguration.objects.all(),
        required=False,
        label="ISIS Configuration",
        to_field_name="name",
    )

    interface = DynamicModelChoiceField(
        queryset=Interface.objects.all(),
        required=False,
        label="Interface",
        query_params={"device_id": "$isis_config__instance__device"},
    )

    circuit_type = forms.MultipleChoiceField(
        choices=models.ISISInterfaceConfiguration._meta.get_field("circuit_type").choices,
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-control"}),
    )

    metric = forms.IntegerField(
        required=False, label="Metric", widget=forms.NumberInput(attrs={"class": "form-control"})
    )

    class Meta:
        fields = ["isis_config_name", "interface", "circuit_type", "metric", "status"]


class ISISInterfaceConfigurationBulkEditForm(NautobotBulkEditForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=models.ISISInterfaceConfiguration.objects.all(), widget=forms.MultipleHiddenInput
    )
    isis_config = DynamicModelChoiceField(
        queryset=models.ISISConfiguration.objects.all(), required=False, label="ISIS Configuration"
    )
    interface = DynamicModelChoiceField(
        queryset=models.Interface.objects.all(),
        required=False,
        label="Interface",
        query_params={"device_id": "$isis_config__instance__device"},
    )
    circuit_type = forms.ChoiceField(
        choices=models.ISISInterfaceConfiguration._meta.get_field("circuit_type").choices,
        required=False,
        widget=StaticSelect2(),
        label="Circuit Type",
    )
    metric = forms.IntegerField(required=False, label="Metric")

    class Meta:
        nullable_fields = ("metric", "status")


# OSPFConfiguration Forms
class OSPFConfigurationForm(NautobotModelForm):
    """Form for creating and editing OSPFConfiguration objects."""

    instance = DynamicModelChoiceField(
        queryset=models.IGPRoutingInstance.objects.filter(protocol="OSPF"), label="IGP Instance"
    )

    class Meta:
        model = models.OSPFConfiguration
        fields = (
            "name",
            "instance",
            "process_id",
            "status",
            "default_cost",
            "default_hello_interval",
            "default_dead_interval",
            "default_priority",
        )
        help_texts = {
            "default_cost": "Default cost inherited by interfaces unless overridden (leave blank for interface-specific values)",
            "default_hello_interval": "Default hello interval inherited by interfaces (leave blank for protocol defaults or config context)",
            "default_dead_interval": "Default dead interval inherited by interfaces (leave blank for protocol defaults or config context)",
            "default_priority": "Default router priority inherited by interfaces (leave blank for protocol defaults or config context)",
        }


class OSPFConfigurationFilterForm(NautobotFilterForm):
    """Form for filtering OSPFConfiguration objects."""

    model = models.OSPFConfiguration
    instance = DynamicModelChoiceField(
        queryset=models.IGPRoutingInstance.objects.filter(protocol="OSPF"), required=False, label="IGP Instance"
    )
    process_id = forms.IntegerField(required=False, label="Process ID")


class OSPFConfigurationBulkEditForm(NautobotBulkEditForm):
    """Form for bulk editing OSPFConfiguration objects."""

    pk = forms.ModelMultipleChoiceField(
        queryset=models.OSPFConfiguration.objects.all(), widget=forms.MultipleHiddenInput
    )
    instance = DynamicModelChoiceField(
        queryset=models.IGPRoutingInstance.objects.filter(protocol="OSPF"), required=False, label="IGP Instance"
    )
    process_id = forms.IntegerField(required=False, label="Process ID")

    class Meta:
        nullable_fields = ()


# OSPFInterfaceConfiguration Forms
class OSPFInterfaceConfigurationForm(NautobotModelForm):
    ospf_config = DynamicModelChoiceField(queryset=models.OSPFConfiguration.objects.all(), label="OSPF Configuration")
    interface = DynamicModelChoiceField(
        queryset=models.Interface.objects.all(),
        label="Interface",
        query_params={"device_id": "$ospf_config__instance__device"},
    )
    area = forms.CharField(required=False, label="Area")
    cost = forms.IntegerField(required=False, label="Cost")

    class Meta:
        model = models.OSPFInterfaceConfiguration
        fields = ("name", "ospf_config", "interface", "area", "cost", "status")


class OSPFInterfaceConfigurationFilterForm(NautobotFilterForm):
    model = models.OSPFInterfaceConfiguration
    ospf_config = DynamicModelChoiceField(
        queryset=models.OSPFConfiguration.objects.all(), required=False, label="OSPF Configuration"
    )
    interface = DynamicModelChoiceField(
        queryset=models.Interface.objects.all(),
        required=False,
        label="Interface",
        query_params={"device_id": "$ospf_config__instance__device"},
    )
    area = forms.CharField(required=False, label="Area")
    cost = forms.IntegerField(required=False, label="Cost")


class OSPFInterfaceConfigurationBulkEditForm(NautobotBulkEditForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=models.OSPFInterfaceConfiguration.objects.all(), widget=forms.MultipleHiddenInput
    )
    ospf_config = DynamicModelChoiceField(
        queryset=models.OSPFConfiguration.objects.all(), required=False, label="OSPF Configuration"
    )
    interface = DynamicModelChoiceField(
        queryset=models.Interface.objects.all(),
        required=False,
        label="Interface",
        query_params={"device_id": "$ospf_config__instance__device"},
    )
    area = forms.CharField(required=False, label="Area")
    cost = forms.IntegerField(required=False, label="Cost")

    class Meta:
        nullable_fields = ("area", "cost", "status")
