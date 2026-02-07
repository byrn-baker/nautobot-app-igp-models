"""Create fixtures for tests."""

from nautobot.dcim.models import Device, DeviceType, Interface, Location, LocationType, Manufacturer
from nautobot.extras.models import Role, Status
from nautobot.ipam.models import VRF, IPAddress, Namespace, Prefix

from nautobot_igp_models.models import (
    IGPRoutingInstance,
    ISISConfiguration,
    ISISInterfaceConfiguration,
    OSPFConfiguration,
    OSPFInterfaceConfiguration,
)


def create_statuses():
    """Create Status objects needed for testing."""
    status_active, _ = Status.objects.get_or_create(
        name="Active",
        defaults={"description": "Unit is active"},
    )
    status_planned, _ = Status.objects.get_or_create(
        name="Planned",
        defaults={"description": "Unit is in planning"},
    )
    status_decommissioned, _ = Status.objects.get_or_create(
        name="Decommissioned",
        defaults={"description": "Unit is decommissioned"},
    )

    # Assign to appropriate content types
    from django.contrib.contenttypes.models import ContentType

    # Get content types for all models that use Status
    ct_device = ContentType.objects.get_for_model(Device)
    ct_interface = ContentType.objects.get_for_model(Interface)
    ct_ipaddress = ContentType.objects.get_for_model(IPAddress)
    ct_prefix = ContentType.objects.get_for_model(Prefix)
    ct_igp = ContentType.objects.get_for_model(IGPRoutingInstance)
    ct_isis_config = ContentType.objects.get_for_model(ISISConfiguration)
    ct_isis_interface = ContentType.objects.get_for_model(ISISInterfaceConfiguration)
    ct_ospf_config = ContentType.objects.get_for_model(OSPFConfiguration)
    ct_ospf_interface = ContentType.objects.get_for_model(OSPFInterfaceConfiguration)

    for status in [status_active, status_planned, status_decommissioned]:
        status.content_types.add(
            ct_device,
            ct_interface,
            ct_ipaddress,
            ct_prefix,
            ct_igp,
            ct_isis_config,
            ct_isis_interface,
            ct_ospf_config,
            ct_ospf_interface,
        )

    return {
        "active": status_active,
        "planned": status_planned,
        "decommissioned": status_decommissioned,
    }


def create_location_type():
    """Create LocationType for testing."""
    location_type, _ = LocationType.objects.get_or_create(
        name="Site",
        defaults={"description": "Network site"},
    )
    return location_type


def create_locations():
    """Create Location objects for testing."""
    location_type = create_location_type()
    statuses = create_statuses()

    location_dc1, _ = Location.objects.get_or_create(
        name="DataCenter-1",
        location_type=location_type,
        defaults={"status": statuses["active"]},
    )

    return {"dc1": location_dc1}


def create_manufacturer():
    """Create Manufacturer for testing."""
    manufacturer, _ = Manufacturer.objects.get_or_create(
        name="Cisco",
        defaults={"description": "Cisco Systems"},
    )
    return manufacturer


def create_device_role():
    """Create Role for devices."""
    role_router, _ = Role.objects.get_or_create(
        name="Router",
        defaults={"description": "Network Router"},
    )
    # Assign to Device content type
    from django.contrib.contenttypes.models import ContentType

    ct_device = ContentType.objects.get_for_model(Device)
    role_router.content_types.add(ct_device)

    return role_router


def create_device_type():
    """Create DeviceType for testing."""
    manufacturer = create_manufacturer()

    device_type, _ = DeviceType.objects.get_or_create(
        model="CSR1000v",
        manufacturer=manufacturer,
        defaults={"comments": "Cisco Cloud Services Router 1000v"},
    )
    return device_type


