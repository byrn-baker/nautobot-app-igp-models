"""API views for nautobot_igp_models."""

from nautobot.apps.api import NautobotModelViewSet

from nautobot_igp_models import filters, models
from nautobot_igp_models.api import serializers


class IGPRoutingInstanceViewSet(NautobotModelViewSet):  # pylint: disable=too-many-ancestors
    """IGPRoutingInstance viewset."""

    queryset = models.IGPRoutingInstance.objects.all()
    serializer_class = serializers.IGPRoutingInstanceSerializer
    filterset_class = filters.IGPRoutingInstanceFilterSet


class ISISConfigurationViewSet(NautobotModelViewSet):  # pylint: disable=too-many-ancestors
    """ISISConfiguration viewset."""

    queryset = models.ISISConfiguration.objects.all()
    serializer_class = serializers.ISISConfigurationSerializer
    filterset_class = filters.ISISConfigurationFilterSet


class ISISInterfaceConfigurationViewSet(NautobotModelViewSet):  # pylint: disable=too-many-ancestors
    """ISIS Interface Configuration viewset."""

    queryset = models.ISISInterfaceConfiguration.objects.all()
    serializer_class = serializers.ISISInterfaceConfigurationSerializer
    filterset_class = filters.ISISInterfaceConfigurationFilterSet


class OSPFConfigurationViewSet(NautobotModelViewSet):  # pylint: disable=too-many-ancestors
    """OSPFConfiguration viewset."""

    queryset = models.OSPFConfiguration.objects.all()
    serializer_class = serializers.OSPFConfigurationSerializer
    filterset_class = filters.OSPFConfigurationFilterSet


class OSPFInterfaceConfigurationViewSet(NautobotModelViewSet):  # pylint: disable=too-many-ancestors
    """OSPF Interface Configuration viewset."""

    queryset = models.OSPFInterfaceConfiguration.objects.all()
    serializer_class = serializers.OSPFInterfaceConfigurationSerializer
    filterset_class = filters.OSPFInterfaceConfigurationFilterSet
