# Configuration Inheritance

The Nautobot IGP Models app uses a **hybrid approach** for managing IGP configuration parameters, combining database fields with Nautobot's config context for maximum flexibility.

## Overview

Configuration values are inherited through a priority chain:

1. **Interface-specific database fields** (highest priority)
2. **Protocol configuration defaults** (database)
3. **Device config context** (flexible/optional settings)
4. **Global protocol defaults** (lowest priority)

This approach provides:
- **Type safety** for core protocol parameters (database fields)
- **Flexibility** for optional/vendor-specific settings (config context)
- **Inheritance** to reduce repetitive configuration
- **Overrides** at any level

## ISIS Configuration Inheritance

### Database Fields (Core Parameters)

ISIS Configuration model provides default values that interfaces inherit:

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `default_metric` | Integer | None | Default metric for ISIS interfaces |
| `default_hello_interval` | Integer | None | Default hello interval in seconds |
| `default_hello_multiplier` | Integer | None | Default hello multiplier |
| `default_priority` | Integer | None | Default DIS priority |

ISIS Interface Configuration model:

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `metric` | Integer | None | Interface-specific metric (overrides default) |
| `circuit_type` | Choice | L1L2 | ISIS circuit type (L1, L2, L1L2) |

### Example: ISIS with Database Inheritance

```python
# Create ISIS configuration with defaults
isis_config = ISISConfiguration.objects.create(
    name="ISIS-Core",
    instance=igp_instance,
    default_metric=15,  # All interfaces inherit this
    default_hello_interval=5,
    status=status_active
)

# Interface 1: Inherits default_metric=15
isis_int1 = ISISInterfaceConfiguration.objects.create(
    name="ISIS-Gi0/0/1",
    isis_config=isis_config,
    device=router1,
    interface=gi001,
    circuit_type="L2",
    # metric is None, inherits 15 from isis_config
    status=status_active
)

# Interface 2: Override with higher cost
isis_int2 = ISISInterfaceConfiguration.objects.create(
    name="ISIS-Gi0/0/2",
    isis_config=isis_config,
    device=router1,
    interface=gi002,
    circuit_type="L2",
    metric=50,  # Explicit override
    status=status_active
)

# Get effective configuration
print(isis_int1.get_effective_metric())  # Returns: 15 (inherited)
print(isis_int2.get_effective_metric())  # Returns: 50 (overridden)
```

### Example: ISIS with Config Context

**Device-level config context** (applies to all interfaces):

```json
{
    "igp": {
        "isis": {
            "hello_interval": 5,
            "hello_multiplier": 4,
            "authentication": {
                "type": "md5",
                "level": "level-2"
            },
            "cisco": {
                "bfd": {
                    "enabled": true,
                    "interval": 50,
                    "min_rx": 50,
                    "multiplier": 3
                },
                "mpls_traffic_eng": true
            }
        }
    }
}
```

**Interface-level config context** (overrides device-level):

```json
{
    "igp": {
        "isis": {
            "hello_interval": 30,
            "cisco": {
                "bfd": {
                    "interval": 300
                }
            }
        }
    }
}
```

**Access effective configuration:**

```python
# Get complete effective config
config = isis_interface.get_effective_config()
# Returns:
# {
#     'metric': 15,
#     'circuit_type': 'L2',
#     'hello_interval': 30,  # From interface config context
#     'hello_multiplier': 4,  # From device config context
#     'priority': 64,  # Global default
# }

# Get vendor-specific config
cisco_config = isis_interface.get_vendor_config('cisco')
# Returns:
# {
#     'bfd': {'enabled': True, 'interval': 300, ...},
#     'mpls_traffic_eng': True
# }
```

## OSPF Configuration Inheritance

### Database Fields (Core Parameters)

OSPF Configuration model provides default values:

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `default_cost` | Integer | None | Default cost for OSPF interfaces |
| `default_hello_interval` | Integer | None | Default hello interval in seconds |
| `default_dead_interval` | Integer | None | Default dead interval in seconds |
| `default_priority` | Integer | None | Default router priority |