def create_devices():
    """Create Device objects for testing."""
    device_type = create_device_type()
    role = create_device_role()
    locations = create_locations()
    statuses = create_statuses()

    device1, _ = Device.objects.get_or_create(
        name="router1",
        defaults={
            "device_type": device_type,
            "role": role,
            "location": locations["dc1"],
            "status": statuses["active"],
        },
    )

    device2, _ = Device.objects.get_or_create(
        name="router2",
        defaults={
            "device_type": device_type,
            "role": role,
            "location": locations["dc1"],
            "status": statuses["active"],
        },
    )

    device3, _ = Device.objects.get_or_create(
        name="router3",
        defaults={
            "device_type": device_type,
            "role": role,
            "location": locations["dc1"],
            "status": statuses["active"],
        },
    )

    return {
        "router1": device1,
        "router2": device2,
        "router3": device3,
    }


def create_interfaces():
    """Create Interface objects for testing."""
    devices = create_devices()
    statuses = create_statuses()
    interfaces = {}

    for device_name, device in devices.items():
        # Loopback interface for router-id
        loopback, _ = Interface.objects.get_or_create(
            name="Loopback0",
            device=device,
            defaults={
                "type": "virtual",
                "status": statuses["active"],
            },
        )

        # Physical interfaces
        ge1, _ = Interface.objects.get_or_create(
            name="GigabitEthernet1",
            device=device,
            defaults={
                "type": "1000base-t",
                "status": statuses["active"],
            },
        )

        ge2, _ = Interface.objects.get_or_create(
            name="GigabitEthernet2",
            device=device,
            defaults={
                "type": "1000base-t",
                "status": statuses["active"],
            },
        )

        interfaces[device_name] = {
            "loopback0": loopback,
            "ge1": ge1,
            "ge2": ge2,
        }

    return interfaces


def create_namespace():
    """Create IP namespace for testing."""
    namespace, _ = Namespace.objects.get_or_create(
        name="Global",
        defaults={"description": "Global IP namespace"},
    )
    return namespace


def create_ip_addresses():
    """Create IPAddress objects for router IDs."""
    interfaces = create_interfaces()
    statuses = create_statuses()
    namespace = create_namespace()
    ip_addresses = {}

    # Create parent prefix for loopback IPs (10.0.0.0/24)
    parent_prefix, _ = Prefix.objects.get_or_create(
        prefix="10.0.0.0/24",
        namespace=namespace,
        defaults={
            "status": statuses["active"],
            "type": "network",
        },
    )

    # Router 1: 10.0.0.1/32
    ip1, _ = IPAddress.objects.get_or_create(
        address="10.0.0.1/32",
        parent=parent_prefix,
        defaults={
            "status": statuses["active"],
            "type": "host",
        },
    )
    ip1.interfaces.set([interfaces["router1"]["loopback0"]])
    ip_addresses["router1"] = ip1

    # Router 2: 10.0.0.2/32
    ip2, _ = IPAddress.objects.get_or_create(
        address="10.0.0.2/32",
        parent=parent_prefix,
        defaults={
            "status": statuses["active"],
            "type": "host",
        },
    )
    ip2.interfaces.set([interfaces["router2"]["loopback0"]])
    ip_addresses["router2"] = ip2

    # Router 3: 10.0.0.3/32
    ip3, _ = IPAddress.objects.get_or_create(
        address="10.0.0.3/32",
        parent=parent_prefix,
        defaults={
            "status": statuses["active"],
            "type": "host",
        },
    )
    ip3.interfaces.set([interfaces["router3"]["loopback0"]])
    ip_addresses["router3"] = ip3

    return ip_addresses


def create_vrfs():
    """Create VRF objects for testing."""
    namespace = create_namespace()

    vrf_global, _ = VRF.objects.get_or_create(
        name="Global",
        namespace=namespace,
        defaults={"description": "Global VRF"},
    )

    vrf_mgmt, _ = VRF.objects.get_or_create(
        name="Management",
        namespace=namespace,
        defaults={"description": "Management VRF"},
    )

    return {
        "global": vrf_global,
        "management": vrf_mgmt,
    }


