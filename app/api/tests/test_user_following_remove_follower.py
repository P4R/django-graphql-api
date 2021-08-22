import pdb
from api.schema import schema
from django.contrib.auth.models import User
from graphene_django.utils.testing import GraphQLTestCase
from graphql_jwt.shortcuts import get_token


class UserFollowingRemoveFollowerTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema
    fixtures = ['fixtures.json']

    def setUp(self):
        user = User.objects.get(pk=1)
        self.remove_follower_mutation = '''
        mutation removeFollower($user_id: ID!) {
            removeFollower(userId: $user_id){
                success
            }
        }
        '''
        self.headers = {
            'HTTP_AUTHORIZATION': 'JWT {}'.format(get_token(user))
        }

    def test_remove_follower_ok(self):
        response = self.query(
            self.remove_follower_mutation,
            op_name='removeFollower',
            variables={
                'user_id': 2,
            },
            headers=self.headers
        )
        self.assertEquals(200, response.status_code)
        self.assertTrue(response.json().get('data').get(
            'removeFollower').get('success'))

    def test_remove_follower_without_login(self):
        response = self.query(
            self.remove_follower_mutation,
            op_name='removeFollower',
            variables={
                'user_id': 2,
            },
        )
        self.assertEquals(200, response.status_code)
        self.assertTrue(
            response.json().get('errors', False)
        )

    def test_remove_follower_user_not_found(self):
        response = self.query(
            self.remove_follower_mutation,
            op_name='removeFollower',
            variables={
                'user_id': 99,
            },
            headers=self.headers
        )
        self.assertEquals(200, response.status_code)
        self.assertTrue(
            response.json().get('errors', False)
        )
