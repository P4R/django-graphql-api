from api.schema import schema
from django.contrib.auth.models import User
from graphene_django.utils.testing import GraphQLTestCase
from graphql_jwt.shortcuts import get_token


class UserFollowingToApproveTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema
    fixtures = ['fixtures.json']

    def setUp(self):
        user = User.objects.get(pk=3)
        self.to_approve_query = '''
        query {
            toApproveFollowing {
                id,
                status
            }
        }
        '''
        self.headers = {
            'HTTP_AUTHORIZATION': 'JWT {}'.format(get_token(user))
        }

    def test_to_approve_ok(self):
        response = self.query(
            self.to_approve_query,
            headers=self.headers
        )
        self.assertEquals(200, response.status_code)
        data = response.json().get('data').get('toApproveFollowing')
        self.assertEquals(
            1,
            len(data)
        )
        self.assertEquals(
            ['p'],
            list(set(map(lambda x: x.get('status').lower(), data)))
        )

    def test_to_approve_without_login(self):
        response = self.query(
            self.to_approve_query,
        )
        self.assertEquals(200, response.status_code)
        self.assertTrue(
            response.json().get('errors', False)
        )
