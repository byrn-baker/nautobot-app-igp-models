"""Django management command to load demo data for IGP models."""

from django.core.management.base import BaseCommand
from django.db import transaction
from nautobot.dcim.models import Device, DeviceType, Interface, Location, LocationType, Manufacturer
from nautobot.extras.models import Role, Status
from nautobot.ipam.models import IPAddress, Namespace, Prefix

from nautobot_igp_models.models import (
    IGPRoutingInstance,
    ISISConfiguration,
    ISISInterfaceConfiguration,
    OSPFConfiguration,
    OSPFInterfaceConfiguration,
)


class Command(BaseCommand):
    """Load demo data for IGP models."""

    help = "Load realistic demo data for testing the Nautobot IGP Models app"

    def add_arguments(self, parser):
        """Add command arguments."""
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete all existing IGP data before loading demo data",
        )
        parser.add_argument(
            "--no-create-dependencies",
            action="store_true",
            help="Only create IGP objects (assumes devices, interfaces, etc. already exist)",
        )

    def handle(self, *args, **options):
        """Execute the command."""
        flush = options.get("flush", False)
        create_dependencies = not options.get("no_create_dependencies", False)

        self.stdout.write(self.style.SUCCESS("Loading IGP demo data..."))

        with transaction.atomic():
            if flush:
                self.stdout.write("Flushing existing IGP data...")
                self._flush_igp_data()

            if create_dependencies:
                self.stdout.write("Creating dependencies (locations, devices, interfaces, IPs)...")
                self._create_dependencies()

            self.stdout.write("Creating IGP routing instances...")
            self._create_igp_instances()

            self.stdout.write("Creating ISIS configurations...")
            self._create_isis_configurations()

            self.stdout.write("Creating ISIS interface configurations...")
            self._create_isis_interface_configurations()

            self.stdout.write("Creating OSPF configurations...")
            self._create_ospf_configurations()

            self.stdout.write("Creating OSPF interface configurations...")
            self._create_ospf_interface_configurations()

        self.stdout.write(self.style.SUCCESS("\n✓ Demo data loaded successfully!"))
        self.stdout.write("\nDemo Topology:")
        self.stdout.write("  DC-CORE-01 (ISIS + OSPF) ←→ DC-CORE-02 (ISIS + OSPF)")
        self.stdout.write("      ↓ OSPF Area 0               ↓ OSPF Area 0")
        self.stdout.write("  DC-EDGE-01                  DC-EDGE-02")
        self.stdout.write("\nYou can now explore the IGP configurations in the Nautobot UI:")
        self.stdout.write("  Navigation → Routing → IGP - Link-State")

    def _flush_igp_data(self):
        """Delete all existing IGP data."""
        OSPFInterfaceConfiguration.objects.all().delete()
        OSPFConfiguration.objects.all().delete()
        ISISInterfaceConfiguration.objects.all().delete()
        ISISConfiguration.objects.all().delete()
        IGPRoutingInstance.objects.all().delete()
        self.stdout.write(self.style.WARNING("  ✓ Flushed all IGP data"))

    def _create_dependencies(self):
        """Create all dependencies needed for IGP configurations."""
        # Create statuses
        status_active, _ = Status.objects.get_or_create(
            name="Active",
            defaults={"description": "Unit is active"},
        )
        status_planned, _ = Status.objects.get_or_create(
            name="Planned",
            defaults={"description": "Unit is in planning"},
        )

        # Assign statuses to content types
        from django.contrib.contenttypes.models import ContentType

        for model in [
            Device,
            Interface,
            IPAddress,
            Prefix,
            IGPRoutingInstance,
            ISISConfiguration,
            ISISInterfaceConfiguration,
            OSPFConfiguration,
            OSPFInterfaceConfiguration,
        ]:
            ct = ContentType.objects.get_for_model(model)
            status_active.content_types.add(ct)
            status_planned.content_types.add(ct)

        # Create location type and location
        location_type, _ = LocationType.objects.get_or_create(
            name="Site",
            defaults={"description": "Network site"},
        )

        location, _ = Location.objects.get_or_create(
            name="DataCenter-1",
            location_type=location_type,
            defaults={"status": status_active},
        )

        # Create manufacturer and device type
        manufacturer, _ = Manufacturer.objects.get_or_create(
            name="Cisco",
            defaults={"description": "Cisco Systems"},
        )

        device_type, _ = DeviceType.objects.get_or_create(
            model="CSR1000v",
            manufacturer=manufacturer,
            defaults={"comments": "Cisco Cloud Services Router 1000v"},
        )

        # Create device role
        role, _ = Role.objects.get_or_create(
            name="Router",
            defaults={"description": "Network Router"},
        )
        ct_device = ContentType.objects.get_for_model(Device)
        role.content_types.add(ct_device)

        # Create devices
        self.devices = {}
        for device_name in ["DC-CORE-01", "DC-CORE-02", "DC-EDGE-01", "DC-EDGE-02"]:
            device, created = Device.objects.get_or_create(
                name=device_name,
                defaults={
                    "device_type": device_type,
                    "role": role,
                    "location": location,
                    "status": status_active,
                },
            )
            self.devices[device_name] = device
            if created:
                self.stdout.write(f"  ✓ Created device: {device_name}")

        # Create interfaces
        self.interfaces = {}
        for device_name, device in self.devices.items():
            self.interfaces[device_name] = {}

            # Loopback interface
            loopback, created = Interface.objects.get_or_create(
                name="Loopback0",
                device=device,
                defaults={
                    "type": "virtual",
                    "status": status_active,
                },
            )
            self.interfaces[device_name]["Loopback0"] = loopback

            # Physical interfaces
            for intf_name in ["GigabitEthernet1", "GigabitEthernet2"]:
                interface, created = Interface.objects.get_or_create(
                    name=intf_name,
                    device=device,
                    defaults={
                        "type": "1000base-t",
                        "status": status_active,
                    },
                )
                self.interfaces[device_name][intf_name] = interface

        # Create IP namespace
        namespace, _ = Namespace.objects.get_or_create(
            name="Global",
            defaults={"description": "Global IP namespace"},
        )

        # Create parent prefix for loopback IPs
        parent_prefix, _ = Prefix.objects.get_or_create(
            prefix="10.0.0.0/24",
            namespace=namespace,
            defaults={
                "status": status_active,
                "type": "network",
            },
        )

        # Create IP addresses for router IDs
        self.ip_addresses = {}
        ip_map = {
            "DC-CORE-01": "10.0.0.1/32",
            "DC-CORE-02": "10.0.0.2/32",
            "DC-EDGE-01": "10.0.0.3/32",
            "DC-EDGE-02": "10.0.0.4/32",
        }

        for device_name, ip_addr in ip_map.items():
            ip, created = IPAddress.objects.get_or_create(
                address=ip_addr,
                parent=parent_prefix,
                defaults={
                    "status": status_active,
                    "type": "host",
                },
            )
            ip.interfaces.set([self.interfaces[device_name]["Loopback0"]])
            self.ip_addresses[device_name] = ip
            if created:
                self.stdout.write(f"  ✓ Created IP address: {ip_addr} on {device_name}")

        self.status_active = status_active
        self.status_planned = status_planned

    def _create_igp_instances(self):
        """Create IGP routing instances."""
        self.igp_instances = {}

        # ISIS instances for core routers
        for device_name in ["DC-CORE-01", "DC-CORE-02"]:
            instance, created = IGPRoutingInstance.objects.get_or_create(
                name=f"ISIS-{device_name}",
                device=self.devices[device_name],
                protocol="ISIS",
                defaults={
                    "description": f"ISIS routing instance for {device_name}",
                    "router_id": self.ip_addresses[device_name],
                    "isis_area": "49.0001",
                    "status": self.status_active,
                },
            )
            self.igp_instances[f"ISIS-{device_name}"] = instance
            if created:
                self.stdout.write(f"  ✓ Created ISIS instance: {device_name}")

        # OSPF instances for all routers
        for device_name in ["DC-CORE-01", "DC-CORE-02", "DC-EDGE-01", "DC-EDGE-02"]:
            instance, created = IGPRoutingInstance.objects.get_or_create(
                name=f"OSPF-{device_name}",
                device=self.devices[device_name],
                protocol="OSPF",
                defaults={
                    "description": f"OSPF routing instance for {device_name}",
                    "router_id": self.ip_addresses[device_name],
                    "status": self.status_active,
                },
            )
            self.igp_instances[f"OSPF-{device_name}"] = instance
            if created:
                self.stdout.write(f"  ✓ Created OSPF instance: {device_name}")

    def _create_isis_configurations(self):
        """Create ISIS configurations."""
        self.isis_configs = {}

        for device_name in ["DC-CORE-01", "DC-CORE-02"]:
            config, created = ISISConfiguration.objects.get_or_create(
                name=f"ISIS-Config-{device_name}",
                instance=self.igp_instances[f"ISIS-{device_name}"],
                defaults={
                    "status": self.status_active,
                    # system_id will be auto-generated
                },
            )
            self.isis_configs[device_name] = config
            if created:
                self.stdout.write(f"  ✓ Created ISIS config: {device_name} (NET: {config.system_id})")

    def _create_isis_interface_configurations(self):
        """Create ISIS interface configurations."""
        for device_name in ["DC-CORE-01", "DC-CORE-02"]:
            for intf_name in ["GigabitEthernet1", "GigabitEthernet2"]:
                config, created = ISISInterfaceConfiguration.objects.get_or_create(
                    name=f"ISIS-{device_name}-{intf_name}",
                    isis_config=self.isis_configs[device_name],
                    device=self.devices[device_name],
                    interface=self.interfaces[device_name][intf_name],
                    defaults={
                        "circuit_type": "L2",
                        "metric": 10,
                        "status": self.status_active,
                    },
                )
                if created:
                    self.stdout.write(f"  ✓ Created ISIS interface: {device_name} {intf_name}")

    def _create_ospf_configurations(self):
        """Create OSPF configurations."""
        self.ospf_configs = {}

        for device_name in ["DC-CORE-01", "DC-CORE-02", "DC-EDGE-01", "DC-EDGE-02"]:
            config, created = OSPFConfiguration.objects.get_or_create(
                name=f"OSPF-Config-{device_name}",
                instance=self.igp_instances[f"OSPF-{device_name}"],
                defaults={
                    "process_id": 1,
                    "status": self.status_active,
                },
            )
            self.ospf_configs[device_name] = config
            if created:
                self.stdout.write(f"  ✓ Created OSPF config: {device_name} (Process 1)")

    def _create_ospf_interface_configurations(self):
        """Create OSPF interface configurations."""
        for device_name in ["DC-CORE-01", "DC-CORE-02", "DC-EDGE-01", "DC-EDGE-02"]:
            for intf_name in ["GigabitEthernet1", "GigabitEthernet2"]:
                config, created = OSPFInterfaceConfiguration.objects.get_or_create(
                    name=f"OSPF-{device_name}-{intf_name}",
                    ospf_config=self.ospf_configs[device_name],
                    interface=self.interfaces[device_name][intf_name],
                    defaults={
                        "area": "0.0.0.0",
                        "cost": 1,
                        "status": self.status_active,
                    },
                )
                if created:
                    self.stdout.write(f"  ✓ Created OSPF interface: {device_name} {intf_name}")
