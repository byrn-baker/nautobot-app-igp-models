"""API views for nautobot_igp_models."""

from nautobot.apps.api import NautobotModelViewSet

from nautobot_igp_models import filters, models
from nautobot_igp_models.api import serializers


class IGPInstanceViewSet(NautobotModelViewSet):  # pylint: disable=too-many-ancestors
    """IGPInstance viewset."""

    queryset = models.IGPInstance.objects.all()
    serializer_class = serializers.IGPInstanceSerializer
    filterset_class = filters.IGPInstanceFilterSet


class ISISConfigurationViewSet(NautobotModelViewSet):  # pylint: disable=too-many-ancestors
    """ISISConfiguration viewset."""

    queryset = models.ISISConfiguration.objects.all()
    serializer_class = serializers.ISISConfigurationSerializer
    filterset_class = filters.ISISConfigurationFilterSet


class OSPFConfigurationViewSet(NautobotModelViewSet):  # pylint: disable=too-many-ancestors
    """OSPFConfiguration viewset."""

    queryset = models.OSPFConfiguration.objects.all()
    serializer_class = serializers.OSPFConfigurationSerializer
    filterset_class = filters.OSPFConfigurationFilterSet
