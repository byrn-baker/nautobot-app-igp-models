"""Django urlpatterns declaration for igp_models app."""

from django.templatetags.static import static
from django.urls import path
from django.views.generic import RedirectView
from nautobot.apps.urls import NautobotUIViewSetRouter

from igp_models import views

app_name = "igp_models"
router = NautobotUIViewSetRouter()

router.register("igpprotocol", views.IGPProtocolUIViewSet)


urlpatterns = [
    path("docs/", RedirectView.as_view(url=static("igp_models/docs/index.html")), name="docs"),
]

urlpatterns += router.urls