def create_igp_routing_instances():
    """Create IGPRoutingInstance objects for testing."""
    devices = create_devices()
    ip_addresses = create_ip_addresses()
    vrfs = create_vrfs()
    statuses = create_statuses()

    # ISIS instances for router1 and router2
    igp_isis_r1, _ = IGPRoutingInstance.objects.get_or_create(
        name="ISIS-router1",
        device=devices["router1"],
        protocol="ISIS",
        defaults={
            "description": "ISIS routing instance for router1",
            "router_id": ip_addresses["router1"],
            "vrf": vrfs["global"],
            "isis_area": "49.0001",
            "status": statuses["active"],
        },
    )

    igp_isis_r2, _ = IGPRoutingInstance.objects.get_or_create(
        name="ISIS-router2",
        device=devices["router2"],
        protocol="ISIS",
        defaults={
            "description": "ISIS routing instance for router2",
            "router_id": ip_addresses["router2"],
            "vrf": vrfs["global"],
            "isis_area": "49.0001",
            "status": statuses["active"],
        },
    )

    # OSPF instances for all three routers
    igp_ospf_r1, _ = IGPRoutingInstance.objects.get_or_create(
        name="OSPF-router1",
        device=devices["router1"],
        protocol="OSPF",
        defaults={
            "description": "OSPF routing instance for router1",
            "router_id": ip_addresses["router1"],
            "vrf": vrfs["global"],
            "status": statuses["active"],
        },
    )

    igp_ospf_r2, _ = IGPRoutingInstance.objects.get_or_create(
        name="OSPF-router2",
        device=devices["router2"],
        protocol="OSPF",
        defaults={
            "description": "OSPF routing instance for router2",
            "router_id": ip_addresses["router2"],
            "vrf": vrfs["global"],
            "status": statuses["active"],
        },
    )

    igp_ospf_r3, _ = IGPRoutingInstance.objects.get_or_create(
        name="OSPF-router3",
        device=devices["router3"],
        protocol="OSPF",
        defaults={
            "description": "OSPF routing instance for router3",
            "router_id": ip_addresses["router3"],
            "vrf": vrfs["global"],
            "status": statuses["active"],
        },
    )

    return {
        "isis_router1": igp_isis_r1,
        "isis_router2": igp_isis_r2,
        "ospf_router1": igp_ospf_r1,
        "ospf_router2": igp_ospf_r2,
        "ospf_router3": igp_ospf_r3,
    }


def create_isis_configurations():
    """Create ISISConfiguration objects for testing."""
    igp_instances = create_igp_routing_instances()
    statuses = create_statuses()

    isis_config_r1, _ = ISISConfiguration.objects.get_or_create(
        name="ISIS-Config-R1",
        instance=igp_instances["isis_router1"],
        defaults={
            "status": statuses["active"],
            # system_id will be auto-generated by model save()
        },
    )

    isis_config_r2, _ = ISISConfiguration.objects.get_or_create(
        name="ISIS-Config-R2",
        instance=igp_instances["isis_router2"],
        defaults={
            "status": statuses["active"],
            # system_id will be auto-generated by model save()
        },
    )

    return {
        "router1": isis_config_r1,
        "router2": isis_config_r2,
    }


def create_isis_interface_configurations():
    """Create ISISInterfaceConfiguration objects for testing."""
    isis_configs = create_isis_configurations()
    devices = create_devices()
    interfaces = create_interfaces()
    statuses = create_statuses()

    # ISIS on router1 GigabitEthernet1
    isis_int_r1_ge1, _ = ISISInterfaceConfiguration.objects.get_or_create(
        name="ISIS-R1-GE1",
        isis_config=isis_configs["router1"],
        device=devices["router1"],
        interface=interfaces["router1"]["ge1"],
        defaults={
            "circuit_type": "L2",
            "metric": 10,
            "status": statuses["active"],
        },
    )

    # ISIS on router2 GigabitEthernet1
    isis_int_r2_ge1, _ = ISISInterfaceConfiguration.objects.get_or_create(
        name="ISIS-R2-GE1",
        isis_config=isis_configs["router2"],
        device=devices["router2"],
        interface=interfaces["router2"]["ge1"],
        defaults={
            "circuit_type": "L2",
            "metric": 10,
            "status": statuses["active"],
        },
    )

    return {
        "router1_ge1": isis_int_r1_ge1,
        "router2_ge1": isis_int_r2_ge1,
    }


