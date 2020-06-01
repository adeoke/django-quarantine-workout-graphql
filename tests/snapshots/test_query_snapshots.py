from gql_query_builder import GqlQuery
from python_graphql_client import GraphqlClient
from snapshottest import TestCase

from util.appconfig import AppConfig


class APITestCase(TestCase):
    def setUp(self):
        self.host = AppConfig.conf_for_current_env()['host']
        self.path = AppConfig.conf_for_current_env()['api_path']
        self.client = GraphqlClient(
            endpoint="{}{}".format(self.host, self.path))

    def test_levels_response_against_snapshot(self):
        """Testing the API for /me"""

        query = GqlQuery().fields(['difficulty']).query(
            'levels').operation().generate()

        levels_resp = self.client.execute(query=query)
        self.assertMatchSnapshot(levels_resp, 'levels_snapshot_resp')

    def test_equipment_against_snapshot(self):
        query = GqlQuery().fields(['difficulty']).query(
            'levels').operation().generate()

        equipment_resp = self.client.execute(query=query)
        self.assertMatchSnapshot(equipment_resp, 'equipment_snapshot_resp')
