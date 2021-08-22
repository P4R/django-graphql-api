import pdb
from api.schema import schema
from django.contrib.auth.models import User
from graphene_django.utils.testing import GraphQLTestCase
from graphql_jwt.shortcuts import get_token


class UserFollowingUnfollowTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema
    fixtures = ['fixtures.json']

    def setUp(self):
        user = User.objects.get(pk=1)
        self.unfollow_mutation = '''
        mutation unfollow($user_id: ID!) {
            unfollow(userId: $user_id){
                success
            }
        }
        '''
        self.headers = {
            'HTTP_AUTHORIZATION': 'JWT {}'.format(get_token(user))
        }

    def test_unfollow_ok(self):
        response = self.query(
            self.unfollow_mutation,
            op_name='unfollow',
            variables={
                'user_id': 2,
            },
            headers=self.headers
        )
        self.assertEquals(200, response.status_code)
        self.assertTrue(response.json().get('data').get(
            'unfollow').get('success'))

    def test_unfollow_without_login(self):
        response = self.query(
            self.unfollow_mutation,
            op_name='unfollow',
            variables={
                'user_id': 2,
            },
        )
        self.assertEquals(200, response.status_code)
        self.assertTrue(
            response.json().get('errors', False)
        )

    def test_unfollow_user_not_found(self):
        response = self.query(
            self.unfollow_mutation,
            op_name='unfollow',
            variables={
                'user_id': 99,
            },
            headers=self.headers
        )
        self.assertEquals(200, response.status_code)
        self.assertTrue(
            response.json().get('errors', False)
        )
