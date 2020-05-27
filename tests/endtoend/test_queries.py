import unittest
from util.config import Config
from python_graphql_client import GraphqlClient
from gql_query_builder import GqlQuery
import json
from jsonpath_ng import jsonpath, parse


class TestLinkQueries(unittest.TestCase):
    def setUp(self):
        self.host = Config.conf_for_current_env()['host']
        self.path = Config.conf_for_current_env()['api_path']
        self.client = GraphqlClient(
            endpoint="{}{}".format(self.host, self.path))

    def test_should_get_body_parts(self):
        expected_body_parts = ['upper body', 'lower body', 'cardio']

        query = GqlQuery().fields(['name']).query(
            'bodyParts').operation().generate()
        data = self.client.execute(query=query)

        jsonpath_expr = parse('data.bodyParts[*].name')
        actual_body_parts = [match.value for match in jsonpath_expr.find(data)]

        self.assertEqual(sorted(actual_body_parts),
                         sorted(expected_body_parts),
                         'expected body parts to be the same, but were not')

    def test_should_get_all_equipment_types(self):
        expected_equipment = ['dumbbells', 'resistance bands', 'barbell',
                              'none']

        query = GqlQuery().fields(['name']).query(
            'equipment').operation().generate()
        data = self.client.execute(query=query)

        jsonpath_expr = parse('data.equipment[*].name')
        actual_equipment = [match.value for match in jsonpath_expr.find(data)]

        self.assertEqual(sorted(actual_equipment), sorted(expected_equipment),
                         'expected equipment to be the same, but were not')

    def test_should_verify_all_stars_details(self):
        expected_result = [{'number': 1, 'classification': 'poor'},
                           {'number': 2, 'classification': 'not good'},
                           {'number': 3, 'classification': 'good'},
                           {'number': 4, 'classification': 'very good'},
                           {'number': 5, 'classification': 'perfect'}]

        query = GqlQuery().fields(['number', 'classification']).query(
            'stars').operation().generate()

        data = self.client.execute(query=query)
        match = parse('data.stars[*]').find(data)
        actual_list_dict = []
        [actual_list_dict.append(result.value) for result in match]

        # assert list of dicts are equal ignoring order (python 3 only assert)
        self.assertCountEqual(actual_list_dict, expected_result)
