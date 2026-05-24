"""Unit tests for views."""

from nautobot.apps.testing import ViewTestCases

from nautobot_igp_models import models
from nautobot_igp_models.tests import fixtures


class IGPRoutingInstanceViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    # pylint: disable=too-many-ancestors
    """Test the IGPRoutingInstance views."""

    model = models.IGPRoutingInstance
    bulk_edit_data = {"description": "Bulk edited description"}
    allowed_number_of_tree_queries_per_view_type = {"retrieve": 1}

    @classmethod
    def setUpTestData(cls):
        """Create test data for IGPRoutingInstance views."""
        all_fixtures = fixtures.create_all_fixtures()
        cls.statuses = all_fixtures["statuses"]
        cls.devices = all_fixtures["devices"]
        cls.ip_addresses = all_fixtures["ip_addresses"]
        cls.vrfs = all_fixtures["vrfs"]

    def get_form_data(self):
        """Return form data for creating/editing IGPRoutingInstance."""
        return {
            "name": "View-Test-IGP-Instance",
            "description": "Test IGP instance from view",
            "device": self.devices["router3"].pk,
            "protocol": "ISIS",
            "router_id": self.ip_addresses["router3"].pk,
            "vrf": self.vrfs["management"].pk,
            "isis_area": "49.0099",
            "status": self.statuses["active"].pk,
            "object_note": "",
            "dynamic_groups": [],
        }

    def get_csv_data(self):
        """Return CSV data for bulk import testing."""
        return (
            "name,description,device,protocol,status",
            f"CSV-IGP-1,CSV Test 1,{self.devices['router1'].pk},ISIS,{self.statuses['active'].pk}",
            f"CSV-IGP-2,CSV Test 2,{self.devices['router2'].pk},OSPF,{self.statuses['active'].pk}",
            f"CSV-IGP-3,CSV Test 3,{self.devices['router3'].pk},OSPF,{self.statuses['active'].pk}",
        )

    def get_bulk_edit_data(self):
        """Return data for bulk edit testing."""
        return self.bulk_edit_data


class ISISConfigurationViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    # pylint: disable=too-many-ancestors
    """Test the ISISConfiguration views."""

    model = models.ISISConfiguration
    bulk_edit_data = {"default_metric": 99}
    allowed_number_of_tree_queries_per_view_type = {"retrieve": 1}

    @classmethod
    def setUpTestData(cls):
        """Create test data for ISISConfiguration views."""
        all_fixtures = fixtures.create_all_fixtures()
        cls.statuses = all_fixtures["statuses"]
        cls.igp_instances = all_fixtures["igp_instances"]

    def get_form_data(self):
        """Return form data for creating/editing ISISConfiguration."""
        return {
            "name": "View-Test-ISIS-Config",
            "instance": self.igp_instances["isis_router1"].pk,
            "system_id": "49.0001.1234.5678.9012.00",
            "status": self.statuses["active"].pk,
            "object_note": "",
        }

    def get_csv_data(self):
        """Return CSV data for bulk import testing."""
        return (
            "name,instance,status",
            f"CSV-ISIS-1,{self.igp_instances['isis_router1'].pk},{self.statuses['active'].pk}",
            f"CSV-ISIS-2,{self.igp_instances['isis_router2'].pk},{self.statuses['active'].pk}",
        )

    def get_bulk_edit_data(self):
        """Return data for bulk edit testing."""
        return self.bulk_edit_data


class ISISInterfaceConfigurationViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    # pylint: disable=too-many-ancestors
    """Test the ISISInterfaceConfiguration views."""

    model = models.ISISInterfaceConfiguration
    bulk_edit_data = {"metric": 50}
    allowed_number_of_tree_queries_per_view_type = {"retrieve": 1}

    @classmethod
    def setUpTestData(cls):
        """Create test data for ISISInterfaceConfiguration views."""
        all_fixtures = fixtures.create_all_fixtures()
        cls.statuses = all_fixtures["statuses"]
        cls.isis_configurations = all_fixtures["isis_configurations"]
        cls.devices = all_fixtures["devices"]
        cls.interfaces = all_fixtures["interfaces"]

    def get_form_data(self):
        """Return form data for creating/editing ISISInterfaceConfiguration."""
        return {
            "name": "View-Test-ISIS-Interface",
            "isis_config": self.isis_configurations["router1"].pk,
            "device": self.devices["router1"].pk,
            "interface": self.interfaces["router1"]["loopback0"].pk,
            "circuit_type": "L2",
            "metric": 10,
            "status": self.statuses["active"].pk,
            "object_note": "",
        }

    def get_csv_data(self):
        """Return CSV data for bulk import testing."""
        return (
            "name,isis_config,interface,circuit_type,metric,status",
            f"CSV-ISIS-Int-1,{self.isis_configurations['router1'].pk},{self.interfaces['router1']['loopback0'].pk},L2,10,{self.statuses['active'].pk}",
        )

    def get_bulk_edit_data(self):
        """Return data for bulk edit testing."""
        return self.bulk_edit_data


class OSPFConfigurationViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    # pylint: disable=too-many-ancestors
    """Test the OSPFConfiguration views."""

    model = models.OSPFConfiguration
    bulk_edit_data = {"process_id": 200}
    allowed_number_of_tree_queries_per_view_type = {"retrieve": 1}

    @classmethod
    def setUpTestData(cls):
        """Create test data for OSPFConfiguration views."""
        all_fixtures = fixtures.create_all_fixtures()
        cls.statuses = all_fixtures["statuses"]
        cls.igp_instances = all_fixtures["igp_instances"]

    def get_form_data(self):
        """Return form data for creating/editing OSPFConfiguration."""
        return {
            "name": "View-Test-OSPF-Config",
            "instance": self.igp_instances["ospf_router1"].pk,
            "process_id": 100,
            "status": self.statuses["active"].pk,
            "object_note": "",
        }

    def get_csv_data(self):
        """Return CSV data for bulk import testing."""
        return (
            "name,instance,process_id,status",
            f"CSV-OSPF-1,{self.igp_instances['ospf_router1'].pk},1,{self.statuses['active'].pk}",
            f"CSV-OSPF-2,{self.igp_instances['ospf_router2'].pk},1,{self.statuses['active'].pk}",
        )

    def get_bulk_edit_data(self):
        """Return data for bulk edit testing."""
        return self.bulk_edit_data


class OSPFInterfaceConfigurationViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    # pylint: disable=too-many-ancestors
    """Test the OSPFInterfaceConfiguration views."""

    model = models.OSPFInterfaceConfiguration
    bulk_edit_data = {"cost": 100}
    allowed_number_of_tree_queries_per_view_type = {"retrieve": 1}

    @classmethod
    def setUpTestData(cls):
        """Create test data for OSPFInterfaceConfiguration views."""
        all_fixtures = fixtures.create_all_fixtures()
        cls.statuses = all_fixtures["statuses"]
        cls.ospf_configurations = all_fixtures["ospf_configurations"]
        cls.interfaces = all_fixtures["interfaces"]

    def get_form_data(self):
        """Return form data for creating/editing OSPFInterfaceConfiguration."""
        return {
            "name": "View-Test-OSPF-Interface",
            "ospf_config": self.ospf_configurations["router1"].pk,
            "interface": self.interfaces["router1"]["ge2"].pk,
            "area": "0.0.0.99",
            "cost": 10,
            "status": self.statuses["active"].pk,
            "object_note": "",
            "dynamic_groups": [],
        }

    def get_csv_data(self):
        """Return CSV data for bulk import testing."""
        return (
            "name,ospf_config,interface,area,cost,status",
            f"CSV-OSPF-Int-1,{self.ospf_configurations['router1'].pk},{self.interfaces['router1']['loopback0'].pk},0.0.0.0,10,{self.statuses['active'].pk}",
        )

    def get_bulk_edit_data(self):
        """Return data for bulk edit testing."""
        return self.bulk_edit_data
