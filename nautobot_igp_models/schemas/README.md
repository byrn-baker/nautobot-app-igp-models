# IGP Config Context Schemas

This directory contains JSON Schema files for validating IGP configuration parameters in Nautobot config context.

## Available Schemas

### ISIS Config Context Schema
**File:** [config_context_isis.json](config_context_isis.json)

Validates ISIS configuration parameters including:
- **Core Parameters:** hello_interval, hello_multiplier, priority
- **Authentication:** MD5, HMAC-SHA, simple text
- **Vendor-Specific Settings:**
  - **Cisco IOS/IOS-XE:** BFD, MPLS-TE, metric style, FRR, passive
  - **Juniper JunOS:** BFD liveness detection, link protection, wide metrics, reference bandwidth
  - **Arista EOS:** BFD, segment routing
  - **Nokia SR OS:** BFD, LDP sync

### OSPF Config Context Schema
**File:** [config_context_ospf.json](config_context_ospf.json)

Validates OSPF configuration parameters including:
- **Core Parameters:** hello_interval, dead_interval, priority, network_type
- **Authentication:** MD5, simple text, null
- **Vendor-Specific Settings:**
  - **Cisco IOS/IOS-XE:** BFD, MPLS-TE, FRR, MTU ignore, passive, demand circuit
  - **Juniper JunOS:** BFD liveness detection, link protection, reference bandwidth, flood reduction
  - **Arista EOS:** BFD, segment routing
  - **Nokia SR OS:** BFD, LDP sync

## Usage

### In Nautobot UI

1. Navigate to **Extensibility > Config Contexts**
2. Create a new Config Context
3. In the **Data** field, reference the schema:
   ```json
   {
     "$schema": "/static/nautobot_igp_models/schemas/config_context_isis.json",
     "igp": {
       "isis": {
         "hello_interval": 5
       }
     }
   }
   ```

### Programmatic Validation

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
            "cisco": {
                "bfd": {"enabled": True}
            }
        }
    }
}

try:
    validate(instance=config_context, schema=schema)
    print("✓ Valid config context")
except ValidationError as e:
    print(f"✗ Validation error: {e.message}")
```

### In CI/CD Pipeline

```bash
# Install JSON schema validator
pip install jsonschema check-jsonschema

# Validate config context files
check-jsonschema \
  --schemafile nautobot_igp_models/schemas/config_context_isis.json \
  config_contexts/isis/*.json
```

## Schema Features

### Type Safety
- Integer ranges validated (e.g., hello_interval: 1-65535)
- Enum values enforced (e.g., authentication type: simple, md5, hmac-sha-1)
- Required fields specified where applicable

### Vendor Separation
Vendor-specific settings are namespaced:
```json
{
  "igp": {
    "isis": {
      "hello_interval": 5,     // Common parameter
      "cisco": {                // Cisco-specific
        "mpls_traffic_eng": true
      },
      "juniper": {              // Juniper-specific
        "link_protection": true
      }
    }
  }
}
```

### Examples Included
Each schema includes multiple realistic examples showing:
- Device-level configuration (applies to all interfaces)
- Interface-level configuration (overrides device settings)
- Vendor-specific features
- Authentication with secret references

## Examples

### Device-Level ISIS Configuration (Cisco)

```json
{
  "igp": {
    "isis": {
      "hello_interval": 5,
      "authentication": {
        "type": "md5",
        "level": "level-2",
        "key": "{{ secrets.isis_key }}"
      },
      "cisco": {
        "bfd": {
          "enabled": true,
          "interval": 50
        },
        "mpls_traffic_eng": true,
        "metric_style": "wide",
        "log_adjacency_changes": true
      }
    }
  }
}
```

### Interface-Level ISIS Configuration Override

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

### Device-Level OSPF Configuration (Juniper)

```json
{
  "igp": {
    "ospf": {
      "hello_interval": 1,
      "dead_interval": 3,
      "network_type": "point-to-point",
      "juniper": {
        "bfd_liveness_detection": {
          "minimum_interval": 300,
          "multiplier": 3
        },
        "link_protection": true,
        "reference_bandwidth": "100g"
      }
    }
  }
}
```

### Multi-Vendor Configuration

```json
{
  "igp": {
    "isis": {
      "hello_interval": 5,
      "cisco": {
        "bfd": {"enabled": true},
        "mpls_traffic_eng": true
      },
      "juniper": {
        "bfd_liveness_detection": {
          "minimum_interval": 300,
          "multiplier": 3
        },
        "link_protection": true
      }
    }
  }
}
```

## Inheritance Chain

Config context parameters follow this inheritance priority:

1. **Interface-specific database fields** (highest priority)
   - Example: `ISISInterfaceConfiguration.metric = 50`

2. **Protocol configuration defaults** (database)
   - Example: `ISISConfiguration.default_metric = 15`

3. **Interface config context** (flexible, interface-level)
   - Example: Interface config context with `hello_interval: 30`

4. **Device config context** (flexible, device-level)
   - Example: Device config context with `hello_interval: 5`

5. **Global protocol defaults** (fallback)
   - Example: Default ISIS metric = 10

## Adding New Vendor Support

To add a new vendor (e.g., Huawei):

1. Add vendor section to schema:
```json
"huawei": {
  "type": "object",
  "properties": {
    "bfd": {
      "type": "boolean",
      "description": "Enable BFD"
    }
  },
  "description": "Huawei VRP specific ISIS settings"
}
```

2. Create Jinja2 template in `templates/config_templates/huawei_isis.j2`

3. Update template README with Huawei examples

4. Test with actual device configuration

## Validation Best Practices

1. **Always validate before applying** - Use schema validation in your automation
2. **Use secret references** - Never hardcode passwords: `{{ secrets.key_name }}`
3. **Test vendor sections** - Ensure vendor config works on actual devices
4. **Document custom parameters** - Add descriptions to all properties
5. **Version control schemas** - Track schema changes with git

## See Also

- [Configuration Inheritance Documentation](../../../docs/user/configuration_inheritance.md)
- [Configuration Templates README](../templates/config_templates/README.md)
- [JSON Schema Documentation](https://json-schema.org/)
- [Nautobot Config Context Documentation](https://docs.nautobot.com/projects/core/en/stable/user-guide/platform-functionality/configcontext/)
