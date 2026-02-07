# App Overview

This document provides an overview of the Nautobot IGP Models app including critical information and important considerations when applying it to your Nautobot environment.

!!! note
    Throughout this documentation, the terms "app" and "plugin" will be used interchangeably.

## Description

The Nautobot IGP Models app provides comprehensive data models for managing Interior Gateway Protocol (IGP) routing configurations in Nautobot. This app extends Nautobot's core functionality to enable detailed modeling of ISIS and OSPF routing instances, process configurations, and interface-level routing parameters.

The app is designed to serve as a source of truth for IGP routing configurations across your network infrastructure, supporting use cases from network documentation and validation to configuration generation and automation workflows.

### Key Capabilities

- **IGP Routing Instances**: Model routing instances per device with protocol selection (ISIS or OSPF), router IDs, VRF assignment, and ISIS area configuration
- **ISIS Configuration**: Manage ISIS-specific settings including automatic NET (Network Entity Title) generation from router IDs and area identifiers
- **ISIS Interface Configuration**: Define interface-level ISIS parameters including circuit types (Level 1, Level 2, Level 1-2) and metrics
- **OSPF Configuration**: Track OSPF process configurations with customizable process IDs
- **OSPF Interface Configuration**: Configure interface-level OSPF parameters including areas and costs
- **Status Management**: Lifecycle tracking with configurable statuses (Planned, Active, Decommissioned, etc.)
- **Full API Access**: Complete REST API for programmatic access and integration with automation tools

## Models

The app provides five main data models:

### IGPRoutingInstance (Base Model)

The foundational model representing a routing instance on a specific device. Each instance specifies:

- Device association
- Protocol type (ISIS or OSPF)
- Router ID (IP Address reference)
- VRF assignment
- ISIS area (for ISIS protocol)
- Status and description

Unique constraint: Each device can have only one routing instance per protocol/VRF combination.

### ISISConfiguration

ISIS-specific configuration linked to an IGP routing instance. Features include:

- Automatic NET generation from router ID and ISIS area
- Manual NET override capability
- Support for standard ISIS NET format (AA.BBBB.XXXX.XXXX.XXXX.CC)

### ISISInterfaceConfiguration

Interface-level ISIS configuration supporting:

- Circuit types: Level 1, Level 2, or Level 1-2
- Configurable metrics
- Per-interface status tracking
- Device and interface associations for validation

### OSPFConfiguration

OSPF process configuration with:

- Customizable process IDs
- Multiple processes per device support
- Linked to OSPF-type routing instances only

### OSPFInterfaceConfiguration

Interface-level OSPF parameters including:

- OSPF area assignment (supports both dotted-decimal and integer formats)
- Interface cost configuration
- Per-interface status tracking

## Audience (User Personas)

This app is designed for:

- **Network Engineers**: Maintain accurate documentation of IGP routing configurations, plan network changes, and validate routing design consistency
- **Network Automation Engineers**: Generate device configurations from structured data, integrate with CI/CD pipelines, and maintain infrastructure-as-code workflows
- **Network Architects**: Design and document routing topologies, plan migrations between protocols, and ensure standardization across the network
- **NOC/Operations Teams**: Reference current routing configurations, track configuration lifecycle states, and correlate routing issues with documented designs

## Authors and Maintainers

- **Primary Author**: Byrn Baker
- **Contributors**: Community contributors via GitHub

For contribution guidelines, see the [Developer Guide](../dev/contributing.md).

## Nautobot Features Used

The IGP Models app leverages Nautobot's extensibility framework and integrates with core Nautobot models:

### Core Model Integration

- **Device Model**: IGP routing instances are associated with specific devices
- **Interface Model**: Interface-level configurations reference device interfaces
- **IPAddress Model**: Router IDs reference IP address objects
- **VRF Model**: Routing instances can be associated with VRFs
- **Status Model**: All configuration objects support status tracking

### Nautobot Extras Framework

The app fully utilizes Nautobot's extras features:

- **Custom Fields**: Add custom fields to any IGP model for site-specific requirements
- **Custom Links**: Create custom links to external systems or documentation
- **Relationships**: Define relationships between IGP objects and other Nautobot models
- **Webhooks**: Trigger external actions on IGP configuration changes
- **Export Templates**: Generate configuration snippets or documentation exports
- **GraphQL**: Query IGP data via Nautobot's GraphQL API
- **Status Fields**: Configurable status values for lifecycle management
- **Tags**: Organize and categorize configurations with tags

### UI Features

- **Navigation**: Dedicated "Routing" → "IGP - Link-State" navigation menu
- **List Views**: Filterable tables for all model types
- **Detail Views**: Comprehensive object detail pages with related objects
- **Forms**: Intelligent forms with dynamic field behavior and validation
- **Bulk Operations**: Bulk edit and bulk delete capabilities
- **CSV Import/Export**: Import and export data via CSV

### API Features

- **REST API**: Full CRUD operations for all models
- **Filtering**: Advanced filtering on all object attributes
- **Bulk Operations**: Bulk create and update via API
- **Token Authentication**: Secure API access with token-based auth
- **OpenAPI Schema**: Auto-generated API documentation

## Demo Data

The app includes a management command to load realistic demo data for testing and evaluation:

```bash
nautobot-server load_igp_demo_data
```

This creates a four-router topology with ISIS and OSPF configurations, useful for:

- Testing the app in a development environment
- Generating documentation screenshots
- Understanding the data model relationships
- Demonstrating the app to stakeholders

For more details, see the [Getting Started Guide](app_getting_started.md).
