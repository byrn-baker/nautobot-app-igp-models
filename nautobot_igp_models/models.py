"""Models for Nautobot IGP Models."""

import logging

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

# Django imports
from django.db import models

# Nautobot imports
from nautobot.apps.models import PrimaryModel
from nautobot.dcim.models import Interface
from nautobot.extras.models import StatusField
from nautobot.extras.utils import extras_features

logger = logging.getLogger(__name__)

# Validator for ISIS Area format (e.g., 49, 49.0001, 49.0000.0001)
isis_area_validator = RegexValidator(
    regex=r"^(\d{1,4})(\.\d{1,4}){0,6}$",
    message="ISIS Area must be in the format '49', '49.0001', etc., with 1-7 segments of 1-4 digits each.",
)


def validate_isis_area(value):
    """Additional validation for ISIS Area beyond regex."""
    if value:
        parts = value.split(".")
        if len(parts) > 7:
            raise ValidationError("ISIS Area cannot exceed 7 segments.")
        total_length = sum(len(part) for part in parts)
        if total_length > 13:
            raise ValidationError("ISIS Area cannot exceed 13 bytes.")


@extras_features(
    "custom_fields",
    "custom_links",
    "custom_validators",
    "export_templates",
    "graphql",
    "relationships",
    "statuses",
    "webhooks",
)
class IGPRoutingInstance(PrimaryModel):  # pylint: disable=too-many-ancestors
    """Base model for Nautobot IGP Models app."""

    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=200, blank=True)
    device = models.ForeignKey(
        to="dcim.Device",
        on_delete=models.PROTECT,
        related_name="igp_routing_instances",
        verbose_name="Device",
    )

    protocol = models.CharField(
        max_length=4, choices=[("ISIS", "ISIS"), ("OSPF", "OSPF")], help_text="The IGP protocol type."
    )

    router_id = models.ForeignKey(
        to="ipam.IPAddress",
        verbose_name="Router ID",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )

    vrf = models.ForeignKey(
        to="ipam.VRF",
        verbose_name="VRF",
        related_name="igp_routing_instances",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )

    isis_area = models.CharField(
        max_length=13,
        blank=True,
        null=True,
        validators=[isis_area_validator, validate_isis_area],
        help_text="ISIS Area (e.g., 49.0001) - required only for ISIS protocol.",
    )

    status = StatusField(null=True)

    def __str__(self):
        return f"{self.protocol} on {self.device}"

    class Meta:
        """Meta class."""

        ordering = ["name"]
        verbose_name = "IGP Routing Instance"
        verbose_name_plural = "IGP Routing Instances"
        unique_together = ["device", "protocol", "vrf"]

    def clean(self):
        """Ensure isis_area is populated only for ISIS and required when ISIS is selected."""
        if self.protocol == "ISIS" and not self.isis_area:
            raise ValidationError({"isis_area": "ISIS Area is required when protocol is ISIS."})
        elif self.protocol == "OSPF" and self.isis_area:
            raise ValidationError({"isis_area": "ISIS Area should not be set for OSPF protocol."})
        if not self.status:
            raise ValidationError("Status must be defined for the IGP Routing Instance.")
        super().clean()


@extras_features(
    "custom_fields",
    "custom_links",
    "custom_validators",
    "export_templates",
    "graphql",
    "relationships",
    "statuses",
    "webhooks",
)
class ISISConfiguration(PrimaryModel):
    """ISIS-specific configuration model."""

    name = models.CharField(max_length=100)
    instance = models.ForeignKey("IGPRoutingInstance", on_delete=models.CASCADE)
    system_id = models.CharField(max_length=50, blank=True)
    status = StatusField(null=True)

    class Meta:
        unique_together = ["instance", "name"]

    def save(self, *args, **kwargs):
        """Save the ISIS configuration and auto-generate NET if system_id is empty."""
        if not self.system_id:  # Only generate if system_id is empty
            try:
                self.system_id = self.generate_full_net()
                logger.debug(f"Auto-generated full NET during save: {self.system_id}")
            except ValueError as e:
                logger.error(f"Error generating full NET during save: {str(e)}")
                self.system_id = ""  # Leave blank if generation fails
        super().save(*args, **kwargs)

    def generate_full_net(self):
        """Generate the full NET (Area ID + System ID + NSEL).

        Based on instance's router_id and isis_area. Returns a string in the format 'AA.BBBB.XXXX.XXXX.XXXX.CC'.
        """
        if not self.instance or not self.instance.router_id or not self.instance.isis_area:
            raise ValueError("Cannot generate NET: No instance, router_id, or isis_area available.")

        router_id = self.instance.router_id
        isis_area = self.instance.isis_area
        logger.debug(f"Router ID string in generate_full_net: {str(router_id)}")
        logger.debug(f"ISIS Area in generate_full_net: {isis_area}")

        # Step 1: Get the Area Identifier (e.g., "49.0001")
        area_id = isis_area  # Use the isis_area directly (e.g., "49.0001")
        logger.debug(f"Area Identifier: {area_id}")

        # Step 2: Generate the System ID based on router_id
        router_id_str = str(router_id).split("/")[0]  # Get "192.168.3.2"
        logger.debug(f"Router ID string after stripping subnet: {router_id_str}")

        # Split into octets
        octets = router_id_str.split(".")
        if len(octets) != 4:
            raise ValueError("Router ID format invalid; expected IPv4 address.")

        # Convert octets to integers
        octet_values = [int(octet) for octet in octets]
        logger.debug(f"Octet values in generate_full_net: {octet_values}")

        # Map octets to three 4-digit segments for System ID
        first_segment = f"{octet_values[0]:04d}"[-4:]  # e.g., "0192"
        second_segment = f"{octet_values[1]:04d}"[-4:]  # e.g., "0168"
        third_segment = f"{octet_values[2]:02d}{octet_values[3]:02d}"[-4:]  # e.g., "0302"

        logger.debug(f"System ID segments in generate_full_net: {first_segment}, {second_segment}, {third_segment}")

        # Combine System ID
        system_id = f"{first_segment}.{second_segment}.{third_segment}"

        # Step 3: Combine Area ID, System ID, and NSEL
        nsel = "00"  # Fixed NSEL for IS-IS routing
        full_net = f"{area_id}.{system_id}.{nsel}"
        return full_net

    def __str__(self):
        return self.name or str(self.id)


