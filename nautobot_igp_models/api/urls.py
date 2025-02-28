"""Django API urlpatterns declaration for nautobot_igp_models app."""

from nautobot.apps.api import OrderedDefaultRouter

from nautobot_igp_models.api import views

router = OrderedDefaultRouter()

router.register("igpinstance", views.IGPInstanceViewSet)
router.register("isisconfiguration", views.ISISConfigurationViewSet)
router.register("ospfconfiguration", views.OSPFConfigurationViewSet)

app_name = "igp_models-api"
urlpatterns = router.urls
