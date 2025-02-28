"""API serializers for nautobot_igp_models."""

from nautobot.apps.api import NautobotModelSerializer, TaggedModelSerializerMixin

from nautobot_igp_models import models


class IGPInstanceSerializer(NautobotModelSerializer, TaggedModelSerializerMixin):  # pylint: disable=too-many-ancestors
    """IGPInstance Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.IGPInstance
        fields = "__all__"


class ISISConfigurationSerializer(NautobotModelSerializer, TaggedModelSerializerMixin):  # pylint: disable=too-many-ancestors
    """ISISConfiguration Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.ISISConfiguration
        fields = "__all__"

class ISISInterfaceConfigurationSerializer(NautobotModelSerializer, TaggedModelSerializerMixin):  # pylint: disable=too-many-ancestors
    """ISISInterfaceConfiguration Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.ISISInterfaceConfiguration
        fields = "__all__"


class OSPFConfigurationSerializer(NautobotModelSerializer, TaggedModelSerializerMixin):  # pylint: disable=too-many-ancestors
    """OSPFConfiguration Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.OSPFConfiguration
        fields = "__all__"

class OSPFInterfaceConfigurationSerializer(NautobotModelSerializer, TaggedModelSerializerMixin):  # pylint: disable=too-many-ancestors
    """OSPFInterfaceConfiguration Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.OSPFInterfaceConfiguration
        fields = "__all__"