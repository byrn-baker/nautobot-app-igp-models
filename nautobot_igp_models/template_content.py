"""Template content injection for Nautobot IGP Models."""

from nautobot.extras.plugins import PluginTemplateExtension

from .models import IGPInstance


class DeviceIGPInstances(PluginTemplateExtension):  # pylint: disable=abstract-method
    """Add IGPInstance to the right side of the Device page."""

    model = "dcim.device"

    def right_page(self):
        """Add content to the right side of the Device detail view."""
        igp_routing_instances = IGPInstance.objects.filter(
            device=self.context["object"],
        )
        return self.render(
            "igp_models/inc/device_igp_routing_instances.html",
            extra_context={"igp_routing_instances": igp_routing_instances},
        )


template_extensions = [DeviceIGPInstances]
