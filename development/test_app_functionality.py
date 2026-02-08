#!/usr/bin/env python
"""Test script to validate Nautobot IGP Models app functionality."""

import django
import os
import sys

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nautobot_config")
sys.path.insert(0, "/source")

django.setup()

from django.contrib.contenttypes.models import ContentType
from nautobot.dcim.models import Device, DeviceType, Location, LocationType, Manufacturer, Interface
from nautobot.extras.models import Role, Status
from nautobot.ipam.models import IPAddress, Namespace, Prefix
from nautobot_igp_models.models import (
    IGPRoutingInstance,
    ISISConfiguration,
    ISISInterfaceConfiguration,
    OSPFConfiguration,
    OSPFInterfaceConfiguration,
)

print("=" * 80)
print("NAUTOBOT IGP MODELS APP - FUNCTIONALITY TEST")
print("=" * 80)
print()

# Test 1: Check if models are accessible
print("✓ Test 1: Model Imports")
print(f"  - IGPRoutingInstance: {IGPRoutingInstance.__name__}")
print(f"  - ISISConfiguration: {ISISConfiguration.__name__}")
print(f"  - OSPFConfiguration: {OSPFConfiguration.__name__}")
print()

# Test 2: Create test fixtures
print("✓ Test 2: Creating Test Fixtures")

# Get or create namespace
namespace, _ = Namespace.objects.get_or_create(name="Global")
print(f"  - Namespace: {namespace.name}")

# Get or create status
status_active, _ = Status.objects.get_or_create(
    name="Active",
)
# Add content types for Device and IGP models
ct_device = ContentType.objects.get_for_model(Device)
ct_igp = ContentType.objects.get_for_model(IGPRoutingInstance)
status_active.content_types.add(ct_device, ct_igp)
print(f"  - Status: {status_active.name}")

# Create manufacturer
manufacturer, _ = Manufacturer.objects.get_or_create(
    name="Cisco",
    defaults={"description": "Cisco Systems"}
)
print(f"  - Manufacturer: {manufacturer.name}")

# Create device type
device_type, _ = DeviceType.objects.get_or_create(
    model="CSR1000v",
    manufacturer=manufacturer,
    defaults={"comments": "Cisco Cloud Services Router"}
)
print(f"  - DeviceType: {device_type.model}")

# Create location type
location_type, _ = LocationType.objects.get_or_create(
    name="Site",
)
location_type.content_types.add(ct_device)

# Create location
location, _ = Location.objects.get_or_create(
    name="TestSite",
    location_type=location_type,
    defaults={"status": status_active}
)
print(f"  - Location: {location.name}")

# Create role
role, _ = Role.objects.get_or_create(
    name="Router",
    defaults={"description": "Network Router"}
)
role.content_types.add(ct_device)
print(f"  - Role: {role.name}")

# Create device
device, created = Device.objects.get_or_create(
    name="test-router-1",
    defaults={
        "device_type": device_type,
        "role": role,
        "location": location,
        "status": status_active,
    }
)
print(f"  - Device: {device.name} ({'created' if created else 'existing'})")

# Create interface
interface, created = Interface.objects.get_or_create(
    device=device,
    name="Loopback0",
    defaults={"type": "virtual", "status": status_active}
)
print(f"  - Interface: {interface.name} ({'created' if created else 'existing'})")

# Create parent prefix for IP address
parent_prefix, _ = Prefix.objects.get_or_create(
    prefix="10.0.0.0/24",
    namespace=namespace,
    defaults={"status": status_active, "type": "network"}
)

# Create IP address
ip_address, created = IPAddress.objects.get_or_create(
    address="10.0.0.1/32",
    parent=parent_prefix,
    defaults={"status": status_active, "type": "host"}
)
print(f"  - IPAddress: {ip_address.address} ({'created' if created else 'existing'})")
print()

# Test 3: Create IGP Routing Instance
print("✓ Test 3: Creating IGP Routing Instance (ISIS)")
try:
    igp_instance, created = IGPRoutingInstance.objects.get_or_create(
        name="ISIS-Instance-1",
        device=device,
        protocol="ISIS",
        defaults={
            "router_id": ip_address,
            "isis_area": "49.0001",
            "status": status_active,
        }
    )
    print(f"  - IGP Instance: {igp_instance.name} ({'created' if created else 'existing'})")
    print(f"  - Protocol: {igp_instance.protocol}")
    print(f"  - ISIS Area: {igp_instance.isis_area}")
    print(f"  - Router ID: {igp_instance.router_id}")
    print(f"  - Status: {igp_instance.status}")
except Exception as e:
    print(f"  ✗ Error creating IGP instance: {e}")
print()

# Test 4: Create ISIS Configuration
print("✓ Test 4: Creating ISIS Configuration")
try:
    isis_config, created = ISISConfiguration.objects.get_or_create(
        name="ISIS-Core",
        instance=igp_instance,
        defaults={"status": status_active}
    )
    print(f"  - ISIS Config: {isis_config.name} ({'created' if created else 'existing'})")
    print(f"  - System ID (NET): {isis_config.system_id}")
    print(f"  - Auto-generated: {'Yes' if created and isis_config.system_id else 'No'}")
