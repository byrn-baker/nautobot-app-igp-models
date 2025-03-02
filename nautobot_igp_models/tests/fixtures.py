"""Create fixtures for tests."""

from nautobot_igp_models.models import IGPRoutingInstance


def create_igproutinginstance():
    """Fixture to create necessary number of IGPRoutingInstance for tests."""
    IGPRoutingInstance.objects.create(name="Test One")
    IGPRoutingInstance.objects.create(name="Test Two")
    IGPRoutingInstance.objects.create(name="Test Three")
