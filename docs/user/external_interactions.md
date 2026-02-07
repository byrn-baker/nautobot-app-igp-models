# External Interactions

This document describes external dependencies and prerequisites for this App to operate, including system requirements, API endpoints, interconnection or integrations to other applications or services, and similar topics.

## External System Integrations

### From the App to Other Systems

The Nautobot IGP Models app can export data to external systems through:

- **REST API**: External systems can query IGP configuration data via the Nautobot REST API
- **GraphQL API**: IGP models are accessible through Nautobot's GraphQL interface for flexible queries
- **Webhooks**: Nautobot's webhook functionality can notify external systems of changes to IGP configurations

### From Other Systems to the App

External systems can interact with the app through:

- **REST API**: External automation tools can create, update, or delete IGP configurations
- **Management Commands**: Bulk import operations can be performed using custom management commands
- **Nautobot Jobs**: Custom Jobs can be created to import or sync IGP data from network devices or other sources

## Nautobot REST API Endpoints

The app provides the following REST API endpoints:

### IGP Routing Instances

- `GET /api/plugins/igp-models/igp-routing-instances/` - List all routing instances
- `POST /api/plugins/igp-models/igp-routing-instances/` - Create a routing instance
- `GET /api/plugins/igp-models/igp-routing-instances/{id}/` - Retrieve a specific routing instance
- `PUT /api/plugins/igp-models/igp-routing-instances/{id}/` - Update a routing instance
- `DELETE /api/plugins/igp-models/igp-routing-instances/{id}/` - Delete a routing instance

### ISIS Configurations

- `GET /api/plugins/igp-models/isis-configurations/` - List all ISIS configurations
- `POST /api/plugins/igp-models/isis-configurations/` - Create an ISIS configuration
- `GET /api/plugins/igp-models/isis-configurations/{id}/` - Retrieve a specific ISIS configuration
- `PUT /api/plugins/igp-models/isis-configurations/{id}/` - Update an ISIS configuration
- `DELETE /api/plugins/igp-models/isis-configurations/{id}/` - Delete an ISIS configuration

### ISIS Interface Configurations

- `GET /api/plugins/igp-models/isis-interface-configurations/` - List all ISIS interface configurations
- `POST /api/plugins/igp-models/isis-interface-configurations/` - Create an ISIS interface configuration
- `GET /api/plugins/igp-models/isis-interface-configurations/{id}/` - Retrieve a specific ISIS interface configuration
- `PUT /api/plugins/igp-models/isis-interface-configurations/{id}/` - Update an ISIS interface configuration
- `DELETE /api/plugins/igp-models/isis-interface-configurations/{id}/` - Delete an ISIS interface configuration

### OSPF Configurations

- `GET /api/plugins/igp-models/ospf-configurations/` - List all OSPF configurations
- `POST /api/plugins/igp-models/ospf-configurations/` - Create an OSPF configuration
- `GET /api/plugins/igp-models/ospf-configurations/{id}/` - Retrieve a specific OSPF configuration
- `PUT /api/plugins/igp-models/ospf-configurations/{id}/` - Update an OSPF configuration
- `DELETE /api/plugins/igp-models/ospf-configurations/{id}/` - Delete an OSPF configuration

### OSPF Interface Configurations

- `GET /api/plugins/igp-models/ospf-interface-configurations/` - List all OSPF interface configurations
- `POST /api/plugins/igp-models/ospf-interface-configurations/` - Create an OSPF interface configuration
- `GET /api/plugins/igp-models/ospf-interface-configurations/{id}/` - Retrieve a specific OSPF interface configuration
- `PUT /api/plugins/igp-models/ospf-interface-configurations/{id}/` - Update an OSPF interface configuration
- `DELETE /api/plugins/igp-models/ospf-interface-configurations/{id}/` - Delete an OSPF interface configuration

### API Usage Examples

#### Python Request Example

```python
import requests

# Nautobot API configuration
NAUTOBOT_URL = "https://nautobot.example.com"
API_TOKEN = "your-api-token-here"
HEADERS = {
    "Authorization": f"Token {API_TOKEN}",
    "Content-Type": "application/json",
}

# Get all IGP routing instances
response = requests.get(
    f"{NAUTOBOT_URL}/api/plugins/igp-models/igp-routing-instances/",
    headers=HEADERS
)
routing_instances = response.json()

# Create a new ISIS configuration
isis_config = {
    "routing_instance": "uuid-of-routing-instance",
    "net_address": "49.0001.1234.5678.9012.00",
    "area_authentication_mode": "md5",
    "area_authentication_key": "secret123",
}
response = requests.post(
    f"{NAUTOBOT_URL}/api/plugins/igp-models/isis-configurations/",
    headers=HEADERS,
    json=isis_config
)
```

#### cURL Example

```bash
# Get all OSPF configurations
curl -X GET \
  https://nautobot.example.com/api/plugins/igp-models/ospf-configurations/ \
  -H "Authorization: Token your-api-token-here" \
  -H "Content-Type: application/json"

# Create a new routing instance
curl -X POST \
  https://nautobot.example.com/api/plugins/igp-models/igp-routing-instances/ \
  -H "Authorization: Token your-api-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "device": "device-uuid",
    "routing_protocol": "ISIS",
    "routing_instance_name": "default"
  }'
```

## Integration with Network Automation Tools

The app integrates well with common network automation tools:

- **Ansible**: Use the `nautobot.nautobot` collection to interact with IGP models
- **Terraform**: Use the Nautobot provider to manage IGP configurations as infrastructure-as-code
- **Python Scripts**: Use the `pynautobot` library for programmatic access
- **CI/CD Pipelines**: Integrate API calls into your continuous integration workflows

## Prerequisites

- Nautobot 2.0 or later
- Valid devices with interfaces defined in Nautobot
- Appropriate user permissions for creating and managing IGP configurations
