from api.schema import schema
from django.contrib.auth.models import User
from graphene_django.utils.testing import GraphQLTestCase
from graphql_jwt.shortcuts import get_token


class UserFollowingFollowersCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema
    fixtures = ['fixtures.json']

    def setUp(self):
        user = User.objects.get(pk=2)
        self.followers_query = '''
        query {
            followers {
                id,
                username
            }
        }
        '''
        self.headers = {
            'HTTP_AUTHORIZATION': 'JWT {}'.format(get_token(user))
        }

    def test_followers_ok(self):
        response = self.query(
            self.followers_query,
            headers=self.headers
        )
        self.assertEquals(200, response.status_code)
        data = response.json().get('data').get('followers')
        self.assertEquals(
            1,
            len(data)
        )
        self.assertTrue(
            1 in list(map(lambda x: int(x.get('id')), data))
        )

    def test_followers_without_login(self):
        response = self.query(
            self.followers_query,
        )
        self.assertEquals(200, response.status_code)
        self.assertTrue(
            response.json().get('errors', False)
        )
