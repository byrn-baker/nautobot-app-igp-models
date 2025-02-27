"""Filtering for igp_models."""

from nautobot.apps.filters import NameSearchFilterSet, NautobotFilterSet

from igp_models import models


class IGPProtocolFilterSet(NautobotFilterSet, NameSearchFilterSet):  # pylint: disable=too-many-ancestors

    class Meta:
        model = models.IGPProtocol
        fields = ["id", "name", "device", "enabled", "process_id"]

class IGPInterfaceFilterSet(NautobotFilterSet, NameSearchFilterSet):  # pylint: disable=too-many-ancestors

    class Meta:
        model = models.IGPProtocol
        fields = ["id", "name", "device", "enabled", "process_id"]