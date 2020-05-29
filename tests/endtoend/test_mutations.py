import unittest
from util.config import Config
from python_graphql_client import GraphqlClient
from gql_query_builder import GqlQuery
from faker import Faker
from faker.providers import profile
from jsonpath_ng import parse


class TestAppMutations(unittest.TestCase):
    def setUp(self):
        self.fake = Faker()
        self.fake.add_provider(profile)
        self.host = Config.conf_for_current_env()['host']
        self.path = Config.conf_for_current_env()['api_path']
        self.client = GraphqlClient(
            endpoint="{}{}".format(self.host, self.path))

    def test_create_user_returns_token_in_data_response(self):
        username = self.fake.simple_profile()['username']
        email = self.fake.simple_profile()['mail']

        # step 1 create the user
        user_field = GqlQuery().fields(['username', 'email', 'id']).query(
            name='user').generate()

        query = GqlQuery().fields([user_field]).query("createUser", input={
            "email": "\"{}\"".format(email),
            "password": "\"password123\"",
            "username": "\"{}\"".format(username)}).operation("mutation"
                                                              ).generate()
        data = self.client.execute(query=query)

        # step 2 use the user to authenticate

        query = GqlQuery().fields(['token']).query("tokenAuth", input={
            "password": "\"password123\"",
            "username": "\"{}\"".format(username)}).operation("mutation",
                                                              name="").generate()

        data = self.client.execute(query=query)
        token = parse('data.tokenAuth.token').find(data)[0].value
        self.assertIsNotNone(token)


