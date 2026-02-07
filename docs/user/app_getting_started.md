# Getting Started with the App

This document provides a step-by-step tutorial on how to get started with the Nautobot IGP Models app and begin modeling your IGP routing configurations.

## Install the App

To install the app, please follow the instructions detailed in the [Installation Guide](../admin/install.md).

## Quick Start with Demo Data

The fastest way to explore the app is to load the included demo data, which creates a realistic four-router network topology with ISIS and OSPF configurations.

### Load Demo Data

From your Nautobot environment, run:

```bash
nautobot-server load_igp_demo_data
```

This command creates:

- 4 routers (DC-CORE-01, DC-CORE-02, DC-EDGE-01, DC-EDGE-02)
- ISIS routing on core routers with auto-generated NETs
- OSPF routing on all routers in area 0.0.0.0
- Complete interface configurations

### Explore the Demo Data

1. Navigate to **Routing** → **IGP - Link-State** → **IGP Routing Instances** in the Nautobot UI
2. You'll see 6 routing instances (2 ISIS, 4 OSPF)
3. Click on any instance to view its detailed configuration
4. Explore related ISIS or OSPF configurations and interface settings

## Creating Your First IGP Configuration

Let's walk through creating a complete ISIS configuration for a router.

### Step 1: Ensure Prerequisites

Before creating IGP configurations, ensure you have:

- A device in Nautobot
- At least one interface on that device
- An IP address assigned to an interface (for router ID)
- An "Active" status (or other appropriate status)

### Step 2: Create an IGP Routing Instance

1. Navigate to **Routing** → **IGP - Link-State** → **IGP Routing Instances**
2. Click the **+ Add** button
3. Fill in the form:
   - **Name**: Descriptive name (e.g., "ISIS-CORE-ROUTER-01")
   - **Device**: Select your device
   - **Protocol**: Choose "ISIS"
   - **Router ID**: Select an IP address from the device
   - **VRF**: Select a VRF (or leave blank for global)
   - **ISIS Area**: Enter area ID (e.g., "49.0001")
   - **Status**: Select "Active"
4. Click **Create**

### Step 3: Create ISIS Configuration

1. Navigate to **Routing** → **IGP - Link-State** → **ISIS Configurations**
2. Click the **+ Add** button
3. Fill in the form:
   - **Name**: Configuration name (e.g., "ISIS-Config-Core-01")
   - **Instance**: Select the IGP Routing Instance you just created
   - **System ID**: Leave blank for auto-generation or enter manually
   - **Status**: Select "Active"
4. Click **Create**

!!! note "Automatic NET Generation"
    If you leave the System ID field blank, the app will automatically generate a valid ISIS NET based on the router ID and ISIS area from the routing instance. For example, router ID 10.0.0.1 in area 49.0001 generates NET: 49.0001.0010.0000.0001.00

### Step 4: Configure ISIS on Interfaces

1. Navigate to **Routing** → **IGP - Link-State** → **ISIS Interface Configurations**
2. Click the **+ Add** button
3. Fill in the form:
   - **Name**: Interface config name (e.g., "ISIS-GE0/0/1")
   - **ISIS Config**: Select the ISIS configuration
   - **Device**: Select your device
   - **Interface**: Select the interface to configure
   - **Circuit Type**: Choose Level 1, Level 2, or Level 1-2
   - **Metric**: Enter the ISIS metric (e.g., 10)
   - **Status**: Select "Active"
4. Click **Create**
5. Repeat for additional interfaces

## Creating an OSPF Configuration

The process for OSPF is similar:

### Step 1: Create OSPF Routing Instance

1. Navigate to **Routing** → **IGP - Link-State** → **IGP Routing Instances**
2. Click **+ Add**
3. Fill in:
   - **Protocol**: Choose "OSPF"
   - **ISIS Area**: Leave blank (not used for OSPF)
   - (Other fields same as ISIS)
4. Click **Create**

### Step 2: Create OSPF Configuration

1. Navigate to **Routing** → **IGP - Link-State** → **OSPF Configurations**
2. Click **+ Add**
3. Fill in:
   - **Name**: Configuration name
   - **Instance**: Select the OSPF routing instance
   - **Process ID**: Enter process ID (defaults to 1)
   - **Status**: Select "Active"
