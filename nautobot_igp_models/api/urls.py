"""Django API urlpatterns declaration for nautobot_igp_models app."""

from nautobot.apps.api import OrderedDefaultRouter

from nautobot_igp_models.api import views

router = OrderedDefaultRouter()
# add the name of your api endpoint, usually hyphenated model name in plural, e.g. "my-model-classes"
router.register("igproutinginstance", views.IGPRoutingInstanceViewSet)
router.register("isisconfiguration", views.ISISConfigurationViewSet)
router.register("isisinterfaceconfiguration", views.ISISInterfaceConfigurationViewSet)
router.register("ospfconfiguration", views.OSPFConfigurationViewSet)
router.register("ospfinterfaceconfiguration", views.OSPFInterfaceConfigurationViewSet)

app_name = "nautobot_igp_models-api"
urlpatterns = router.urls
