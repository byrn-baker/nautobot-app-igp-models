# Upgrading the App

Here you will find any steps necessary to upgrade the App in your Nautobot environment.

## Upgrade Guide

When a new release comes out it may be necessary to run a migration of the database to account for any changes in the data models used by this app. Execute the command `nautobot-server post-upgrade` within the runtime environment of your Nautobot installation after updating the `nautobot-igp-models` package via `pip`.

### Standard Upgrade Process

1. Update the package:

```bash
pip3 install --upgrade nautobot-igp-models
```

2. Run database migrations:

```bash
nautobot-server post-upgrade
```

This command will automatically:
- Run any pending database migrations
- Clear stale content types
- Rebuild the search index
- Collect static files

3. Restart Nautobot services:

```bash
sudo systemctl restart nautobot nautobot-worker nautobot-scheduler
```

### Version-Specific Upgrade Notes

#### Upgrading to v1.0.0

This is the initial release, so no special upgrade considerations are needed. Follow the standard installation procedure outlined in the [Installation Guide](install.md).

### Rollback Procedure

If you need to rollback to a previous version:

1. Install the previous version:

```bash
pip3 install nautobot-igp-models==<previous-version>
```

2. Rollback database migrations if needed:

```bash
nautobot-server migrate nautobot_igp_models <previous-migration-number>
```

3. Restart services:

```bash
sudo systemctl restart nautobot nautobot-worker nautobot-scheduler
```
