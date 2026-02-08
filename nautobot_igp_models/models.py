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

    # Default values for interface inheritance (hybrid approach)
    default_metric = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Default ISIS metric for interfaces (overridable at interface level)",
    )
    default_hello_interval = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Default hello interval in seconds (can be overridden by config context)",
    )
    default_hello_multiplier = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Default hello multiplier (can be overridden by config context)",
    )
    default_priority = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Default DIS priority (can be overridden by config context)",
    )

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
    metric = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="ISIS metric for this interface. If not set, inherits from ISIS configuration default.",
    )
    status = StatusField(null=True)

    class Meta:
        unique_together = ("isis_config", "interface")
        verbose_name = "ISIS Interface Configuration"
        verbose_name_plural = "ISIS Interface Configurations"

    def get_effective_metric(self):
        """Get effective metric with inheritance: interface > isis_config default > global default."""
        if self.metric is not None:
            return self.metric
        if self.isis_config.default_metric is not None:
            return self.isis_config.default_metric
        return 10  # Global default for ISIS

    def get_effective_config(self):
        """
        Get effective configuration with full inheritance chain.

        Priority order (highest to lowest):
        1. Interface-specific database fields
        2. ISIS configuration defaults (database)
        3. Device config context (flexible/optional settings)
        4. Global protocol defaults

        Returns:
            dict: Complete effective configuration for this interface
        """
        # Start with global protocol defaults
        config = {
            "metric": 10,
            "hello_interval": 10,
            "hello_multiplier": 3,
            "priority": 64,
            "circuit_type": self.circuit_type,
        }

        # Layer 1: Device-level config context (organization-wide defaults)
        if hasattr(self.device, "config_context") and self.device.config_context:
            device_ctx = self.device.config_context.get("igp", {}).get("isis", {})
            config.update({k: v for k, v in device_ctx.items() if v is not None})

        # Layer 2: ISIS configuration defaults from database
        if self.isis_config.default_metric is not None:
            config["metric"] = self.isis_config.default_metric
        if self.isis_config.default_hello_interval is not None:
            config["hello_interval"] = self.isis_config.default_hello_interval
        if self.isis_config.default_hello_multiplier is not None:
            config["hello_multiplier"] = self.isis_config.default_hello_multiplier
        if self.isis_config.default_priority is not None:
            config["priority"] = self.isis_config.default_priority

        # Layer 3: Interface-specific overrides from database
        if self.metric is not None:
            config["metric"] = self.metric
        config["circuit_type"] = self.circuit_type  # Always from interface

        # Layer 4: Interface-level config context (most specific)
        if hasattr(self.interface, "config_context") and self.interface.config_context:
            if_ctx = self.interface.config_context.get("igp", {}).get("isis", {})
            config.update({k: v for k, v in if_ctx.items() if v is not None})

        return config

    def get_vendor_config(self, vendor=None):
        """
        Get vendor-specific configuration from config context.

        Args:
            vendor (str, optional): Specific vendor ('cisco', 'juniper', etc.).
                                   If None, returns all vendor configs.

        Returns:
            dict: Vendor-specific configuration settings
        """
        vendor_config = {}

        if hasattr(self.device, "config_context") and self.device.config_context:
            isis_ctx = self.device.config_context.get("igp", {}).get("isis", {})

            if vendor:
                vendor_config = isis_ctx.get(vendor, {})
            else:
                # Return all vendor-specific configs
                for key, value in isis_ctx.items():
                    if key not in ["metric", "hello_interval", "hello_multiplier", "priority"]:
                        vendor_config[key] = value

        return vendor_config

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

    # Default values for interface inheritance (hybrid approach)
    default_cost = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Default OSPF cost for interfaces (overridable at interface level)",
    )
    default_hello_interval = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Default hello interval in seconds (can be overridden by config context)",
    )
    default_dead_interval = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Default dead interval in seconds (can be overridden by config context)",
    )
    default_priority = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Default router priority (can be overridden by config context)",
    )

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
    cost = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="OSPF cost for this interface. If not set, inherits from OSPF configuration default.",
    )
    status = StatusField(null=True)

    class Meta:
        unique_together = ("ospf_config", "interface")
        verbose_name = "OSPF Interface Configuration"
        verbose_name_plural = "OSPF Interface Configurations"

    def get_effective_cost(self):
        """Get effective cost with inheritance: interface > ospf_config default > global default."""
        if self.cost is not None:
            return self.cost
        if self.ospf_config.default_cost is not None:
            return self.ospf_config.default_cost
        return 1  # Global default for OSPF

    def get_effective_config(self):
        """
        Get effective configuration with full inheritance chain.

        Priority order (highest to lowest):
        1. Interface-specific database fields
        2. OSPF configuration defaults (database)
        3. Device config context (flexible/optional settings)
        4. Global protocol defaults

        Returns:
            dict: Complete effective configuration for this interface
        """
        # Start with global protocol defaults
        config = {
            "cost": 1,
            "hello_interval": 10,
            "dead_interval": 40,
            "priority": 1,
            "area": self.area,
        }

        # Layer 1: Device-level config context (organization-wide defaults)
        if hasattr(self.interface, "device") and hasattr(self.interface.device, "config_context"):
            if self.interface.device.config_context:
                device_ctx = self.interface.device.config_context.get("igp", {}).get("ospf", {})
                config.update({k: v for k, v in device_ctx.items() if v is not None})

        # Layer 2: OSPF configuration defaults from database
        if self.ospf_config.default_cost is not None:
            config["cost"] = self.ospf_config.default_cost
        if self.ospf_config.default_hello_interval is not None:
            config["hello_interval"] = self.ospf_config.default_hello_interval
        if self.ospf_config.default_dead_interval is not None:
            config["dead_interval"] = self.ospf_config.default_dead_interval
        if self.ospf_config.default_priority is not None:
            config["priority"] = self.ospf_config.default_priority

        # Layer 3: Interface-specific overrides from database
        if self.cost is not None:
            config["cost"] = self.cost
        config["area"] = self.area  # Always from interface

        # Layer 4: Interface-level config context (most specific)
        if hasattr(self.interface, "config_context") and self.interface.config_context:
            if_ctx = self.interface.config_context.get("igp", {}).get("ospf", {})
            config.update({k: v for k, v in if_ctx.items() if v is not None})

        return config

    def get_vendor_config(self, vendor=None):
        """
        Get vendor-specific configuration from config context.

        Args:
            vendor (str, optional): Specific vendor ('cisco', 'juniper', etc.).
                                   If None, returns all vendor configs.

        Returns:
            dict: Vendor-specific configuration settings
        """
        vendor_config = {}

        if hasattr(self.interface, "device") and hasattr(self.interface.device, "config_context"):
            if self.interface.device.config_context:
                ospf_ctx = self.interface.device.config_context.get("igp", {}).get("ospf", {})

                if vendor:
                    vendor_config = ospf_ctx.get(vendor, {})
                else:
                    # Return all vendor-specific configs
                    for key, value in ospf_ctx.items():
                        if key not in ["cost", "hello_interval", "dead_interval", "priority"]:
                            vendor_config[key] = value

        return vendor_config

    def __str__(self):
        return f"OSPF Area {self.area} on {self.interface}"
