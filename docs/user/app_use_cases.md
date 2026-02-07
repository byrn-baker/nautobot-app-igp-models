# Use Cases and Examples

This document describes common use cases and real-world scenarios for using the Nautobot IGP Models app.

## Use Case 1: IGP Source of Truth

### Problem

Network teams often lack a centralized, authoritative source for IGP routing configurations. Documentation exists in various forms (spreadsheets, wiki pages, diagrams) but quickly becomes outdated, leading to:

- Configuration drift between documented and actual state
- Difficulty planning changes without complete visibility
- Risk of errors during maintenance windows
- Challenges onboarding new team members

### Solution

Use the IGP Models app as the single source of truth for all IGP routing configurations.

### Implementation

1. **Initial Data Load**: Document all existing IGP configurations in Nautobot
   - Create IGP routing instances for each device/protocol combination
   - Add ISIS and OSPF configurations with accurate parameters
   - Configure all routing-enabled interfaces

2. **Validation**: Compare Nautobot data against actual device configurations
   - Use network automation tools to parse device configs
   - Identify discrepancies
   - Update Nautobot or devices to achieve consistency

3. **Maintenance**: Keep Nautobot updated as changes occur
   - Update IGP configs in Nautobot before deploying changes
   - Use Nautobot data to generate device configurations
   - Validate post-change that devices match Nautobot state

### Benefits

- Single source of truth for IGP routing design
- Accurate documentation always available
- Foundation for automation and validation
- Historical tracking via status fields and change logs

## Use Case 2: Configuration Generation

### Problem

Manually configuring ISIS or OSPF on devices is time-consuming and error-prone. Typing commands for each interface, ensuring correct metrics and areas, and maintaining consistency across devices leads to:

- Human errors (typos, wrong areas, incorrect metrics)
- Inconsistent configurations across similar devices
- Time wasted on repetitive tasks
- Difficulty maintaining standards

### Solution

Generate router configurations from IGP Models data using automation tools.

### Implementation Example (Ansible)

```yaml
---
- name: Generate ISIS Configuration
  hosts: routers
  tasks:
    - name: Get IGP Instance from Nautobot
      uri:
        url: "{{ nautobot_url }}/api/plugins/nautobot-igp-models/igp-routing-instances/"
        headers:
          Authorization: "Token {{ nautobot_token }}"
        method: GET
      register: igp_instances
      delegate_to: localhost

    - name: Get ISIS Configuration
      uri:
        url: "{{ nautobot_url }}/api/plugins/nautobot-igp-models/isis-configurations/"
        headers:
          Authorization: "Token {{ nautobot_token }}"
        method: GET
      register: isis_configs
      delegate_to: localhost

    - name: Generate ISIS Config
      template:
        src: isis_config.j2
        dest: "/tmp/{{ inventory_hostname }}_isis.cfg"
      delegate_to: localhost
```

**Template (isis_config.j2)**:

```jinja
router isis {{ isis_instance.isis_area }}
  net {{ isis_config.system_id }}
  is-type level-2-only
  metric-style wide

{% for interface in isis_interfaces %}
interface {{ interface.interface.name }}
  ip router isis {{ isis_instance.isis_area }}
  isis circuit-type {{ interface.circuit_type }}
  isis metric {{ interface.metric }}
{% endfor %}
```

### Benefits

- Consistent configurations across all devices
- Reduced configuration time
- Fewer errors
- Easy to implement design standards
- Reproducible configurations

## Use Case 3: ISIS to OSPF Migration

### Problem

Your organization is migrating from ISIS to OSPF. This requires:

- Running both protocols simultaneously during transition
- Tracking which devices have been migrated
- Ensuring OSPF is configured correctly before removing ISIS
- Maintaining documentation of current and target states

### Solution

Use IGP Models app to plan and track the migration.

### Implementation

1. **Document Current State**
   - Model all existing ISIS configurations with Status: "Active"
   - Include all interface configurations

2. **Design Target State**
   - Create OSPF configurations for same devices with Status: "Planned"
   - Map ISIS areas to OSPF areas
   - Configure OSPF on same interfaces

3. **Migration Execution**
   - Deploy OSPF alongside ISIS (both marked "Active")
   - Validate OSPF routing
   - Change ISIS configurations to Status: "Decommissioning"
   - Remove ISIS from devices
   - Update ISIS configurations to Status: "Decommissioned"

4. **Progress Tracking**
   - Filter by status to see migration progress
   - Generate reports showing completed vs. pending devices
   - Keep historical data for audit purposes

### Benefits

- Clear visibility into migration progress
- Both current and target state documented
- Historical record of migration
- Ability to roll back if needed
- Status-based filtering for reporting

## Use Case 4: Network Design Validation

### Problem

As the network grows, ensuring routing design consistency becomes challenging:

