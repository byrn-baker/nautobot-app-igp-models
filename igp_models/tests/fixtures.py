"""Create fixtures for tests."""

from igp_models.models import IGPProtocol


def create_igpprotocol():
    """Fixture to create necessary number of IGPProtocol for tests."""
    IGPProtocol.objects.create(name="Test One")
    IGPProtocol.objects.create(name="Test Two")
    IGPProtocol.objects.create(name="Test Three")
