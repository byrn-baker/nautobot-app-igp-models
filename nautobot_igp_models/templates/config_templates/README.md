# IGP Configuration Templates

This directory contains Jinja2 templates for generating IGP device configurations using the hybrid configuration inheritance system.

## Available Templates

### ISIS Templates (4 vendors)
- `cisco_ios_isis.j2` - Cisco IOS ISIS configuration
- `cisco_iosxr_isis.j2` - Cisco IOS XR ISIS configuration
- `juniper_isis.j2` - Juniper JunOS ISIS configuration
- `arista_eos_isis.j2` - Arista EOS ISIS configuration

### OSPF Templates (3 vendors)
- `cisco_ios_ospf.j2` - Cisco IOS OSPF configuration
- `cisco_iosxr_ospf.j2` - Cisco IOS XR OSPF configuration
- `arista_eos_ospf.j2` - Arista EOS OSPF configuration

## Usage

### Python Example

```python
from django.template.loader import get_template
from nautobot_igp_models.models import ISISConfiguration, ISISInterfaceConfiguration

# Get ISIS configuration and interfaces
isis_config = ISISConfiguration.objects.get(name="ISIS-Core")
interfaces = isis_config.interface_configurations.all()

# Load template
template = get_template('config_templates/cisco_ios_isis.j2')

# Render configuration
config = template.render({
    'isis_config': isis_config,
    'interfaces': interfaces,
})

print(config)
```

### Nautobot Job Example

```python
from nautobot.apps.jobs import Job, ObjectVar
from nautobot_igp_models.models import ISISConfiguration
from django.template.loader import get_template

class GenerateISISConfigJob(Job):
    """Generate ISIS configuration for a device."""

    isis_config = ObjectVar(
        model=ISISConfiguration,
        description="ISIS Configuration to generate"
    )

    vendor = StringVar(
        description="Vendor platform",
        default="cisco_ios",
        choices=[
            ("cisco_ios", "Cisco IOS"),
            ("juniper", "Juniper JunOS"),
        ]
    )

    class Meta:
        name = "Generate ISIS Configuration"
        description = "Generate device configuration using inheritance"

    def run(self, isis_config, vendor):
        """Generate configuration."""
        interfaces = isis_config.interface_configurations.all()

        # Select appropriate template
        template_name = f'config_templates/{vendor}_isis.j2'
        template = get_template(template_name)

        # Render configuration
        config = template.render({
            'isis_config': isis_config,
            'interfaces': interfaces,
        })

        self.logger.info(f"Generated configuration for {isis_config.instance.device.name}")
        self.logger.info(config)

        return config
```

### Export Template Usage

You can also use these as Nautobot Export Templates:

1. Go to **Extensibility > Export Templates**
2. Create a new Export Template:
   - **Content Type**: ISISConfiguration
   - **Template Code**: Copy content from `cisco_ios_isis.j2`
   - **File Extension**: `txt`
3. On an ISIS Configuration detail page, click "Export" to generate config

## Configuration Inheritance

These templates leverage the hybrid inheritance system:

### Database Fields (Always Available)
```python
# Access core parameters
effective_metric = interface_config.get_effective_metric()  # 15
circuit_type = interface_config.circuit_type  # "L2"

# Get complete effective config
config = interface_config.get_effective_config()
# {
#     'metric': 15,
#     'circuit_type': 'L2',
#     'hello_interval': 10,
#     'priority': 64
# }
```

### Config Context (Flexible Settings)
```python
# Get vendor-specific config
cisco_config = interface_config.get_vendor_config('cisco')
# {
#     'bfd': {'enabled': True, 'interval': 50},
#     'mpls_traffic_eng': True
# }
```

## Example Config Context

### Device-Level (Applies to all interfaces)

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
                "metric_style": "wide"
            },
            "juniper": {
                "bfd_liveness_detection": {
                    "minimum_interval": 300,
                    "multiplier": 3
                },
                "link_protection": true,
                "wide_metrics_only": true
            }
        }
    }
}
```

### Interface-Level (Overrides device settings)

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

## Generated Configuration Example

### Input Data

```python
# ISIS Config
isis_config.name = "ISIS-Core"
isis_config.default_metric = 15
isis_config.default_hello_interval = 5

# Interface 1 - Inherits defaults
interface1.interface.name = "GigabitEthernet0/0/1"
interface1.metric = None  # Inherits 15
interface1.circuit_type = "L2"

# Interface 2 - Override metric
interface2.interface.name = "GigabitEthernet0/0/2"
interface2.metric = 50  # Explicit override
interface2.circuit_type = "L2"

# Config Context (device-level)
{
    "igp": {
        "isis": {
            "cisco": {
                "bfd": {"enabled": true},
                "mpls_traffic_eng": true
            }
        }
    }
}
```

### Output (Cisco IOS)

```
!
! ISIS Configuration for router1
!
router isis ISIS-Core
 net 49.0001.0192.0168.0001.00
 is-type level-2-only
 metric-style wide
 log-adjacency-changes
!
!
interface GigabitEthernet0/0/1
 description ISIS ISIS-Core - L2
 ip router isis ISIS-Core
 isis circuit-type level-2
 isis metric 15
 isis hello-interval 5
 isis bfd
 isis mpls traffic-eng level-2
!
!
interface GigabitEthernet0/0/2
 description ISIS ISIS-Core - L2
 ip router isis ISIS-Core
 isis circuit-type level-2
 isis metric 50
 isis hello-interval 5
 isis bfd
 isis mpls traffic-eng level-2
!
!
! End of ISIS configuration
!
```

## Adding New Templates

To add a new vendor template:

1. Create a new `.j2` file in this directory
2. Use `get_effective_config()` for core parameters
3. Use `get_vendor_config('vendor_name')` for vendor settings
4. Document required config context structure
5. Test with actual device configurations

## Config Context Validation

The app provides JSON Schema files for validating config context structure:

- **ISIS Schema:** `../../schemas/config_context_isis.json`
- **OSPF Schema:** `../../schemas/config_context_ospf.json`
- **Schema Documentation:** `../../schemas/README.md`

Use these schemas to validate your config context before applying it to devices.

## See Also

- [Configuration Inheritance Documentation](../../../docs/user/configuration_inheritance.md)
- [Config Context Schemas](../../schemas/README.md)
- [App Usage Guide](../../../docs/user/app_use_cases.md)
- [Jinja2 Documentation](https://jinja.palletsprojects.com/)
