"""App declaration for igp_models."""

# Metadata is inherited from Nautobot. If not including Nautobot in the environment, this should be added
from importlib import metadata

from nautobot.apps import NautobotAppConfig

__version__ = metadata.version(__name__)


class IgpModelsConfig(NautobotAppConfig):
    """App configuration for the igp_models app."""

    name = "igp_models"
    verbose_name = "Igp Models"
    version = __version__
    author = "Byrn Baker"
    description = "Igp Models."
    base_url = "igp-models"
    required_settings = []
    min_version = "2.0.0"
    max_version = "2.9999"
    default_settings = {}
    caching_config = {}
    docs_view_name = "plugins:igp_models:docs"


config = IgpModelsConfig  # pylint:disable=invalid-name
