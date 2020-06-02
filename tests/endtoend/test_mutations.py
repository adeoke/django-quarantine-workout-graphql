"""Mutations test module"""
import unittest
from faker import Faker
from faker.providers import profile
from gql_query_builder import GqlQuery
from jsonpath_ng import parse
from python_graphql_client import GraphqlClient
from util.appconfig import AppConfig


class TestAppMutations(unittest.TestCase):
    """Mutations test class"""

    def setUp(self):
        """Test setup method"""
        self.fake = Faker()
        self.fake.add_provider(profile)
        self.host = AppConfig.conf_for_current_env()['host']
        self.path = AppConfig.conf_for_current_env()['api_path']
        self.client = GraphqlClient(
            endpoint="{}{}".format(self.host, self.path))

    def test_using_variables_for_existing_user_obtains_token_auth_in_response_data(
            self):
        """User authentication test"""
        username = AppConfig.conf_for_current_env()['user']['username']
        password = AppConfig.conf_for_current_env()['user']['password']

        query = GqlQuery().fields(
            ['token', 'payload', 'refreshExpiresIn']) \
            .query("tokenAuth", input={"username": "\"{}\"".format(username), \
                                       "password": "\"{}\"".format( \
                                           password)}).operation( \
            "mutation", name="userAuth").generate()

        data = self.client.execute(query=query)

        token_expr = 'data.tokenAuth.token'
        username_expr = 'data.tokenAuth.payload.username'
        refresh_expires_in_expr = 'data.tokenAuth.refreshExpiresIn'

        response_token = parse(token_expr).find(data)[0].value
        response_username = parse(username_expr).find(data)[0].value
        response_expiry = parse(refresh_expires_in_expr).find(data)[0].value

        self.assertIsNotNone(response_token)
        self.assertEqual(response_username, username,
                         'Expected username {}, but got {}'.format(username,
                                                                   response_username))
        self.assertIsNotNone(response_expiry)

    def test_create_user_returns_token_in_data_response(self):
        """User mutation test"""
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
        create_user_data = self.client.execute(query=query)

        # check user is created
        username_expr = 'data.createUser.user.username'
        email_expr = 'data.createUser.user.email'

        username_resp = parse(username_expr).find(create_user_data)[0].value
        email_resp = parse(email_expr).find(create_user_data)[0].value

        self.assertEqual(username_resp, username,
                         'Expected username {}, but got {}.'.format(username,
                                                                    username_resp))
        self.assertEqual(email_resp, email,
                         'Expected email {}, but got {}.'.format(email,
                                                                 email_resp))

        # step 2 use the user to authenticate
        query = GqlQuery().fields(['token']).query("tokenAuth", input={
            "password": "\"password123\"",
            "username": "\"{}\"".format(username)}).operation("mutation",
                                                              name="").generate()

        data = self.client.execute(query=query)
        token_expr = 'data.tokenAuth.token'

        token = parse(token_expr).find(data)[0].value
        self.assertIsNotNone(token)
