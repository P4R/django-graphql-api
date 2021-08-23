from api.schema import schema
from django.contrib.auth.models import User
from graphene_django.utils.testing import GraphQLTestCase
from graphql_jwt.shortcuts import get_token


class UserFollowingFollowTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema
    fixtures = ['fixtures.json']

    def setUp(self):
        user = User.objects.get(pk=2)
        self.follow_mutation = '''
        mutation follow($user_id: ID!) {
            follow(userId: $user_id){
                userFollowing{
                    status
                    user{
                        id
                    }
                    followingUser{
                        id
                    }
                }
            }
        }
        '''
        self.headers = {
            'HTTP_AUTHORIZATION': 'JWT {}'.format(get_token(user))
        }

    def test_follow_ok(self):
        response = self.query(
            self.follow_mutation,
            op_name='follow',
            variables={
                'user_id': 3,
            },
            headers=self.headers
        )
        self.assertEquals(200, response.status_code)
        data = response.json().get('data').get(
            'follow').get('userFollowing')
        self.assertEquals('p', data.get('status').lower())
        self.assertEquals(2, int(data.get('user').get('id')))
        self.assertEquals(3, int(data.get('followingUser').get('id')))

    def test_follow_without_login(self):
        response = self.query(
            self.follow_mutation,
            op_name='follow',
            variables={
                'user_id': 3,
            },
        )
        self.assertEquals(200, response.status_code)
        self.assertTrue(
            response.json().get('errors', False)
        )

    def test_follow_user_not_found(self):
        response = self.query(
            self.follow_mutation,
            op_name='follow',
            variables={
                'user_id': 99,
            },
            headers=self.headers
        )
        self.assertEquals(200, response.status_code)
        self.assertTrue(
            response.json().get('errors', False)
        )
