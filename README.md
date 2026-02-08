# Nautobot IGP Models

<p align="center">
  <img src="https://raw.githubusercontent.com/byrn-baker/nautobot-app-igp-models/develop/docs/images/icon-nautobot-igp-models.png" class="logo" height="200px">
  <br>
  <a href="https://github.com/byrn-baker/nautobot-app-igp-models/actions"><img src="https://github.com/byrn-baker/nautobot-app-igp-models/actions/workflows/ci.yml/badge.svg?branch=main"></a>
  <a href="https://nautobot-igp-models.readthedocs.io/"><img src="https://readthedocs.org/projects/nautobot-igp-models/badge/"></a>
  <a href="https://pypi.org/project/nautobot-igp-models/"><img src="https://img.shields.io/pypi/v/nautobot-igp-models"></a>
  <a href="https://pypi.org/project/nautobot-igp-models/"><img src="https://img.shields.io/pypi/dm/nautobot-igp-models"></a>
  <br>
  An <a href="https://networktocode.com/nautobot-apps/">App</a> for <a href="https://nautobot.com/">Nautobot</a>.
</p>

## Overview

The Nautobot IGP Models app extends Nautobot to provide comprehensive modeling and management of Interior Gateway Protocol (IGP) routing configurations. This app enables network engineers and automation teams to maintain a source of truth for ISIS and OSPF routing instances, process configurations, and interface-level routing parameters across their network infrastructure.

With this app, you can model complete IGP topologies including routing instances per device, protocol-specific configurations (ISIS NET generation, OSPF process IDs), and granular interface settings (ISIS circuit types and metrics, OSPF areas and costs). The app provides full CRUD operations via both the Nautobot web UI and REST API, making it ideal for both manual network documentation and programmatic network automation workflows. Whether you're documenting existing IGP deployments, planning network migrations, or generating router configurations from structured data, the IGP Models app provides the data foundation you need.

The app integrates seamlessly with Nautobot's existing device and interface models, supports custom fields and relationships for extensibility, and includes comprehensive filtering and bulk editing capabilities. It also features intelligent defaults like automatic ISIS NET generation from router IDs and configurable status tracking for lifecycle management.

### Key Features

- **Multiple IGP Protocol Support**: Model both ISIS and OSPF configurations on the same or different devices
- **Hierarchical Configuration**: Organize routing configs from device-level instances down to interface-specific parameters
- **ISIS NET Auto-Generation**: Automatically generate valid ISIS Network Entity Titles (NETs) from router IDs and area identifiers
- **Comprehensive Interface Configuration**: Track circuit types, metrics, areas, and costs at the interface level
- **Full API Access**: Complete REST API for programmatic access and automation integration
- **Status Lifecycle Management**: Track configuration states (Planned, Active, Decommissioned)
- **Extensibility**: Leverage Nautobot's custom fields, relationships, and webhooks
- **Demo Data**: Includes management command to load realistic network topology for testing

### Supported Use Cases

- Network documentation and source of truth for IGP routing configurations
- Configuration generation for network automation tools (Ansible, Nornir, etc.)
- Migration planning between routing protocols (ISIS to OSPF, vice versa)
- Validation of routing design consistency across the network
- Integration with monitoring systems for configuration drift detection

More details can be found in the [Using the App](https://docs.nautobot.com/projects/nautobot-igp-models/en/latest/user/app_use_cases/) documentation.

## Try it out!

This app can be tested in your local development environment using the included demo data:

```bash
# Start development environment
invoke build && invoke start

# Load demo data
invoke nbshell
# In the shell:
from nautobot_igp_models.management.commands.load_igp_demo_data import Command
Command().handle()
exit()

# Access Nautobot at http://localhost:8080
# Navigate to: Routing → IGP - Link-State
```

The demo data creates a realistic 4-router network topology with ISIS and OSPF configurations for exploration and testing.

## Documentation

Full documentation for this App can be found over on the [Nautobot Docs](https://docs.nautobot.com) website:

- [User Guide](https://docs.nautobot.com/projects/nautobot-igp-models/en/latest/user/app_overview/) - Overview, Using the App, Getting Started.
- [Administrator Guide](https://docs.nautobot.com/projects/nautobot-igp-models/en/latest/admin/install/) - How to Install, Configure, Upgrade, or Uninstall the App.
- [Developer Guide](https://docs.nautobot.com/projects/nautobot-igp-models/en/latest/dev/contributing/) - Extending the App, Code Reference, Contribution Guide.
- [Release Notes / Changelog](https://docs.nautobot.com/projects/nautobot-igp-models/en/latest/admin/release_notes/).
- [Frequently Asked Questions](https://docs.nautobot.com/projects/nautobot-igp-models/en/latest/user/faq/).

### Contributing to the Documentation

You can find all the Markdown source for the App documentation under the [`docs`](https://github.com/byrn-baker/nautobot-app-igp-models/tree/develop/docs) folder in this repository. For simple edits, a Markdown capable editor is sufficient: clone the repository and edit away.

If you need to view the fully-generated documentation site, you can build it with [MkDocs](https://www.mkdocs.org/). A container hosting the documentation can be started using the `invoke` commands (details in the [Development Environment Guide](https://docs.nautobot.com/projects/nautobot-igp-models/en/latest/dev/dev_environment/#docker-development-environment)) on [http://localhost:8001](http://localhost:8001). Using this container, as your changes to the documentation are saved, they will be automatically rebuilt and any pages currently being viewed will be reloaded in your browser.

Any PRs with fixes or improvements are very welcome!

## Questions

For any questions or comments, please check the [FAQ](https://docs.nautobot.com/projects/nautobot-igp-models/en/latest/user/faq/) first. Feel free to also swing by the [Network to Code Slack](https://networktocode.slack.com/) (channel `#nautobot`), sign up [here](http://slack.networktocode.com/) if you don't have an account.
