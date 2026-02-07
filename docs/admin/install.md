# Installing the App in Nautobot

Here you will find detailed instructions on how to **install** and **configure** the App within your Nautobot environment.

## Prerequisites

- The app is compatible with Nautobot 3.0.0 and higher.
- Python version: 3.10, 3.11, 3.12, or 3.13
- Databases supported: PostgreSQL, MySQL

!!! note
    Please check the [dedicated page](compatibility_matrix.md) for a full compatibility matrix and the deprecation policy.

### Access Requirements

This app does not require access to any external systems. All functionality operates within the Nautobot environment using the existing device and interface models.

## Install Guide

!!! note
    Apps can be installed from the [Python Package Index](https://pypi.org/) or locally. See the [Nautobot documentation](https://docs.nautobot.com/projects/core/en/stable/user-guide/administration/installation/app-install/) for more details. The pip package name for this app is [`nautobot-igp-models`](https://pypi.org/project/nautobot-igp-models/).

The app is available as a Python package via PyPI and can be installed with `pip`:

```shell
pip install nautobot-igp-models
```

To ensure Nautobot IGP Models is automatically re-installed during future upgrades, create a file named `local_requirements.txt` (if not already existing) in the Nautobot root directory (alongside `requirements.txt`) and list the `nautobot-igp-models` package:

```shell
echo nautobot-igp-models >> local_requirements.txt
```

Once installed, the app needs to be enabled in your Nautobot configuration. The following block of code below shows the additional configuration required to be added to your `nautobot_config.py` file:

- Append `"nautobot_igp_models"` to the `PLUGINS` list.
- Append the `"nautobot_igp_models"` dictionary to the `PLUGINS_CONFIG` dictionary and override any defaults.

```python
# In your nautobot_config.py
PLUGINS = ["nautobot_igp_models"]

# PLUGINS_CONFIG = {
#   "nautobot_igp_models": {
#     ADD YOUR SETTINGS HERE
#   }
# }
```

Once the Nautobot configuration is updated, run the Post Upgrade command (`nautobot-server post_upgrade`) to run migrations and clear any cache:

```shell
nautobot-server post_upgrade
```

Then restart (if necessary) the Nautobot services which may include:

- Nautobot
- Nautobot Workers
- Nautobot Scheduler

```shell
sudo systemctl restart nautobot nautobot-worker nautobot-scheduler
```

## App Configuration

The app includes sensible defaults and does not require additional configuration to function. However, you can optionally configure the default statuses for the models.

### Optional Configuration

The app automatically creates default statuses for all models during migration. If you want to customize the statuses, you can add the following to your `PLUGINS_CONFIG`:

```python
PLUGINS_CONFIG = {
    "nautobot_igp_models": {
        "default_statuses": {
            "IGPRoutingInstance": ["Planned", "Active", "Decommissioned"],
            "ISISConfiguration": ["Active", "Decommissioned", "Deprovisioning", "Offline", "Planned", "Provisioning"],
            "ISISInterfaceConfiguration": ["Active", "Decommissioned", "Deprovisioning", "Offline", "Planned", "Provisioning"],
            "OSPFConfiguration": ["Active", "Decommissioned", "Deprovisioning", "Offline", "Planned", "Provisioning"],
            "OSPFInterfaceConfiguration": ["Active", "Decommissioned", "Deprovisioning", "Offline", "Planned", "Provisioning"],
        }
    }
}
```

!!! note
    If the statuses don't already exist in your Nautobot instance, they will be created automatically during migration.
