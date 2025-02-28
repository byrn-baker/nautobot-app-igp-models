"""Models for Igp Models."""

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.contenttypes.models import ContentType
from nautobot.apps.models import PrimaryModel
from nautobot.dcim.models import Device, Interface
from nautobot.extras.models import StatusField
from nautobot.extras.utils import extras_features
from nautobot.ipam.models import VRF, IPAddress

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


@extras_features("custom_fields", "graphql", "statuses", "relationships")
class IGPInstance(PrimaryModel):
    """Represents an IGP routing instance on a device."""

    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="igp_instances")
    protocol = models.CharField(
        max_length=4, choices=[("ISIS", "ISIS"), ("OSPF", "OSPF")], help_text="The IGP protocol type."
    )
    router_id = models.ForeignKey(IPAddress, on_delete=models.PROTECT, help_text="Router ID IP Address.")
    vrf = models.ForeignKey(
        VRF, on_delete=models.PROTECT, blank=True, null=True, help_text="Optional VRF for this IGP instance."
    )
    isis_area = models.CharField(
        max_length=13,
        blank=True,
        null=True,
        validators=[isis_area_validator, validate_isis_area],
        help_text="ISIS Area (e.g., 49.0001) - required only for ISIS protocol.",
    )
    status = StatusField(null=True)

    class Meta:
        unique_together = ("device", "protocol", "vrf")
        verbose_name = "IGP Instance"
        verbose_name_plural = "IGP Instances"

    def __str__(self):
        return f"{self.protocol} on {self.device}"

    def clean(self):
        """Ensure isis_area is populated only for ISIS and required when ISIS is selected."""
        if self.protocol == "ISIS" and not self.isis_area:
            raise ValidationError({"isis_area": "ISIS Area is required when protocol is ISIS."})
        elif self.protocol == "OSPF" and self.isis_area:
            raise ValidationError({"isis_area": "ISIS Area should not be set for OSPF protocol."})
        super().clean()


@extras_features("custom_fields", "graphql", "statuses", "relationships")
class ISISConfiguration(PrimaryModel):
    """ISIS-specific configuration."""

    instance = models.ForeignKey(
        IGPInstance, on_delete=models.CASCADE, limit_choices_to={"protocol": "ISIS"}, related_name="isis_configurations"
    )
    system_id = models.CharField(
        max_length=19,  # e.g., 49.0001.1921.6800.1001.00
        unique=True,
        help_text="ISIS System ID (e.g., 49.0001.1921.6800.1001.00)",
    )
    status = StatusField(null=True)

    class Meta:
        verbose_name = "ISIS Configuration"
        verbose_name_plural = "ISIS Configurations"

    def save(self, *args, **kwargs):
        """Auto-populate system_id based on router_id and isis_area if not provided."""
        if not self.system_id:
            self.system_id = self.generate_system_id()
        super().save(*args, **kwargs)

    def generate_system_id(self):
        """Generate ISIS System ID from router_id and isis_area."""
        router_id_str = self.instance.router_id.address.split("/")[0].replace(".", "")
        # Pad to 12 digits if needed, e.g., 192168001001
        router_id_str = router_id_str.zfill(12)
        # Format: aa.aaaa.bbbb.cccc.dddd.00 (area + router ID)
        area_part = self.instance.isis_area.replace(".", "")
        system_id = f"{area_part}.{router_id_str[:4]}.{router_id_str[4:8]}.{router_id_str[8:]}.00"
        return system_id

    def __str__(self):
        return self.system_id

@extras_features("custom_fields", "graphql", "statuses", "relationships")
class ISISInterfaceConfiguration(PrimaryModel):
    isis_config = models.ForeignKey(
        ISISConfiguration,
        on_delete=models.CASCADE,
        related_name="interface_configurations"
    )
    interface = models.ForeignKey(
        Interface,
        on_delete=models.CASCADE,
        related_name="isis_configurations"
    )
    circuit_type = models.CharField(
        max_length=10,
        choices=[("L1", "Level-1"), ("L2", "Level-2"), ("L1L2", "Level-1-2")],
        default="L1L2",
        help_text="ISIS circuit type for this interface."
    )
    metric = models.PositiveIntegerField(
        default=10,
        help_text="ISIS metric for this interface."
    )
    status = StatusField(null=True)

    class Meta:
        unique_together = ("isis_config", "interface")
        verbose_name = "ISIS Interface Configuration"
        verbose_name_plural = "ISIS Interface Configurations"

    def __str__(self):
        return f"ISIS {self.circuit_type} on {self.interface}"

@extras_features("custom_fields", "graphql", "statuses", "relationships")
class OSPFConfiguration(PrimaryModel):
    """OSPF-specific configuration."""

    instance = models.ForeignKey(
        IGPInstance, on_delete=models.CASCADE, limit_choices_to={"protocol": "OSPF"}, related_name="ospf_configurations"
    )
    process_id = models.PositiveIntegerField(default=1, help_text="OSPF Process ID.")
    status = StatusField(null=True)

    class Meta:
        unique_together = ("instance", "process_id")
        verbose_name = "OSPF Configuration"
        verbose_name_plural = "OSPF Configurations"

    def __str__(self):
        return f"OSPF {self.process_id} on {self.instance.device}"

@extras_features("custom_fields", "graphql", "statuses", "relationships")
class OSPFInterfaceConfiguration(PrimaryModel):
    ospf_config = models.ForeignKey(
        OSPFConfiguration,
        on_delete=models.CASCADE,
        related_name="interface_configurations"
    )
    interface = models.ForeignKey(
        Interface,
        on_delete=models.CASCADE,
        related_name="ospf_configurations"
    )
    area = models.CharField(
        max_length=15,
        help_text="OSPF Area for this interface (e.g., 0.0.0.0)"
    )
    cost = models.PositiveIntegerField(
        default=1,
        help_text="OSPF cost for this interface."
    )
    status = StatusField(null=True)

    class Meta:
        unique_together = ("ospf_config", "interface")
        verbose_name = "OSPF Interface Configuration"
        verbose_name_plural = "OSPF Interface Configurations"

    def __str__(self):
        return f"OSPF Area {self.area} on {self.interface}"