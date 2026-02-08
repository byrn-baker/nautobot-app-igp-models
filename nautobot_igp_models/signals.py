"""Nautobot signal handler functions for nautobot_igp_models."""

import logging
import os

from django.apps import apps as global_apps
from django.conf import settings
from django.core.management import call_command

logger = logging.getLogger(__name__)

PLUGIN_SETTINGS = settings.PLUGINS_CONFIG["nautobot_igp_models"]


def post_migrate_create_statuses(sender, *, apps=global_apps, **kwargs):
    """Callback function for post_migrate() -- create default Statuses."""
    # pylint: disable=invalid-name
    if not apps:
        return

    Status = apps.get_model("extras", "Status")

    for model_name, default_statuses in PLUGIN_SETTINGS.get("default_statuses", {}).items():
        model = sender.get_model(model_name)

        ContentType = apps.get_model("contenttypes", "ContentType")
        ct_model = ContentType.objects.get_for_model(model)
        for name in default_statuses:
            try:
                status = Status.objects.get(name=name)
            except Status.DoesNotExist:
                logger.warning(f"Unable to find status: {name}, skipping")
                continue

            if ct_model not in status.content_types.all():
                status.content_types.add(ct_model)
                status.save()


def post_migrate_load_resources(sender, *, apps=global_apps, **kwargs):
    """Callback function for post_migrate() -- load config context schemas and export templates."""
    # Only run if we're not in a migration (avoid issues during initial migrate)
    if os.environ.get("NAUTOBOT_SKIP_RESOURCE_LOADING"):
        logger.info("Skipping IGP resource loading (NAUTOBOT_SKIP_RESOURCE_LOADING is set)")
        return

    try:
        logger.info("Loading IGP config context schemas and export templates...")
        call_command("load_igp_resources", verbosity=0)
        logger.info("✓ IGP resources loaded successfully")
    except Exception as e:
        logger.warning(f"Unable to load IGP resources: {e}")
        # Don't fail the migration if resource loading fails
        pass
