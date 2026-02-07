"""Django urlpatterns declaration for nautobot_igp_models app."""

from django.templatetags.static import static
from django.urls import path
from django.views.generic import RedirectView
from nautobot.apps.urls import NautobotUIViewSetRouter

from nautobot_igp_models import views

app_name = "nautobot_igp_models"
router = NautobotUIViewSetRouter()

router.register("igproutinginstance", views.IGPRoutingInstanceUIViewSet)
router.register("isis-configuration", views.ISISConfigurationUIViewSet)
router.register("isis-interface-configuration", views.ISISInterfaceConfigurationUIViewSet)
router.register("ospf-configuration", views.OSPFConfigurationUIViewSet)
router.register("ospf-interface-configuration", views.OSPFInterfaceConfigurationUIViewSet)

urlpatterns = [
    path("docs/", RedirectView.as_view(url=static("nautobot_igp_models/docs/index.html")), name="docs"),
]

urlpatterns += router.urls
