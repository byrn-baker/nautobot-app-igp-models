from django.templatetags.static import static
from django.urls import path
from django.views.generic import RedirectView
from nautobot.core.views.routers import NautobotUIViewSetRouter

from . import views

router = NautobotUIViewSetRouter()
router.register("igp-instances", views.IGPInstanceUIViewSet)
router.register("isis-configuration", views.ISISConfigurationUIViewSet)
router.register("isis-interface-configuration", views.ISISInterfaceConfigurationUIViewSet)
router.register("ospf-configuration", views.OSPFConfigurationUIViewSet)
router.register("ospf-interface-configuration", views.OSPFInterfaceConfigurationUIViewSet)

urlpatterns = [
    path("docs/", RedirectView.as_view(url=static("nautobot_bgp_models/docs/index.html")), name="docs"),
]
app_name = "nautobot_igp_models"
urlpatterns += router.urls