4. Click **Create**

### Step 3: Configure OSPF on Interfaces

1. Navigate to **Routing** → **IGP - Link-State** → **OSPF Interface Configurations**
2. Click **+ Add**
3. Fill in:
   - **Name**: Interface config name
   - **OSPF Config**: Select the OSPF configuration
   - **Interface**: Select the interface
   - **Area**: Enter OSPF area (e.g., "0.0.0.0" or "1")
   - **Cost**: Enter interface cost (e.g., 1)
   - **Status**: Select "Active"
4. Click **Create**

## Using Filters

The app provides powerful filtering capabilities:

1. On any list view, use the **Filters** panel on the right
2. Filter by:
   - Device
   - Protocol type (ISIS/OSPF)
   - Status
   - Area (for OSPF)
   - Circuit type (for ISIS)
   - And more...

## Bulk Operations

### Bulk Edit

1. Select multiple objects using checkboxes
2. Choose **Edit Selected** from the dropdown
3. Modify fields that should apply to all selected objects
4. Click **Apply**

### CSV Import

1. Click **Import** on any list view
2. Download the CSV template
3. Fill in your data
4. Upload and import

## API Access

All IGP models are accessible via the Nautobot REST API:

### List IGP Routing Instances

```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://nautobot/api/plugins/nautobot-igp-models/igp-routing-instances/
```

### Create ISIS Configuration

```bash
curl -X POST -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "ISIS-Config-API",
    "instance": "UUID_OF_INSTANCE",
    "status": "UUID_OF_STATUS"
  }' \
  http://nautobot/api/plugins/nautobot-igp-models/isis-configurations/
```

### Filter by Device

```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  "http://nautobot/api/plugins/nautobot-igp-models/igp-routing-instances/?device=router1"
```

For complete API documentation, visit `/api/docs/` in your Nautobot instance.

## Using with PyNautobot

The app works seamlessly with PyNautobot:

```python
from pynautobot import api

# Connect to Nautobot
nautobot = api(url="http://nautobot", token="YOUR_TOKEN")

# Get all ISIS configurations
isis_configs = nautobot.plugins.nautobot-igp-models.isis-configurations.all()

# Create a new OSPF interface configuration
ospf_int = nautobot.plugins.nautobot-igp-models.ospf-interface-configurations.create(
    name="OSPF-API-Test",
    ospf_config="uuid-of-ospf-config",
    interface="uuid-of-interface",
    area="0.0.0.0",
    cost=10,
    status="uuid-of-active-status"
)
```

## What's Next?

Now that you've created your first IGP configurations, you can:

- **Explore Use Cases**: Check out the [Use Cases](app_use_cases.md) guide for common scenarios
- **API Integration**: Integrate with your automation tools (Ansible, Nornir, custom scripts)
- **Configuration Generation**: Use the data to generate router configurations
- **Validation**: Build workflows to validate routing design consistency
- **Migration Planning**: Model both current and target state for protocol migrations

## Getting Help

- **Documentation**: Full documentation available at [docs.nautobot.com](https://docs.nautobot.com/projects/nautobot-igp-models/)
- **Issues**: Report bugs or request features on [GitHub](https://github.com/byrn-baker/nautobot-app-igp-models/issues)
- **Community**: Join the discussion on [Nautobot Slack](https://slack.networktocode.com)

## Tips and Best Practices

### Naming Conventions

Use consistent naming for easier filtering and automation:

- IGP Instances: `{PROTOCOL}-{DEVICE-NAME}` (e.g., "ISIS-CORE-01")
- Configurations: `{PROTOCOL}-Config-{DEVICE-NAME}` (e.g., "OSPF-Config-Edge-01")
- Interface Configs: `{PROTOCOL}-{DEVICE}-{INTERFACE}` (e.g., "ISIS-CORE-01-GE1")

### Status Workflow

Use statuses to track configuration lifecycle:

- **Planned**: Configuration designed but not yet deployed
- **Active**: Currently deployed and operational
- **Decommissioned**: Removed from network but kept for historical reference

### Validation

Regularly validate your data:

- Ensure all routing instances have valid router IDs
- Verify ISIS areas are consistent across devices in same domain
- Check OSPF area boundaries align with design
- Confirm interface configurations match deployed state
