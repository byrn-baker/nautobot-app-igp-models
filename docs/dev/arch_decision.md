# Architecture Decision Records

The intention is to document deviations from a standard Model View Controller (MVC) design.

## Model Hierarchy Design

### Decision

The IGP Models app uses a hierarchical model structure with `IGPRoutingInstance` as the parent model and protocol-specific configurations (ISIS, OSPF) as child models. Interface configurations are further children of their respective protocol configurations.

### Rationale

- **Flexibility**: Devices can have multiple routing instances, each potentially running different IGP protocols
- **Extensibility**: New IGP protocols (e.g., EIGRP, RIP) can be added without modifying existing models
- **Data Integrity**: Foreign key relationships ensure referential integrity between routing instances, protocol configurations, and interface configurations
- **Separation of Concerns**: Protocol-specific settings are isolated in their respective models, avoiding model bloat

### Consequences

- Queries may require joins across multiple tables
- Each protocol requires its own set of configuration models
- Changes to common routing instance attributes require updates to the parent model only

## Protocol-Specific Configuration Models

### Decision

Each IGP protocol (ISIS, OSPF) has dedicated configuration models rather than using a single polymorphic model with protocol-type fields.

### Rationale

- **Type Safety**: Protocol-specific fields are strongly typed and validated
- **Clarity**: Each model clearly represents its protocol's configuration options
- **Maintainability**: Protocol configurations can evolve independently
- **API Design**: REST API endpoints are clean and protocol-specific

### Consequences

- More models to maintain
- Code duplication for similar functionality across protocols
- Clearer separation and easier testing

## Interface Configuration Approach

### Decision

Interface configurations are stored in separate models (ISISInterfaceConfiguration, OSPFInterfaceConfiguration) linked to both the protocol configuration and the Nautobot Interface model.

### Rationale

- **Granularity**: Interface-level settings can be managed independently
- **Flexibility**: Interfaces can be added/removed from IGP participation without affecting the protocol configuration
- **Realism**: Matches how network engineers think about and configure IGP protocols

### Consequences

- Additional complexity in data modeling
- More relationships to manage
- Better alignment with real-world network configurations
