"""Module to Test GraphQL API queries"""

import unittest
from gql_query_builder import GqlQuery
from jsonpath_ng import parse
from python_graphql_client import GraphqlClient
from util.appconfig import AppConfig


class TestAppQueries(unittest.TestCase):
    """Test class"""

    def setUp(self):
        """Test setup"""
        self.host = AppConfig.conf_for_current_env()['host']
        self.path = AppConfig.conf_for_current_env()['api_path']
        self.client = GraphqlClient(
            endpoint="{}{}".format(self.host, self.path))

    def test_should_get_body_parts(self):
        """bodypart query test"""
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
        """equipment query test"""
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
        """stars query test"""
        expected_result = [{'number': 1, 'classification': 'poor'},
                           {'number': 2, 'classification': 'not good'},
                           {'number': 3, 'classification': 'good'},
                           {'number': 4, 'classification': 'very good'},
                           {'number': 5, 'classification': 'perfect'}]

        query = GqlQuery().fields(['number', 'classification']).query(
            'stars').operation().generate()

        data = self.client.execute(query=query)
        match = parse('data.stars[*]').find(data)
        actual_list_dict = [result.value for result in match]

        # assert list of dicts are equal ignoring order (python 3 only assert)
        self.assertCountEqual(actual_list_dict, expected_result)

    def test_workout_variable_query_for_expected_exercise_name(self):
        """workout query using variables test"""
        # set expected exercise name, as per the seeded data to db
        expected_exercise_name = 'straight bar military press'

        # create query that takes in a variable
        query = GqlQuery().fields(['name', 'description']).query(
            'workout', input={"level": "$level"}).operation("query",
                                                            name='workout_query',
                                                            input={
                                                                "$level": "String"}).generate()

        # Think of variables like arguments to method parameters.
        variables = {"level": "advanced"}

        # perform the request
        data = self.client.execute(query=query, variables=variables)

        # search through the response data for expected description
        exercise_names = [name.value for name in
                          parse('data.workout[*].name').find(data)]

        self.assertTrue(expected_exercise_name in exercise_names,
                        'Expected exercise name was not found in the response data')
