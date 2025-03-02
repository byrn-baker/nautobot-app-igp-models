"""Tables for nautobot_igp_models."""

import django_tables2 as tables
from nautobot.apps.tables import BaseTable, StatusTableMixin, ButtonsColumn, ToggleColumn

from nautobot_igp_models import models


class IGPRoutingInstanceTable(StatusTableMixin, BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    name = tables.Column(linkify=True)
    device = tables.LinkColumn()
    protocol = tables.Column()
    router_id = tables.LinkColumn()
    vrf = tables.LinkColumn()
    isis_area = tables.Column(verbose_name="ISIS Area", empty_values=())
    actions = ButtonsColumn(
        models.IGPRoutingInstance,
        buttons=("edit", "delete"),
        pk_field="pk",
    )

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.IGPRoutingInstance
        fields = (
            "pk",
            "name",
            "description",
            "device",
            "protocol",
            "router_id",
            "vrf",
            "isis_area",
            "status",
        )

class ISISConfigurationTable(StatusTableMixin, BaseTable):
    """Table for displaying ISISConfiguration objects."""

    pk = ToggleColumn()
    instance = tables.LinkColumn()
    system_id = tables.Column(verbose_name="System ID")
    actions = ButtonsColumn(
        model=models.ISISConfiguration,
        buttons=("edit", "delete"),
    )

    class Meta(BaseTable.Meta):
        model = models.ISISConfiguration
        fields = ("pk", "instance", "system_id", "status", "actions")
        default_columns = ("pk", "instance", "system_id", "status", "actions")

class ISISInterfaceConfigurationTable(StatusTableMixin, BaseTable):
    """Table for displaying ISISInterfaceConfiguration objects."""
    pk = ToggleColumn()
    isis_config = tables.LinkColumn()
    interface = tables.LinkColumn()
    circuit_type = tables.Column()
    metric = tables.Column()
    actions = ButtonsColumn(
        model=models.ISISInterfaceConfiguration,
        buttons=("edit", "delete"),
    )
    
    class Meta(BaseTable.Meta):
        model = models.ISISInterfaceConfiguration
        fields = ("pk", "isis_config", "interface", "circuit_type", "metric", "status", "actions")
        default_columns = ("pk", "isis_config", "interface", "circuit_type", "metric", "status", "actions")

class OSPFConfigurationTable(StatusTableMixin, BaseTable):
    """Table for displaying OSPFConfiguration objects."""

    pk = ToggleColumn()
    instance = tables.LinkColumn()
    area = tables.Column(verbose_name="OSPF Area")
    process_id = tables.Column(verbose_name="Process ID")
    actions = ButtonsColumn(
        model=models.OSPFConfiguration,
        buttons=("edit", "delete"),
    )

    class Meta(BaseTable.Meta):
        model = models.OSPFConfiguration
        fields = ("pk", "instance", "area", "process_id", "status", "actions")
        default_columns = ("pk", "instance", "area", "process_id", "status", "actions")

class OSPFInterfaceConfigurationTable(StatusTableMixin, BaseTable):
    """Table for displaying OSPFInterfaceConfiguration objects."""
    pk = ToggleColumn()
    ospf_config = tables.LinkColumn()
    interface = tables.LinkColumn()
    area = tables.Column()
    cost = tables.Column()
    hello_interval = tables.Column()
    dead_interval = tables.Column()
    actions = ButtonsColumn(
        model=models.OSPFInterfaceConfiguration,
        buttons=("edit", "delete"),
    )
    
    class Meta(BaseTable.Meta):
        model = models.OSPFInterfaceConfiguration
        fields = ("pk", "ospf_config", "interface", "area", "cost", "hello_interval", "dead_interval", "status", "actions")
        default_columns = ("pk", "ospf_config", "interface", "area", "cost", "hello_interval", "dead_interval", "status", "actions")