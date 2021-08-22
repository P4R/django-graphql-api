from api.schema import schema
from django.contrib.auth.models import User
from graphene_django.utils.testing import GraphQLTestCase
from graphql_jwt.shortcuts import get_token


class UserSearchTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema
    fixtures = ['fixtures.json']

    def setUp(self):
        user = User.objects.get(pk=1)
        self.search_user_query = '''
        query userSearch($user: String!){
            userSearch(user: $user){
                id,
                username
            }
        }
        '''
        self.headers = {
            'HTTP_AUTHORIZATION': 'JWT {}'.format(get_token(user))
        }

    def test_search_user_ok(self):
        response = self.query(
            self.search_user_query,
            op_name='userSearch',
            variables={
                'user': 'pere2'
            },
            headers=self.headers
        )
        self.assertEquals(200, response.status_code)
        self.assertEquals(
            1,
            len(response.json().get('data').get('userSearch'))
        )

    def test_search_user_ok_2(self):
        response = self.query(
            self.search_user_query,
            op_name='userSearch',
            variables={
                'user': 'pere'
            },
            headers=self.headers
        )
        self.assertEquals(200, response.status_code)
        self.assertEquals(
            3,
            len(response.json().get('data').get('userSearch'))
        )

    def test_user_search_without_login(self):
        response = self.query(
            self.search_user_query,
            op_name='userSearch',
            variables={
                'user': 'pere'
            },
        )
        self.assertEquals(200, response.status_code)
        self.assertTrue(
            response.json().get('errors', False)
        )
