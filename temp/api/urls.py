"""Django API urlpatterns declaration for igp_models app."""

from nautobot.apps.api import OrderedDefaultRouter

from igp_models.api import views

router = OrderedDefaultRouter()
# add the name of your api endpoint, usually hyphenated model name in plural, e.g. "my-model-classes"
router.register("igpprotocol", views.IGPProtocolViewSet)

app_name = "igp_models-api"
urlpatterns = router.urls
