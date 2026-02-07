# Uninstall the App from Nautobot

Here you will find any steps necessary to cleanly remove the App from your Nautobot environment.

## Database Cleanup

Prior to removing the app from the `nautobot_config.py`, run the following command to roll back any migration specific to this app.

```shell
nautobot-server migrate nautobot_igp_models zero
```

This will remove all database tables, indexes, and constraints created by the IGP Models app. Note that this action will permanently delete all IGP routing instance data, ISIS configurations, OSPF configurations, and related interface configurations stored in the database.

## Remove App configuration

Remove the configuration you added in `nautobot_config.py` from `PLUGINS` & `PLUGINS_CONFIG`.

Remove or comment out these lines:

```python
PLUGINS = [
    "nautobot_igp_models",  # Remove this line
]

PLUGINS_CONFIG = {
    # "nautobot_igp_models": {  # Remove this section
    #     # Add any plugin-specific configuration here
    # }
}
```

## Uninstall the package

```bash
$ pip3 uninstall nautobot-igp-models
```

After uninstalling, restart the Nautobot services:

```bash
sudo systemctl restart nautobot nautobot-worker nautobot-scheduler
```
