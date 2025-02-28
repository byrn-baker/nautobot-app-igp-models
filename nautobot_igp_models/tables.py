"""Tables for the Nautobot IGP Models app."""

import django_tables2 as tables
from nautobot.apps.tables import BaseTable, ButtonsColumn, ColorColumn, ToggleColumn

from nautobot_igp_models import models


class IGPInstanceTable(BaseTable):
    """Table for displaying IGPInstance objects."""

    pk = ToggleColumn()
    device = tables.LinkColumn()
    protocol = tables.Column()
    router_id = tables.LinkColumn()
    vrf = tables.LinkColumn()
    isis_area = tables.Column(verbose_name="ISIS Area", empty_values=())
    status = ColorColumn()
    actions = ButtonsColumn(
        model=models.IGPInstance,
        buttons=("edit", "delete"),
    )

    class Meta(BaseTable.Meta):
        model = models.IGPInstance
        fields = ("pk", "device", "protocol", "router_id", "vrf", "isis_area", "status", "actions")
        default_columns = ("pk", "device", "protocol", "router_id", "vrf", "isis_area", "status", "actions")


class ISISConfigurationTable(BaseTable):
    """Table for displaying ISISConfiguration objects."""

    pk = ToggleColumn()
    instance = tables.LinkColumn()
    system_id = tables.Column(verbose_name="System ID")
    status = ColorColumn()
    actions = ButtonsColumn(
        model=models.ISISConfiguration,
        buttons=("edit", "delete"),
    )

    class Meta(BaseTable.Meta):
        model = models.ISISConfiguration
        fields = ("pk", "instance", "system_id", "status", "actions")
        default_columns = ("pk", "instance", "system_id", "status", "actions")

class ISISInterfaceConfigurationTable(BaseTable):
    """Table for displaying ISISInterfaceConfiguration objects."""
    pk = ToggleColumn()
    isis_config = tables.LinkColumn()
    interface = tables.LinkColumn()
    circuit_type = tables.Column()
    metric = tables.Column()
    status = ColorColumn()
    actions = ButtonsColumn(
        model=models.ISISInterfaceConfiguration,
        buttons=("edit", "delete"),
    )
    
    class Meta(BaseTable.Meta):
        model = models.ISISInterfaceConfiguration
        fields = ("pk", "isis_config", "interface", "circuit_type", "metric", "status", "actions")
        default_columns = ("pk", "isis_config", "interface", "circuit_type", "metric", "status", "actions")
    
class OSPFConfigurationTable(BaseTable):
    """Table for displaying OSPFConfiguration objects."""

    pk = ToggleColumn()
    instance = tables.LinkColumn()
    area = tables.Column(verbose_name="OSPF Area")
    process_id = tables.Column(verbose_name="Process ID")
    status = ColorColumn()
    actions = ButtonsColumn(
        model=models.OSPFConfiguration,
        buttons=("edit", "delete"),
    )

    class Meta(BaseTable.Meta):
        model = models.OSPFConfiguration
        fields = ("pk", "instance", "area", "process_id", "status", "actions")
        default_columns = ("pk", "instance", "area", "process_id", "status", "actions")

class OSPFInterfaceConfigurationTable(BaseTable):
    """Table for displaying OSPFInterfaceConfiguration objects."""
    pk = ToggleColumn()
    ospf_config = tables.LinkColumn()
    interface = tables.LinkColumn()
    area = tables.Column()
    cost = tables.Column()
    hello_interval = tables.Column()
    dead_interval = tables.Column()
    status = ColorColumn()
    actions = ButtonsColumn(
        model=models.OSPFInterfaceConfiguration,
        buttons=("edit", "delete"),
    )
    
    class Meta(BaseTable.Meta):
        model = models.OSPFInterfaceConfiguration
        fields = ("pk", "ospf_config", "interface", "area", "cost", "hello_interval", "dead_interval", "status", "actions")
        default_columns = ("pk", "ospf_config", "interface", "area", "cost", "hello_interval", "dead_interval", "status", "actions")