OSPF Interface Configuration model:

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `cost` | Integer | None | Interface-specific cost (overrides default) |
| `area` | String | Required | OSPF area (e.g., 0.0.0.0) |

### Example: OSPF with Database Inheritance

```python
# Create OSPF configuration with defaults
ospf_config = OSPFConfiguration.objects.create(
    name="OSPF-Core",
    instance=ospf_instance,
    process_id=1,
    default_cost=10,  # All interfaces inherit this
    default_hello_interval=5,
    default_dead_interval=20,
    status=status_active
)

# Interface inherits default_cost=10
ospf_int = OSPFInterfaceConfiguration.objects.create(
    name="OSPF-Gi0/0/1",
    ospf_config=ospf_config,
    interface=gi001,
    area="0.0.0.0",
    # cost is None, inherits 10 from ospf_config
    status=status_active
)

print(ospf_int.get_effective_cost())  # Returns: 10 (inherited)
```

### Example: OSPF with Config Context

**Device-level config context:**

```json
{
    "igp": {
        "ospf": {
            "hello_interval": 10,
            "dead_interval": 40,
            "authentication": {
                "type": "message-digest",
                "key_id": 1
            },
            "cisco": {
                "bfd": {
                    "enabled": true
                },
                "fast_reroute": "per-prefix"
            }
        }
    }
}
```

## Configuration Generation

### Generate Cisco IOS Configuration

```python
def generate_cisco_isis_config(interface_config):
    """Generate Cisco IOS ISIS configuration from interface config."""
    effective = interface_config.get_effective_config()
    vendor = interface_config.get_vendor_config('cisco')

    lines = [
        f"interface {interface_config.interface.name}",
        f" ip router isis {interface_config.isis_config.name}",
        f" isis circuit-type {effective['circuit_type'].lower()}",
        f" isis metric {effective['metric']}",
    ]

    # Optional parameters from config context
    if 'hello_interval' in effective:
        lines.append(f" isis hello-interval {effective['hello_interval']}")

    if 'hello_multiplier' in effective:
        lines.append(f" isis hello-multiplier {effective['hello_multiplier']}")

    # Vendor-specific features
    if vendor.get('bfd', {}).get('enabled'):
        lines.append(" isis bfd")

    if vendor.get('mpls_traffic_eng'):
        lines.append(" isis mpls traffic-eng level-2")

    return "\n".join(lines)

# Usage
config_text = generate_cisco_isis_config(isis_interface)
print(config_text)
```

**Output:**
```
interface GigabitEthernet0/0/1
 ip router isis ISIS-Core
 isis circuit-type level-2
 isis metric 15
 isis hello-interval 30
 isis hello-multiplier 4
 isis bfd
 isis mpls traffic-eng level-2
```

## Best Practices

### Use Database Fields For:

1. **Required protocol parameters** that define core functionality
   - ISIS: metric, circuit_type
   - OSPF: cost, area

2. **Values you need to query/filter on**
   - "Find all interfaces with ISIS metric > 50"
   - "Show all OSPF interfaces in area 0.0.0.0"

3. **Settings that require validation**
   - Area formats, metric ranges

### Use Config Context For:

1. **Optional protocol parameters**
   - Hello timers, authentication
   - Can vary by environment

2. **Vendor-specific features**
   - BFD, MPLS traffic engineering
   - Different per vendor

3. **Organization-specific defaults**
   - Standard hello intervals
   - Authentication policies

4. **Settings that reference secrets**
   - Authentication keys
   - MD5 passwords

## Config Context Schema

### JSON Schema Validation

The app provides JSON Schema files for validating config context structure:

- **ISIS:** [nautobot_igp_models/schemas/config_context_isis.json](../../nautobot_igp_models/schemas/config_context_isis.json)
- **OSPF:** [nautobot_igp_models/schemas/config_context_ospf.json](../../nautobot_igp_models/schemas/config_context_ospf.json)
- **Documentation:** [schemas/README.md](../../nautobot_igp_models/schemas/README.md)

