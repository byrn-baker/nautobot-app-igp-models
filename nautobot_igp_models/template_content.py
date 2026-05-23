"""Template content extensions for Device and Interface detail views."""

from nautobot.apps.ui import ObjectsTablePanel, Tab, TemplateExtension

from nautobot_igp_models.tables import (
    IGPRoutingInstanceTable,
    ISISInterfaceConfigurationTable,
    OSPFInterfaceConfigurationTable,
)


class DeviceIGPTab(TemplateExtension):
    """Add IGP Routing tab to Device detail view."""

    model = "dcim.device"

    object_detail_tabs = [
        Tab(
            tab_id="igp_routing",
            label="IGP Routing",
            panels=[
                ObjectsTablePanel(
                    table_class=IGPRoutingInstanceTable,
                    table_filter="device",
                    table_title="IGP Routing Instances",
                    related_field_name="device",
                    max_display_count=50,
                    weight=100,
                    section="full-width",
                ),
            ],
            weight=550,
        ),
    ]


class InterfaceIGPTab(TemplateExtension):
    """Add IGP tab to Interface detail view."""

    model = "dcim.interface"

    object_detail_tabs = [
        Tab(
            tab_id="igp_routing",
            label="IGP Routing",
            panels=[
                ObjectsTablePanel(
                    table_class=ISISInterfaceConfigurationTable,
                    table_filter="interface",
                    table_title="ISIS Interface Configurations",
                    related_field_name="interface",
                    max_display_count=50,
                    weight=100,
                    section="full-width",
                ),
                ObjectsTablePanel(
                    table_class=OSPFInterfaceConfigurationTable,
                    table_filter="interface",
                    table_title="OSPF Interface Configurations",
                    related_field_name="interface",
                    max_display_count=50,
                    weight=200,
                    section="full-width",
                ),
            ],
            weight=550,
        ),
    ]


template_extensions = [DeviceIGPTab, InterfaceIGPTab]
