"""API serializers for igp_models."""

from nautobot.apps.api import NautobotModelSerializer, TaggedModelSerializerMixin

from igp_models import models


class IGPProtocolSerializer(NautobotModelSerializer, TaggedModelSerializerMixin):  # pylint: disable=too-many-ancestors
    """IGPProtocol Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.IGPProtocol
        fields = "__all__"

        # Option for disabling write for certain fields:
        # read_only_fields = []