These schemas provide:
- Type validation (integers, booleans, strings)
- Range constraints (e.g., hello_interval: 1-65535)
- Enum validation (e.g., authentication types)
- Vendor-specific parameter definitions
- Multiple examples for each use case

### Recommended Structure

```json
{
    "igp": {
        "isis": {
            // Common protocol settings
            "hello_interval": 10,
            "hello_multiplier": 3,
            "priority": 64,

            // Authentication
            "authentication": {
                "type": "md5",
                "level": "level-2",
                "key": "{{ secrets.isis_auth_key }}"
            },

            // Vendor-specific settings
            "cisco": {
                "bfd": {
                    "enabled": true,
                    "interval": 50,
                    "min_rx": 50,
                    "multiplier": 3
                },
                "mpls_traffic_eng": true,
                "metric_style": "wide"
            },
            "juniper": {
                "bfd_liveness_detection": {
                    "minimum_interval": 300,
                    "multiplier": 3
                },
                "link_protection": true
            }
        },
        "ospf": {
            // Common protocol settings
            "hello_interval": 10,
            "dead_interval": 40,
            "priority": 1,

            // Authentication
            "authentication": {
                "type": "md5",
                "key_id": 1,
                "key": "{{ secrets.ospf_auth_key }}"
            },

            // Vendor-specific settings
            "cisco": {
                "bfd": {
                    "enabled": true
                },
                "fast_reroute": {
                    "per_prefix": true
                }
            }
        }
    }
}
```

### Validating Config Context

Use the JSON schemas to validate your config context:

```python
import json
from jsonschema import validate, ValidationError

# Load schema
with open('nautobot_igp_models/schemas/config_context_isis.json') as f:
    schema = json.load(f)

# Validate config context
config_context = {
    "igp": {
        "isis": {
            "hello_interval": 5,
            "cisco": {"bfd": {"enabled": True}}
        }
    }
}

try:
    validate(instance=config_context, schema=schema)
    print("✓ Valid config context")
except ValidationError as e:
    print(f"✗ Validation error: {e.message}")
```

## API Usage

### Create Configuration with Defaults

```bash
# Create ISIS config with defaults
curl -X POST "http://nautobot/api/plugins/nautobot-igp-models/isis-configurations/" \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "ISIS-Core",
    "instance": "UUID_OF_IGP_INSTANCE",
    "default_metric": 15,
    "default_hello_interval": 5,
    "status": "UUID_OF_STATUS"
  }'

# Create interface that inherits defaults
curl -X POST "http://nautobot/api/plugins/nautobot-igp-models/isis-interface-configurations/" \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "ISIS-Gi0/0/1",
    "isis_config": "UUID_OF_ISIS_CONFIG",
    "device": "UUID_OF_DEVICE",
    "interface": "UUID_OF_INTERFACE",
    "circuit_type": "L2",
    "status": "UUID_OF_STATUS"
  }'
```

## Migration Guide

If you have existing configurations without default values:

1. **Default values are optional** - Leave them blank to maintain current behavior
2. **Add defaults gradually** - Start with commonly used values
3. **Use config context** - For environment-specific settings

Example migration:

```python
# Add default metric to existing ISIS configs
for isis_config in ISISConfiguration.objects.all():
    # Analyze interface metrics
    interface_metrics = isis_config.interface_configurations.all().values_list('metric', flat=True)
    most_common_metric = Counter(interface_metrics).most_common(1)[0][0]

    # Set as default
    isis_config.default_metric = most_common_metric
    isis_config.save()
```

## See Also

- [Nautobot Config Context Documentation](https://docs.nautobot.com/projects/core/en/stable/user-guide/platform-functionality/configcontext/)
- [App Overview](app_overview.md)
- [External Interactions](external_interactions.md)
