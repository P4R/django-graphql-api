from api.schema import schema
from django.contrib.auth.models import User
from graphene_django.utils.testing import GraphQLTestCase
from graphql_jwt.shortcuts import get_token


class IdeaUserTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema
    fixtures = ['fixtures.json']

    def setUp(self):
        user = User.objects.get(pk=1)
        self.user_ideas_query = '''
        query userIdeas($user_id: ID!){
            userIdeas(userId: $user_id){
                id,
            }
        }
        '''
        self.headers = {
            'HTTP_AUTHORIZATION': 'JWT {}'.format(get_token(user))
        }

    def test_user_ideas_ok(self):
        response = self.query(
            self.user_ideas_query,
            variables={
                'user_id': 2
            },
            headers=self.headers
        )
        self.assertEquals(200, response.status_code)
        self.assertEquals(
            2,
            len(response.json().get('data').get('userIdeas'))
        )

    def test_user_ideas_without_login(self):
        response = self.query(
            self.user_ideas_query,
            variables={
                'user_id': 2
            },
        )
        self.assertEquals(200, response.status_code)
        self.assertTrue(
            response.json().get('errors', False)
        )
