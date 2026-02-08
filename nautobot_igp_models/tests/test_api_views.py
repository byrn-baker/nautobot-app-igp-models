"""Unit tests for API views."""

from nautobot.apps.testing import APIViewTestCases

from nautobot_igp_models import models
from nautobot_igp_models.tests import fixtures


class IGPRoutingInstanceAPIViewTest(APIViewTestCases.APIViewTestCase):
    # pylint: disable=too-many-ancestors
    """Test the API viewsets for IGPRoutingInstance."""

    model = models.IGPRoutingInstance

    @classmethod
    def setUpTestData(cls):
        """Create test data for IGPRoutingInstance API views."""
        all_fixtures = fixtures.create_all_fixtures()
        cls.statuses = all_fixtures["statuses"]
        cls.devices = all_fixtures["devices"]
        cls.ip_addresses = all_fixtures["ip_addresses"]
        cls.vrfs = all_fixtures["vrfs"]

    @property
    def create_data(self):
        """Return data for creating IGPRoutingInstance via API."""
        # Use management VRF to avoid conflicts with fixtures that use global VRF
        return [
            {
                "name": "API-Test-IGP-1",
                "description": "API test IGP instance 1",
                "device": str(self.devices["router1"].pk),
                "protocol": "ISIS",
                "router_id": str(self.ip_addresses["router1"].pk),
                "vrf": str(self.vrfs["management"].pk),
                "isis_area": "49.0001",
                "status": str(self.statuses["active"].pk),
            },
            {
                "name": "API-Test-IGP-2",
                "description": "API test IGP instance 2",
                "device": str(self.devices["router2"].pk),
                "protocol": "OSPF",
                "router_id": str(self.ip_addresses["router2"].pk),
                "vrf": str(self.vrfs["management"].pk),
                "status": str(self.statuses["active"].pk),
            },
            {
                "name": "API-Test-IGP-3",
                "description": "API test IGP instance 3",
                "device": str(self.devices["router3"].pk),
                "protocol": "ISIS",
                "router_id": str(self.ip_addresses["router3"].pk),
                "vrf": str(self.vrfs["management"].pk),
                "isis_area": "49.0002",
                "status": str(self.statuses["active"].pk),
            },
        ]

    @property
    def bulk_update_data(self):
        """Return data for bulk update testing."""
        return {"description": "Bulk updated via API"}


class ISISConfigurationAPIViewTest(APIViewTestCases.APIViewTestCase):
    # pylint: disable=too-many-ancestors
    """Test the API viewsets for ISISConfiguration."""

    model = models.ISISConfiguration

    @classmethod
    def setUpTestData(cls):
        """Create test data for ISISConfiguration API views."""
        all_fixtures = fixtures.create_all_fixtures()
        cls.statuses = all_fixtures["statuses"]
        cls.igp_instances = all_fixtures["igp_instances"]

    @property
    def create_data(self):
        """Return data for creating ISISConfiguration via API."""
        # Note: These will fail due to unique constraint conflicts with fixtures
        # TODO: Need to refactor to create new IGP instances without configs
        return [
            {
                "name": "API-ISIS-Config-1",
                "instance": str(self.igp_instances["isis_router1"].pk),
                "system_id": "49.0001.1111.2222.3333.00",
                "status": str(self.statuses["active"].pk),
            },
            {
                "name": "API-ISIS-Config-2",
                "instance": str(self.igp_instances["isis_router2"].pk),
                "status": str(self.statuses["active"].pk),
                # system_id will be auto-generated
            },
            {
                "name": "API-ISIS-Config-3",
                "instance": str(self.igp_instances["isis_router3"].pk),
                "system_id": "49.0001.4444.5555.6666.00",
                "status": str(self.statuses["planned"].pk),
            },
        ]

    @property
    def bulk_update_data(self):
        """Return data for bulk update testing."""
        return {}  # ISIS config doesn't have many bulk-updateable fields


