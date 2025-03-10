"""Menu items."""

from nautobot.apps.ui import NavMenuAddButton, NavMenuGroup, NavMenuItem, NavMenuTab

menu_items = (
    NavMenuTab(
        name="Routing",
        weight=350,
        groups=(
            NavMenuGroup(
                name="IGP - Link-State",
                weight=150,
                items = (
                    NavMenuItem(
                        link="plugins:nautobot_igp_models:igproutinginstance_list",
                        name="Nautobot IGP Models",
                        permissions=["nautobot_igp_models.view_igproutinginstance"],
                        buttons=(
                            NavMenuAddButton(
                                link="plugins:nautobot_igp_models:igproutinginstance_add",
                                permissions=["nautobot_igp_models.add_igproutinginstance"],
                            ),
                        ),
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_igp_models:isisconfiguration_list",
                        name="ISIS Configuration",
                        permissions=["nautobot_igp_models.view_isisconfiguration"],
                        buttons=(
                            NavMenuAddButton(
                                link="plugins:nautobot_igp_models:isisconfiguration_add",
                                permissions=["nautobot_igp_models.add_isisconfiguration"],
                            ),
                        ),
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_igp_models:isisinterfaceconfiguration_list",
                        name="ISIS Interface Configuration",
                        permissions=["nautobot_igp_models.view_isisinterfaceconfiguration"],
                        buttons=(
                            NavMenuAddButton(
                                link="plugins:nautobot_igp_models:isisinterfaceconfiguration_add",
                                permissions=["nautobot_igp_models.add_isisinterfaceconfiguration"],
                            ),
                        ),
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_igp_models:ospfconfiguration_list",
                        name="OSPF Configuration",
                        permissions=["nautobot_igp_models.view_ospfconfiguration"],
                        buttons=(
                            NavMenuAddButton(
                                link="plugins:nautobot_igp_models:ospfconfiguration_add",
                                permissions=["nautobot_igp_models.add_ospfconfiguration"],
                            ),
                        ),
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_igp_models:ospfinterfaceconfiguration_list",
                        name="OSPF Interface Configuration",
                        permissions=["nautobot_igp_models.view_ospfinterfaceconfiguration"],
                        buttons=(
                            NavMenuAddButton(
                                link="plugins:nautobot_igp_models:ospfinterfaceconfiguration_add",
                                permissions=["nautobot_igp_models.add_ospfinterfaceconfiguration"],
                            ),
                        ),
                    ),
                )
            ),
        ),
    ),
)