@extras_features(
    "custom_fields",
    "custom_links",
    "custom_validators",
    "export_templates",
    "graphql",
    "relationships",
    "statuses",
    "webhooks",
)
class ISISInterfaceConfiguration(PrimaryModel):
    """ISIS interface-level configuration model."""

    name = models.CharField(max_length=100)

    isis_config = models.ForeignKey(
        ISISConfiguration, on_delete=models.CASCADE, related_name="interface_configurations"
    )

    device = models.ForeignKey(
        "dcim.Device",
        on_delete=models.CASCADE,
        related_name="isis_interface_configurations",
        help_text="The device this ISIS interface belongs to.",
    )

    interface = models.ForeignKey(Interface, on_delete=models.CASCADE, related_name="isis_configurations")
    circuit_type = models.CharField(
        max_length=10,
        choices=[("L1", "Level-1"), ("L2", "Level-2"), ("L1L2", "Level-1-2")],
        default="L1L2",
        help_text="ISIS circuit type for this interface.",
    )
    metric = models.PositiveIntegerField(default=10, help_text="ISIS metric for this interface.")
    status = StatusField(null=True)

    class Meta:
        unique_together = ("isis_config", "interface")
        verbose_name = "ISIS Interface Configuration"
        verbose_name_plural = "ISIS Interface Configurations"

    def __str__(self):
        return f"ISIS {self.circuit_type} on {self.interface}"


@extras_features(
    "custom_fields",
    "custom_links",
    "custom_validators",
    "export_templates",
    "graphql",
    "relationships",
    "statuses",
    "webhooks",
)
class OSPFConfiguration(PrimaryModel):
    """OSPF-specific configuration."""

    name = models.CharField(max_length=100)

    instance = models.ForeignKey(
        IGPRoutingInstance,
        on_delete=models.CASCADE,
        limit_choices_to={"protocol": "OSPF"},
        related_name="ospf_configurations",
    )
    process_id = models.PositiveIntegerField(default=1, help_text="OSPF Process ID.")
    status = StatusField(null=True)

    class Meta:
        unique_together = ("instance", "process_id")
        verbose_name = "OSPF Configuration"
        verbose_name_plural = "OSPF Configurations"

    def __str__(self):
        return f"OSPF {self.process_id} on {self.instance.device}"


@extras_features(
    "custom_fields",
    "custom_links",
    "custom_validators",
    "export_templates",
    "graphql",
    "relationships",
    "statuses",
    "webhooks",
)
class OSPFInterfaceConfiguration(PrimaryModel):
    """OSPF interface-level configuration model."""

    name = models.CharField(max_length=100)

    ospf_config = models.ForeignKey(
        OSPFConfiguration, on_delete=models.CASCADE, related_name="interface_configurations"
    )
    interface = models.ForeignKey(Interface, on_delete=models.CASCADE, related_name="ospf_configurations")
    area = models.CharField(max_length=15, help_text="OSPF Area for this interface (e.g., 0.0.0.0)")
    cost = models.PositiveIntegerField(default=1, help_text="OSPF cost for this interface.")
    status = StatusField(null=True)

    class Meta:
        unique_together = ("ospf_config", "interface")
        verbose_name = "OSPF Interface Configuration"
        verbose_name_plural = "OSPF Interface Configurations"

    def __str__(self):
        return f"OSPF Area {self.area} on {self.interface}"
