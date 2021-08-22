import pdb
from api.schema import schema
from django.contrib.auth.models import User
from graphene_django.utils.testing import GraphQLTestCase
from graphql_jwt.shortcuts import get_token


class UserFollowingAcceptFollowTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema
    fixtures = ['fixtures.json']

    def setUp(self):
        user = User.objects.get(pk=3)
        self.follow_mutation = '''
        mutation acceptFollow($id: ID!, $accept: Boolean!) {
            acceptFollow(id: $id, accept: $accept){
                userFollowing{
                    status
                }
            }
        }
        '''
        self.headers = {
            'HTTP_AUTHORIZATION': 'JWT {}'.format(get_token(user))
        }

    def test_accept_follow_ok(self):
        response = self.query(
            self.follow_mutation,
            op_name='acceptFollow',
            variables={
                'id': 2,
                'accept': True
            },
            headers=self.headers
        )
        self.assertEquals(200, response.status_code)
        data = response.json().get('data').get(
            'acceptFollow').get('userFollowing')
        self.assertEquals('a', data.get('status').lower())

    def test_deny_follow_ok(self):
        response = self.query(
            self.follow_mutation,
            op_name='acceptFollow',
            variables={
                'id': 2,
                'accept': False
            },
            headers=self.headers
        )
        self.assertEquals(200, response.status_code)
        data = response.json().get('data').get(
            'acceptFollow').get('userFollowing')
        self.assertEquals('d', data.get('status').lower())

    def test_accept_follow_without_login(self):
        response = self.query(
            self.follow_mutation,
            op_name='acceptFollow',
            variables={
                'id': 2,
                'accept': False
            },
        )
        self.assertEquals(200, response.status_code)
        self.assertTrue(
            response.json().get('errors', False)
        )

    def test_accept_follow_not_found(self):
        response = self.query(
            self.follow_mutation,
            op_name='acceptFollow',
            variables={
                'id': 99,
                'accept': False
            },
            headers=self.headers
        )
        self.assertEquals(200, response.status_code)
        self.assertTrue(
            response.json().get('errors', False)
        )
