"""Django API urlpatterns declaration for nautobot_igp_models app."""

from nautobot.apps.api import OrderedDefaultRouter

from nautobot_igp_models.api import views

router = OrderedDefaultRouter()
# add the name of your api endpoint, usually hyphenated model name in plural, e.g. "my-model-classes"
router.register("igp-routing-instances", views.IGPRoutingInstanceViewSet)
router.register("isis-configurations", views.ISISConfigurationViewSet)
router.register("isis-interface-configurations", views.ISISInterfaceConfigurationViewSet)
router.register("ospf-configurations", views.OSPFConfigurationViewSet)
router.register("ospf-interface-configurations", views.OSPFInterfaceConfigurationViewSet)

app_name = "nautobot_igp_models-api"
urlpatterns = router.urls
