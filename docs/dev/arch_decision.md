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

## Hybrid Configuration Approach

### Decision

The app uses a hybrid approach for managing configuration parameters, combining database fields for core protocol settings with Nautobot's config context for optional/vendor-specific parameters.

### Rationale

- **Type Safety**: Core protocol parameters (metric, cost, circuit type, area) are database fields with validation
- **Flexibility**: Optional parameters (hello timers, authentication, vendor features) use config context
- **Inheritance**: Protocol configurations provide default values that interfaces can inherit or override
- **Queryability**: Database fields can be filtered and searched efficiently
- **Extensibility**: Config context allows adding vendor-specific features without migrations
- **Best of Both Worlds**: Combines structured data (database) with flexible configuration (JSON)

### Configuration Inheritance Chain

Priority order (highest to lowest):
1. Interface-specific database fields (explicit overrides)
2. Protocol configuration defaults (database)
3. Device/Interface config context (flexible settings)
4. Global protocol defaults (fallback values)

### Implementation

**Database Fields for Core Parameters:**
- ISIS: default_metric, default_hello_interval, default_hello_multiplier, default_priority
- OSPF: default_cost, default_hello_interval, default_dead_interval, default_priority

**Config Context for Optional Parameters:**
- Authentication settings
- Vendor-specific features (BFD, MPLS TE, fast-reroute)
- Environment-specific defaults
- Settings referencing secrets

**Helper Methods:**
- `get_effective_metric()` / `get_effective_cost()`: Returns inherited or explicit value
- `get_effective_config()`: Returns complete merged configuration
- `get_vendor_config()`: Returns vendor-specific settings from config context

### Consequences

**Advantages:**
- Core protocol settings are type-safe and validated
- Optional settings don't require migrations
- Easy to query/filter on database fields
- Vendor-specific features can be added dynamically
- Configuration generation can use both sources

**Trade-offs:**
- Two sources of truth require coordination
- Config context values aren't validated at database level
- Developers must understand both systems
- More complex configuration retrieval logic

**Mitigation:**
- Clear documentation on when to use each approach
- Helper methods encapsulate complexity
- Validation can be added at form/serializer level for config context