- Are all core routers in the same ISIS area?
- Do interface metrics follow the design standard?
- Are OSPF areas configured correctly at boundaries?
- Is the router ID assignment scheme followed?

### Solution

Use Nautobot's API and filtering to validate routing design rules.

### Implementation Example (Python Script)

```python
from pynautobot import api

nautobot = api(url="http://nautobot", token="TOKEN")

# Validation 1: All core routers should use ISIS area 49.0001
def validate_isis_area():
    core_devices = nautobot.dcim.devices.filter(role="core-router")

    for device in core_devices:
        igp_instances = nautobot.plugins.nautobot-igp-models.igp-routing-instances.filter(
            device_id=device.id,
            protocol="ISIS"
        )

        for instance in igp_instances:
            if instance.isis_area != "49.0001":
                print(f"❌ {device.name}: Invalid ISIS area {instance.isis_area}")
            else:
                print(f"✓ {device.name}: Correct ISIS area")

# Validation 2: All interfaces should have metrics between 1 and 100
def validate_isis_metrics():
    isis_interfaces = nautobot.plugins.nautobot-igp-models.isis-interface-configurations.all()

    for intf in isis_interfaces:
        if not (1 <= intf.metric <= 100):
            print(f"❌ {intf.interface.device.name} {intf.interface.name}: "
                  f"Metric {intf.metric} outside valid range")

# Validation 3: OSPF backbone area only on core routers
def validate_ospf_areas():
    ospf_interfaces = nautobot.plugins.nautobot-igp-models.ospf-interface-configurations.filter(
        area="0.0.0.0"
    )

    for intf in ospf_interfaces:
        device = intf.interface.device
        if device.role.name != "core-router":
            print(f"❌ {device.name}: Backbone area on non-core router")

# Run validations
validate_isis_area()
validate_isis_metrics()
validate_ospf_areas()
```

### Benefits

- Automated validation of design rules
- Early detection of configuration errors
- Consistent enforcement of standards
- CI/CD integration for pre-deployment checks

## Use Case 5: Multi-VRF Routing Documentation

### Problem

Large organizations often run multiple VRFs with separate IGP instances per VRF. Documenting which VRF uses which routing protocol and tracking interface assignments becomes complex.

### Solution

Leverage the VRF field in IGP Routing Instances to model multi-VRF routing.

### Implementation

1. **Create VRF-Specific Routing Instances**
   ```
   - Name: ISIS-CORE-01-GLOBAL, VRF: Global, Protocol: ISIS
   - Name: OSPF-CORE-01-MGMT, VRF: Management, Protocol: OSPF
   - Name: OSPF-CORE-01-CUST-A, VRF: Customer-A, Protocol: OSPF
   ```

2. **Configure Interfaces per VRF**
   - Assign interface configurations to appropriate VRF instances
   - Use filters to view configurations by VRF

3. **Generate VRF-Specific Configs**
   - Query API by VRF to generate configurations
   - Ensure interface assignments are correct

### Benefits

- Clear separation of routing instances by VRF
- Accurate multi-VRF documentation
- Simplified configuration generation per VRF
- Better understanding of VRF routing topology

## Common Workflows

### Workflow: Adding a New Router to ISIS Domain

1. Create Device in Nautobot
2. Add Interfaces
3. Assign IP Address for Router ID
4. Create IGP Routing Instance (Protocol: ISIS, ISIS Area: 49.0001)
5. Create ISIS Configuration (auto-generates NET)
6. Add ISIS Interface Configurations for each participating interface
7. Generate configuration from Nautobot data
8. Deploy to device
9. Validate ISIS neighbors form correctly

### Workflow: Changing OSPF Area Boundaries

1. Identify interfaces moving to new area
2. Update OSPF Interface Configurations in Nautobot
3. Generate updated configurations
4. Deploy during maintenance window
5. Validate OSPF neighbors re-establish
6. Verify routing tables are correct

### Workflow: Decommissioning a Router

1. Update IGP Routing Instance Status to "Decommissioning"
2. Update all related configs to "Decommissioning"
3. Remove from production
4. Update statuses to "Decommissioned"
5. Keep data for historical reference

## Integration Examples

### Ansible Integration

Use `nautobot.nautobot` collection to query IGP data in playbooks.

### Nornir Integration

Query Nautobot API in Nornir inventory to get IGP parameters for devices.

### CI/CD Integration

- Pre-deployment: Validate new configs against Nautobot design
- Post-deployment: Verify device state matches Nautobot data

### ChatOps Integration

Use Nautobot ChatOps to query IGP configurations from Slack/Teams.

## Summary

The IGP Models app supports a wide range of use cases from simple documentation to complex multi-VRF, multi-protocol environments with automated configuration generation and validation. The key is to start with your most pressing need and expand from there, building on Nautobot's extensibility to create workflows that match your organization's processes.
