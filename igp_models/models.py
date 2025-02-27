"""Models for Igp Models."""
import uuid
# Django imports
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
# Nautobot imports
from nautobot.apps.models import PrimaryModel, BaseModel
from nautobot.dcim.models import Device, Interface
from nautobot.ipam.models import IPAddress, VRF
from nautobot.extras.models import StatusField, StatusModel


def generate_isis_net(device, area_id):
    """Generate a unique IS-IS NET address for a device using the specified area_id."""
    # Use device's primary IP or a UUID-derived value for SystemID
    if device.primary_ip4:
        ip_octets = device.primary_ip4.address.ip.exploded.split(".")
        system_id = f"{ip_octets[0]}{ip_octets[1]}.{ip_octets[2]}{ip_octets[3]}.0000"
    else:
        # Fallback to UUID if no IP is available
        uuid_part = slugify(str(uuid.uuid4()))[:12].replace("-", "")
        system_id = f"{uuid_part[:4]}.{uuid_part[4:8]}.{uuid_part[8:]}"

    # Ensure area_id is stripped of '49.' prefix if present (IS-IS convention)
    if area_id.startswith("49."):
        area_part = area_id[3:]
    else:
        area_part = area_id

    # Construct NET: AFI.Area.SystemID.SEL
    return f"49.{area_part}.{system_id}.00"


class IGPProtocol(models.Model):
    """Supported IGP protocols: OSPF and IS-IS."""
    name = models.CharField(max_length=50, unique=True, help_text=_("Name of the IGP protocol"))

    class Meta:
        verbose_name = _("IGP Protocol")
        verbose_name_plural = _("IGP Protocols")

    def __str__(self):
        return self.name


class IGPRoutingInstance(BaseModel, StatusModel):
    """Represents an IGP process/instance running on a device."""
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        related_name="igp_instances",
        help_text=_("Device running this IGP instance")
    )
    protocol = models.ForeignKey(
        IGPProtocol,
        on_delete=models.PROTECT,
        related_name="instances",
        help_text=_("IGP protocol (OSPF or IS-IS)")
    )
    process_id = models.CharField(
        max_length=50,
        blank=True,
        help_text=_("Process ID (e.g., OSPF process ID, IS-IS instance identifier)")
    )
    router_id = models.ForeignKey(
        IPAddress,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="igp_router_ids",
        help_text=_("Router ID for this IGP instance")
    )
    vrf = models.ForeignKey(
        VRF,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="igp_instances",
        help_text=_("VRF context for this IGP instance")
    )
    isis_net = models.CharField(
        max_length=50,
        blank=True,
        unique=True,
        help_text=_("IS-IS Network Entity Title (NET) address, required if protocol is IS-IS")
    )
    status = StatusField()

    class Meta:
        verbose_name = _("IGP Routing Instance")
        verbose_name_plural = _("IGP Routing Instances")
        unique_together = (("device", "protocol", "process_id", "vrf"),)

    def __str__(self):
        return f"{self.protocol.name} Instance on {self.device.name} (PID: {self.process_id or 'N/A'})"

    def get_primary_area_id(self):
        """Retrieve the area_id from the first associated IGPArea, if any."""
        area = self.areas.first()  # Get the first IGPArea linked to this instance
        return area.area_id if area else "0001"  # Fallback to "0001" if no area exists

    def save(self, *args, **kwargs):
        """Auto-generate IS-IS NET based on the associated area's area_id."""
        if self.protocol.name == "IS-IS" and not self.isis_net:
            area_id = self.get_primary_area_id()
            self.isis_net = generate_isis_net(self.device, area_id)
        super().save(*args, **kwargs)

    def clean(self):
        """Validate IS-IS NET requirement."""
        if self.protocol.name == "IS-IS" and not self.isis_net:
            raise ValidationError(_("IS-IS requires a NET address."))


