"""Forms for nautobot_igp_models."""

from django import forms
from nautobot.apps.forms import NautobotBulkEditForm, NautobotFilterForm, NautobotModelForm, TagsBulkEditFormMixin, DynamicModelChoiceField, StaticSelect2
from nautobot.dcim.models import Device, Interface
from nautobot.ipam.models import IPAddress, VRF
from nautobot_igp_models import models


class IGPRoutingInstanceForm(NautobotModelForm):  # pylint: disable=too-many-ancestors
    """IGPRoutingInstance creation/edit form."""

    device = DynamicModelChoiceField(queryset=Device.objects.all(), label="Device")
    router_id = DynamicModelChoiceField(queryset=IPAddress.objects.all(), label="Router ID", query_params={"device_id": "$device"})
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
    router_id = DynamicModelChoiceField(queryset=IPAddress.objects.all(), required=False, label="Router ID", query_params={"device_id": "$device"})
    vrf = DynamicModelChoiceField(queryset=VRF.objects.all(), required=False, label="VRF")
    isis_area = forms.CharField(required=False, label="ISIS Area")

    class Meta:
        """Meta attributes."""

        nullable_fields = [
            "description",
            "vrf", 
            "isis_area"
        ]


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
        fields = ("name", "instance", "system_id", "status")
        help_texts = {
            "system_id": "Enter a value in the format XXXX.XXXX.XXXX (e.g., 0192.0003.0002). A suggestion will be provided based on Router ID and ISIS Area once an IGP Instance is selected."
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        print("=== Initializing ISISConfigurationForm ===")
        print("Self.instance (ISISConfiguration):", self.instance)
        print("Form data:", self.data)

        suggested_net = None
        selected_instance = None

        if self.instance and self.instance.pk and hasattr(self.instance, 'instance'):
            try:
                selected_instance = self.instance.instance
                print("Selected instance from self.instance:", selected_instance)
            except models.IGPRoutingInstance.DoesNotExist:
                print("No related IGPRoutingInstance found on self.instance")
                selected_instance = None

        if not selected_instance and "instance" in self.data:
            instance_id = self.data.get("instance")
            print("Instance ID from form data:", instance_id)
            if instance_id:
                try:
                    selected_instance = models.IGPRoutingInstance.objects.get(pk=instance_id)
                    print("Selected instance from form data:", selected_instance)
                except (ValueError, models.IGPRoutingInstance.DoesNotExist):
                    print("Failed to retrieve IGPRoutingInstance with ID:", instance_id)
                    selected_instance = None

        if selected_instance:
            router_id = getattr(selected_instance, 'router_id', None)
            isis_area = getattr(selected_instance, 'isis_area', None)
            print("Router ID:", router_id)
            print("Router ID string representation:", str(router_id) if router_id else None)
            print("ISIS Area:", isis_area)

            if router_id and isis_area:
                try:
                    suggested_net = self.generate_full_net(router_id, isis_area)
                    print("Generated full NET suggestion:", suggested_net)
                except ValueError as e:
                    print("Error generating NET suggestion:", str(e))
                    suggested_net = None
            else:
                print("Cannot generate NET suggestion: router_id or isis_area missing")
        else:
            print("No selected instance available to generate NET suggestion")

        if suggested_net:
            self.fields["system_id"].help_text = (
                "Enter the full NET in the format AA.BBBB.XXXX.XXXX.XXXX.CC (e.g., 49.0001.0192.0168.0302.00). "
                f"Suggested NET: {suggested_net}"
            )
            print("Updated help text with NET suggestion:", self.fields["system_id"].help_text)
        else:
            self.fields["system_id"].help_text = (
                "Enter the full NET in the format AA.BBBB.XXXX.XXXX.XXXX.CC (e.g., 49.0001.0192.0168.0302.00). "
                "Select an IGP Instance with a Router ID and ISIS Area to see a suggested NET."
            )
            print("Set default help text:", self.fields["system_id"].help_text)

    def generate_full_net(self, router_id, isis_area):
        """
        Generate the full NET (Area ID + System ID + NSEL) based on router_id and isis_area.
        Returns a string in the format 'AA.BBBB.XXXX.XXXX.XXXX.CC'.
        """
        print("Generating full NET with router_id:", router_id, "isis_area:", isis_area)

        # Step 1: Get the Area Identifier (e.g., "49.0001")
        area_id = isis_area  # Use the isis_area directly (e.g., "49.0001")
        print("Area Identifier:", area_id)

        # Step 2: Generate the System ID based on router_id
        router_id_str = str(router_id)  # e.g., "192.168.3.2/24"
        print("Router ID string representation:", router_id_str)

        # Strip the subnet mask (e.g., "/24") if present
        ip_address = router_id_str.split("/")[0]  # Gets "192.168.3.2"
        print("IP address after stripping subnet:", ip_address)

        # Split the IP address into octets
        octets = ip_address.split(".")
        if len(octets) != 4:
            raise ValueError("Router ID format invalid; expected IPv4 address.")
        
        # Convert octets to integers
        octet_values = [int(octet) for octet in octets]
        print("Octet values:", octet_values)

        # Map octets to three 4-digit segments for System ID
        # First segment: First octet (e.g., 192 -> 0192)
        first_segment = f"{octet_values[0]:04d}"[-4:]  # e.g., "0192"
        # Second segment: Second octet (e.g., 168 -> 0168)
        second_segment = f"{octet_values[1]:04d}"[-4:]  # e.g., "0168"
        # Third segment: Third and fourth octets (e.g., 3, 2 -> 0302)
        third_segment = f"{octet_values[2]:02d}{octet_values[3]:02d}"[-4:]  # e.g., "0302"

        print("System ID segments:", first_segment, second_segment, third_segment)

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

    instance = DynamicModelChoiceField(
        queryset=models.IGPRoutingInstance.objects.filter(protocol="ISIS"), required=False, label="IGP Instance"
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
        queryset=models.IGPRoutingInstance.objects.filter(protocol="OSPF"), 
        label="IGP Instance"
    )

    class Meta:
        model = models.OSPFConfiguration
        fields = ("instance", "process_id", "status")


class OSPFConfigurationFilterForm(NautobotFilterForm):
    """Form for filtering OSPFConfiguration objects."""

    model = models.OSPFConfiguration
    instance = DynamicModelChoiceField(
        queryset=models.IGPRoutingInstance.objects.filter(protocol="OSPF"), required=False, label="IGP Instance"
    )
    process_id = forms.IntegerField(required=False, label="Process ID")


class OSPFConfigurationBulkEditForm(NautobotBulkEditForm):
    """Form for bulk editing OSPFConfiguration objects."""

    instance = DynamicModelChoiceField(
        queryset=models.IGPRoutingInstance.objects.filter(protocol="OSPF"), required=False, label="IGP Instance"
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
        query_params={"device_id": "$ospf_config__instance__device"}
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