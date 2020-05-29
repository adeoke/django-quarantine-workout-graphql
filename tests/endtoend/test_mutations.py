import unittest
from util.config import Config
from python_graphql_client import GraphqlClient
from gql_query_builder import GqlQuery
from jsonpath_ng import parse


class TestAppMutations(unittest.TestCase):
    def setUp(self):
        self.host = Config.conf_for_current_env()['host']
        self.path = Config.conf_for_current_env()['api_path']
        self.client = GraphqlClient(
            endpoint="{}{}".format(self.host, self.path))

    def test_create_user_returns_token_in_data_response(self):
        # step 1 create the user
        # user_field = GqlQuery().fields(['username', 'email', 'id']).query(
        #     name='user').generate()
        #
        # query = GqlQuery().fields([user_field]).query("createUser", input={
        #     "email": "\"anemail4@example.com\"",
        #     "password": "\"password123\"",
        #     "username": "\"auserisnamed4\""}).operation("mutation"
        #                                             ).generate()
        # print(query)
        # data = self.client.execute(query=query)
        # print(data)

        # step 2 use the user to authenticate

        query = GqlQuery().fields(['token']).query("tokenAuth", input={"password": "\"password123\"",
        "username": "\"auserisnamed4\""}).operation("mutation", name="").generate()

        data = self.client.execute(query=query)
        print(data)

        # authenticate that the token is returned.




# client info
# https://stackoverflow.com/questions/48693825/making-a-graphql-mutation-from-my-python-code-getting-error

# builder
# https://gist.github.com/gbaman/b3137e18c739e0cf98539bf4ec4366ad