class ISISInterfaceConfigurationAPIViewTest(APIViewTestCases.APIViewTestCase):
    # pylint: disable=too-many-ancestors
    """Test the API viewsets for ISISInterfaceConfiguration."""

    model = models.ISISInterfaceConfiguration

    @classmethod
    def setUpTestData(cls):
        """Create test data for ISISInterfaceConfiguration API views."""
        all_fixtures = fixtures.create_all_fixtures()
        cls.statuses = all_fixtures["statuses"]
        cls.isis_configurations = all_fixtures["isis_configurations"]
        cls.devices = all_fixtures["devices"]
        cls.interfaces = all_fixtures["interfaces"]

    @property
    def create_data(self):
        """Return data for creating ISISInterfaceConfiguration via API."""
        # Using ge2 and loopback0 to avoid conflicts with fixtures that use ge1
        return [
            {
                "name": "API-ISIS-Int-1",
                "isis_config": str(self.isis_configurations["router1"].pk),
                "device": str(self.devices["router1"].pk),
                "interface": str(self.interfaces["router1"]["loopback0"].pk),
                "circuit_type": "L2",
                "metric": 10,
                "status": str(self.statuses["active"].pk),
            },
            {
                "name": "API-ISIS-Int-2",
                "isis_config": str(self.isis_configurations["router2"].pk),
                "device": str(self.devices["router2"].pk),
                "interface": str(self.interfaces["router2"]["loopback0"].pk),
                "circuit_type": "L1L2",
                "metric": 20,
                "status": str(self.statuses["active"].pk),
            },
            {
                "name": "API-ISIS-Int-3",
                "isis_config": str(self.isis_configurations["router3"].pk),
                "device": str(self.devices["router3"].pk),
                "interface": str(self.interfaces["router3"]["ge2"].pk),
                "circuit_type": "L1",
                "metric": 30,
                "status": str(self.statuses["planned"].pk),
            },
        ]

    @property
    def bulk_update_data(self):
        """Return data for bulk update testing."""
        return {"metric": 100}


class OSPFConfigurationAPIViewTest(APIViewTestCases.APIViewTestCase):
    # pylint: disable=too-many-ancestors
    """Test the API viewsets for OSPFConfiguration."""

    model = models.OSPFConfiguration

    @classmethod
    def setUpTestData(cls):
        """Create test data for OSPFConfiguration API views."""
        all_fixtures = fixtures.create_all_fixtures()
        cls.statuses = all_fixtures["statuses"]
        cls.igp_instances = all_fixtures["igp_instances"]

    @property
    def create_data(self):
        """Return data for creating OSPFConfiguration via API."""
        return [
            {
                "name": "API-OSPF-Config-1",
                "instance": str(self.igp_instances["ospf_router1"].pk),
                "process_id": 100,
                "status": str(self.statuses["active"].pk),
            },
            {
                "name": "API-OSPF-Config-2",
                "instance": str(self.igp_instances["ospf_router2"].pk),
                "process_id": 200,
                "status": str(self.statuses["planned"].pk),
            },
            {
                "name": "API-OSPF-Config-3",
                "instance": str(self.igp_instances["ospf_router1"].pk),
                "process_id": 300,
                "status": str(self.statuses["active"].pk),
            },
        ]

    @property
    def bulk_update_data(self):
        """Return data for bulk update testing."""
        return {}  # OSPF config doesn't have many bulk-updateable fields


class OSPFInterfaceConfigurationAPIViewTest(APIViewTestCases.APIViewTestCase):
    # pylint: disable=too-many-ancestors
    """Test the API viewsets for OSPFInterfaceConfiguration."""

    model = models.OSPFInterfaceConfiguration

    @classmethod
    def setUpTestData(cls):
        """Create test data for OSPFInterfaceConfiguration API views."""
        all_fixtures = fixtures.create_all_fixtures()
        cls.statuses = all_fixtures["statuses"]
        cls.ospf_configurations = all_fixtures["ospf_configurations"]
        cls.interfaces = all_fixtures["interfaces"]

    @property
    def create_data(self):
        """Return data for creating OSPFInterfaceConfiguration via API."""
        return [
            {
                "name": "API-OSPF-Int-1",
                "ospf_config": str(self.ospf_configurations["router1"].pk),
                "interface": str(self.interfaces["router1"]["loopback0"].pk),
                "area": "0.0.0.0",
                "cost": 10,
                "status": str(self.statuses["active"].pk),
            },
            {
                "name": "API-OSPF-Int-2",
                "ospf_config": str(self.ospf_configurations["router2"].pk),
                "interface": str(self.interfaces["router2"]["loopback0"].pk),
                "area": "0.0.0.1",
                "cost": 20,
                "status": str(self.statuses["active"].pk),
            },
            {
                "name": "API-OSPF-Int-3",
                "ospf_config": str(self.ospf_configurations["router1"].pk),
                "interface": str(self.interfaces["router1"]["ge2"].pk),
                "area": "0.0.0.2",
                "cost": 30,
                "status": str(self.statuses["planned"].pk),
            },
        ]

    @property
    def bulk_update_data(self):
        """Return data for bulk update testing."""
        return {"cost": 50}
