"""App declaration for nautobot_igp_models."""

# Metadata is inherited from Nautobot. If not including Nautobot in the environment, this should be added
from importlib import metadata
from django.db.models.signals import post_migrate
from nautobot.apps import NautobotAppConfig

__version__ = metadata.version(__name__)


class NautobotIgpModelsConfig(NautobotAppConfig):
    """App configuration for the nautobot_igp_models app."""

    name = "nautobot_igp_models"
    verbose_name = "Nautobot IGP Models"
    version = __version__
    author = "Byrn Baker"
    description = "Nautobot IGP Models."
    base_url = "nautobot-igp-models"
    required_settings = []
    min_version = "2.0.0"
    max_version = "2.9999"
    default_settings = {
        "default_statuses": {
            "IGPRoutingInstance": ["Planned", "Active", "Decommissioned"],
            "ISISConfiguration": ["Active", "Decommissioned", "Deprovisioning", "Offline", "Planned", "Provisioning"],
            "ISISInterfaceConfiguration": ["Active", "Decommissioned", "Deprovisioning", "Offline", "Planned", "Provisioning"],
            "OSPFConfiguration": ["Active", "Decommissioned", "Deprovisioning", "Offline", "Planned", "Provisioning"],
            "OSPFInterfaceConfiguration": ["Active", "Decommissioned", "Deprovisioning", "Offline", "Planned", "Provisioning"],
        }
    }
    caching_config = {}
    docs_view_name = "plugins:nautobot_igp_models:docs"
    
    def ready(self):
        """Callback invoked after the app is loaded."""
        super().ready()

        from .signals import (  # pylint: disable=import-outside-toplevel
            post_migrate_create_statuses,
        )

        post_migrate.connect(post_migrate_create_statuses, sender=self)


config = NautobotIgpModelsConfig  # pylint:disable=invalid-name