class IGPArea(BaseModel):
    """Represents an OSPF area or IS-IS level."""
    OSPF_AREA_TYPES = (
        ("normal", _("Normal")),
        ("stub", _("Stub")),
        ("nssa", _("NSSA")),
    )
    ISIS_LEVELS = (
        ("L1", _("Level 1")),
        ("L2", _("Level 2")),
        ("L1L2", _("Level 1-2")),
    )

    routing_instance = models.ForeignKey(
        IGPRoutingInstance,
        on_delete=models.CASCADE,
        related_name="areas",
        help_text=_("Associated IGP routing instance")
    )
    area_id = models.CharField(
        max_length=15,
        help_text=_("Area ID (e.g., '0.0.0.0' for OSPF, '49.0001' for IS-IS)")
    )
    area_type = models.CharField(
        max_length=10,
        choices=OSPF_AREA_TYPES + ISIS_LEVELS,
        blank=True,
        help_text=_("Type of area or level (e.g., 'stub' for OSPF, 'L1' for IS-IS)")
    )

    class Meta:
        verbose_name = _("IGP Area")
        verbose_name_plural = _("IGP Areas")
        unique_together = (("routing_instance", "area_id"),)

    def __str__(self):
        return f"Area {self.area_id} ({self.routing_instance})"

    def clean(self):
        """Validate area_id and area_type based on protocol."""
        protocol_name = self.routing_instance.protocol.name
        if protocol_name == "OSPF":
            try:
                parts = self.area_id.split(".")
                if len(parts) != 4 or not all(0 <= int(p) <= 255 for p in parts):
                    raise ValueError
            except ValueError:
                raise ValidationError(_("OSPF area ID must be in format 'x.x.x.x' (0-255 per octet)."))
            if self.area_type not in [choice[0] for choice in self.OSPF_AREA_TYPES]:
                raise ValidationError(_("Invalid OSPF area type."))
        elif protocol_name == "IS-IS":
            if not self.area_id.startswith("49.") or len(self.area_id) < 3:
                raise ValidationError(_("IS-IS area ID must start with '49.' followed by area identifier."))
            if self.area_type not in [choice[0] for choice in self.ISIS_LEVELS]:
                raise ValidationError(_("Invalid IS-IS level."))


class IGPInterface(BaseModel, StatusModel):
    """Configuration of an interface participating in an IGP."""
    interface = models.ForeignKey(
        Interface,
        on_delete=models.CASCADE,
        related_name="igp_configs",
        help_text=_("Physical or logical interface")
    )
    routing_instance = models.ForeignKey(
        IGPRoutingInstance,
        on_delete=models.CASCADE,
        related_name="interfaces",
        help_text=_("IGP instance this interface belongs to")
    )
    area = models.ForeignKey(
        IGPArea,
        on_delete=models.CASCADE,
        related_name="interfaces",
        help_text=_("Area or level this interface participates in")
    )
    cost = models.PositiveIntegerField(
        default=1,
        help_text=_("Interface cost/metric")
    )
    passive = models.BooleanField(
        default=False,
        help_text=_("Whether this interface is passive (no adjacency formed)")
    )
    status = StatusField()

    class Meta:
        verbose_name = _("IGP Interface")
        verbose_name_plural = _("IGP Interfaces")
        unique_together = (("interface", "routing_instance"),)

    def __str__(self):
        return f"{self.interface} in {self.routing_instance}"

    def clean(self):
        if self.interface.device != self.routing_instance.device:
            raise ValidationError(
                _("Interface device ({self.interface.device}) must match routing instance device ({self.routing_instance.device})")
            )


class IGPAdjacency(BaseModel, StatusModel):
    """Represents an IGP adjacency between two endpoints."""
    local_interface = models.ForeignKey(
        IGPInterface,
        on_delete=models.CASCADE,
        related_name="local_adjacencies",
        help_text=_("Local interface forming the adjacency")
    )
    remote_ip = models.ForeignKey(
        IPAddress,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="igp_adjacencies",
        help_text=_("Remote neighbor IP address")
    )
    remote_device = models.ForeignKey(
        Device,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="igp_remote_adjacencies",
        help_text=_("Remote device (optional, if modeled in Nautobot)")
    )
    status = StatusField()

    def __str__(self):
        return f"Adjacency from {self.local_interface} to {self.remote_ip or self.remote_device or 'Unknown'}"