# v1.0 Release Notes

This document describes all new features and changes in the release `1.0`. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Release Overview

The initial 1.0 release of the Nautobot IGP Models app introduces comprehensive support for Interior Gateway Protocol (IGP) modeling within Nautobot. This release provides data models and management capabilities for both ISIS and OSPF routing protocols.

Key features in this release:

- Core IGP routing instance model supporting multiple routing protocol instances per device
- ISIS protocol support with configuration and interface-level settings
- OSPF protocol support with configuration and interface-level settings
- REST API endpoints for all models
- Comprehensive filtering and search capabilities
- Management commands for data import and validation

This release is compatible with Nautobot 2.0 and later versions.

## [v1.0.0] - 2025-02-07

### Added

- IGP Routing Instance model for managing routing protocol instances on devices
- ISIS Configuration model with support for NET addresses, area authentication, and protocol settings
- ISIS Interface Configuration model for interface-level ISIS parameters
- OSPF Configuration model with support for router ID, area configuration, and protocol settings
- OSPF Interface Configuration model for interface-level OSPF parameters
- REST API serializers and viewsets for all models
- Comprehensive filtering capabilities for all models
- Form validation for protocol-specific configurations
- Management commands for bulk operations
- Template-based detail views for routing instances and configurations
- Navigation menu integration
- Test coverage for models, forms, filters, and API endpoints

### Changed

- N/A (initial release)

### Fixed

- N/A (initial release)
