# Management Commands

## load_igp_resources

Loads IGP config context schemas and export templates into Nautobot.

### What It Does

This command automatically installs:

1. **Config Context Schemas** - JSON Schema validation for ISIS and OSPF config context
2. **Export Templates** - Device configuration templates for Cisco IOS and Juniper JunOS

### Usage

```bash
# Load resources (skip existing)
nautobot-server load_igp_resources

# Force update existing resources
nautobot-server load_igp_resources --force
```

### Automatic Loading

This command is automatically run during `nautobot-server post-upgrade` via post-migrate signal.

To skip automatic loading (e.g., during testing):
```bash
export NAUTOBOT_SKIP_RESOURCE_LOADING=1
nautobot-server migrate
```

### Resources Loaded

#### Config Context Schemas

- **IGP ISIS Configuration**
  - Validates ISIS config context structure
  - Located at: `nautobot_igp_models/schemas/config_context_isis.json`

- **IGP OSPF Configuration**
  - Validates OSPF config context structure
  - Located at: `nautobot_igp_models/schemas/config_context_ospf.json`

#### Export Templates

**ISIS Configuration Templates:**
- Cisco IOS - For ISISConfiguration model
- Cisco IOS XR - For ISISConfiguration model
- Juniper JunOS - For ISISConfiguration model
- Arista EOS - For ISISConfiguration model

**OSPF Configuration Templates:**
- Cisco IOS - For OSPFConfiguration model
- Cisco IOS XR - For OSPFConfiguration model
- Arista EOS - For OSPFConfiguration model

Export templates are available from the object detail page under the "Export" button.

### Troubleshooting

**Resources not showing up:**
```bash
# Manually run the command with verbose output
nautobot-server load_igp_resources --force
```

**Export templates not visible:**
1. Ensure the model has `export_templates` in `@extras_features` decorator ✅ (already enabled)
2. Run `nautobot-server load_igp_resources --force`
3. Refresh the browser page
4. Check Extensibility > Export Templates in Nautobot UI

**Config context schemas not available:**
1. Navigate to Extensibility > Config Context Schemas
2. Verify schemas are present
3. If missing, run `nautobot-server load_igp_resources --force`

## analyze_igp_defaults

Analyzes existing IGP configurations and suggests default values for protocol-level settings.

See `nautobot_igp_models/management/commands/analyze_igp_defaults.py` for details.

## load_igp_demo_data

Loads demonstration data for the IGP Models app (if present).

See `nautobot_igp_models/management/commands/load_igp_demo_data.py` for details.
