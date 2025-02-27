"""API views for igp_models."""

from nautobot.apps.api import NautobotModelViewSet

from igp_models import filters, models
from igp_models.api import serializers


class IGPProtocolViewSet(NautobotModelViewSet):  # pylint: disable=too-many-ancestors
    """IGPProtocol viewset."""

    queryset = models.IGPProtocol.objects.all()
    serializer_class = serializers.IGPProtocolSerializer
    filterset_class = filters.IGPProtocolFilterSet

    # Option for modifying the default HTTP methods:
    # http_method_names = ["get", "post", "put", "patch", "delete", "head", "options", "trace"]
