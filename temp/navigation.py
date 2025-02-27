"""Menu items."""

from nautobot.apps.ui import NavMenuAddButton, NavMenuGroup, NavMenuItem, NavMenuTab

items = (
    NavMenuItem(
        link="plugins:igp_models:igpprotocol_list",
        name="Igp Models",
        permissions=["igp_models.view_igpprotocol"],
        buttons=(
            NavMenuAddButton(
                link="plugins:igp_models:igpprotocol_add",
                permissions=["igp_models.add_igpprotocol"],
            ),
        ),
    ),
)

menu_items = (
    NavMenuTab(
        name="Apps",
        groups=(NavMenuGroup(name="Igp Models", items=tuple(items)),),
    ),
)