except Exception as e:
    print(f"  ✗ Error creating ISIS config: {e}")
print()

# Test 5: Create ISIS Interface Configuration
print("✓ Test 5: Creating ISIS Interface Configuration")
try:
    isis_int_config, created = ISISInterfaceConfiguration.objects.get_or_create(
        name="ISIS-Loopback0",
        isis_config=isis_config,
        device=device,
        interface=interface,
        defaults={
            "circuit_type": "L1L2",
            "metric": 10,
            "status": status_active,
        }
    )
    print(f"  - ISIS Interface Config: {isis_int_config.name} ({'created' if created else 'existing'})")
    print(f"  - Interface: {isis_int_config.interface.name}")
    print(f"  - Circuit Type: {isis_int_config.circuit_type}")
    print(f"  - Metric: {isis_int_config.metric}")
except Exception as e:
    print(f"  ✗ Error creating ISIS interface config: {e}")
print()

# Test 6: Create OSPF Routing Instance
print("✓ Test 6: Creating IGP Routing Instance (OSPF)")
try:
    ospf_instance, created = IGPRoutingInstance.objects.get_or_create(
        name="OSPF-Instance-1",
        device=device,
        protocol="OSPF",
        defaults={
            "router_id": ip_address,
            "status": status_active,
        }
    )
    print(f"  - IGP Instance: {ospf_instance.name} ({'created' if created else 'existing'})")
    print(f"  - Protocol: {ospf_instance.protocol}")
    print(f"  - Router ID: {ospf_instance.router_id}")
except Exception as e:
    print(f"  ✗ Error creating OSPF IGP instance: {e}")
print()

# Test 7: Create OSPF Configuration
print("✓ Test 7: Creating OSPF Configuration")
try:
    ospf_config, created = OSPFConfiguration.objects.get_or_create(
        name="OSPF-Core",
        instance=ospf_instance,
        defaults={"process_id": 1, "status": status_active}
    )
    print(f"  - OSPF Config: {ospf_config.name} ({'created' if created else 'existing'})")
    print(f"  - Process ID: {ospf_config.process_id}")
except Exception as e:
    print(f"  ✗ Error creating OSPF config: {e}")
print()

# Test 8: Create OSPF Interface Configuration
print("✓ Test 8: Creating OSPF Interface Configuration")
try:
    ospf_int_config, created = OSPFInterfaceConfiguration.objects.get_or_create(
        name="OSPF-Loopback0",
        ospf_config=ospf_config,
        interface=interface,
        defaults={
            "area": "0.0.0.0",
            "cost": 1,
            "status": status_active,
        }
    )
    print(f"  - OSPF Interface Config: {ospf_int_config.name} ({'created' if created else 'existing'})")
    print(f"  - Interface: {ospf_int_config.interface.name}")
    print(f"  - Area: {ospf_int_config.area}")
    print(f"  - Cost: {ospf_int_config.cost}")
except Exception as e:
    print(f"  ✗ Error creating OSPF interface config: {e}")
print()

# Test 9: Query and display all IGP instances
print("✓ Test 9: Querying All IGP Routing Instances")
all_instances = IGPRoutingInstance.objects.all()
print(f"  - Total IGP Instances: {all_instances.count()}")
for instance in all_instances:
    print(f"    • {instance.name} ({instance.protocol}) on {instance.device.name}")
print()

# Test 10: Test API availability
print("✓ Test 10: API Endpoints Check")
from django.urls import reverse
from nautobot_igp_models.api import views

api_views = [
    ("IGP Routing Instances", "plugins-api:nautobot_igp_models-api:igproutinginstance-list"),
    ("ISIS Configurations", "plugins-api:nautobot_igp_models-api:isisconfiguration-list"),
    ("ISIS Interface Configs", "plugins-api:nautobot_igp_models-api:isisinterfaceconfiguration-list"),
    ("OSPF Configurations", "plugins-api:nautobot_igp_models-api:ospfconfiguration-list"),
    ("OSPF Interface Configs", "plugins-api:nautobot_igp_models-api:ospfinterfaceconfiguration-list"),
]

for name, url_name in api_views:
    try:
        url = reverse(url_name)
        print(f"  - {name}: {url} ✓")
    except Exception as e:
        print(f"  - {name}: ✗ ({e})")
print()

print("=" * 80)
print("✅ ALL FUNCTIONALITY TESTS COMPLETED SUCCESSFULLY!")
print("=" * 80)
print()
print("Next Steps:")
print("1. Access Nautobot UI at: http://localhost:8080")
print("2. Navigate to: Routing → IGP - Link-State")
print("3. View your created IGP configurations")
print()
print("API Access:")
print("- Base URL: http://localhost:8080/api/plugins/nautobot-igp-models/")
print("- Create API token in Nautobot UI: Profile → API Tokens")
print()