def create_ospf_configurations():
    """Create OSPFConfiguration objects for testing."""
    igp_instances = create_igp_routing_instances()
    statuses = create_statuses()

    ospf_config_r1, _ = OSPFConfiguration.objects.get_or_create(
        name="OSPF-Config-R1",
        instance=igp_instances["ospf_router1"],
        defaults={
            "process_id": 1,
            "status": statuses["active"],
        },
    )

    ospf_config_r2, _ = OSPFConfiguration.objects.get_or_create(
        name="OSPF-Config-R2",
        instance=igp_instances["ospf_router2"],
        defaults={
            "process_id": 1,
            "status": statuses["active"],
        },
    )

    ospf_config_r3, _ = OSPFConfiguration.objects.get_or_create(
        name="OSPF-Config-R3",
        instance=igp_instances["ospf_router3"],
        defaults={
            "process_id": 1,
            "status": statuses["active"],
        },
    )

    return {
        "router1": ospf_config_r1,
        "router2": ospf_config_r2,
        "router3": ospf_config_r3,
    }


def create_ospf_interface_configurations():
    """Create OSPFInterfaceConfiguration objects for testing."""
    ospf_configs = create_ospf_configurations()
    interfaces = create_interfaces()
    statuses = create_statuses()

    # OSPF on router1 GigabitEthernet1
    ospf_int_r1_ge1, _ = OSPFInterfaceConfiguration.objects.get_or_create(
        name="OSPF-R1-GE1",
        ospf_config=ospf_configs["router1"],
        interface=interfaces["router1"]["ge1"],
        defaults={
            "area": "0.0.0.0",
            "cost": 1,
            "status": statuses["active"],
        },
    )

    # OSPF on router2 GigabitEthernet1
    ospf_int_r2_ge1, _ = OSPFInterfaceConfiguration.objects.get_or_create(
        name="OSPF-R2-GE1",
        ospf_config=ospf_configs["router2"],
        interface=interfaces["router2"]["ge1"],
        defaults={
            "area": "0.0.0.0",
            "cost": 1,
            "status": statuses["active"],
        },
    )

    # OSPF on router3 GigabitEthernet1
    ospf_int_r3_ge1, _ = OSPFInterfaceConfiguration.objects.get_or_create(
        name="OSPF-R3-GE1",
        ospf_config=ospf_configs["router3"],
        interface=interfaces["router3"]["ge1"],
        defaults={
            "area": "0.0.0.0",
            "cost": 1,
            "status": statuses["active"],
        },
    )

    return {
        "router1_ge1": ospf_int_r1_ge1,
        "router2_ge1": ospf_int_r2_ge1,
        "router3_ge1": ospf_int_r3_ge1,
    }


def create_all_fixtures():
    """
    Create all fixtures in proper dependency order.

    Returns a dictionary with all created objects organized by type.
    """
    return {
        "statuses": create_statuses(),
        "locations": create_locations(),
        "manufacturer": create_manufacturer(),
        "device_role": create_device_role(),
        "device_type": create_device_type(),
        "devices": create_devices(),
        "interfaces": create_interfaces(),
        "ip_addresses": create_ip_addresses(),
        "vrfs": create_vrfs(),
        "igp_instances": create_igp_routing_instances(),
        "isis_configurations": create_isis_configurations(),
        "isis_interface_configurations": create_isis_interface_configurations(),
        "ospf_configurations": create_ospf_configurations(),
        "ospf_interface_configurations": create_ospf_interface_configurations(),
    }
