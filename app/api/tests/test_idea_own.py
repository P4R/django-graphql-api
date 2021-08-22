from api.schema import schema
from django.contrib.auth.models import User
from graphene_django.utils.testing import GraphQLTestCase
from graphql_jwt.shortcuts import get_token


class IdeaOwnTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema
    fixtures = ['fixtures.json']

    def setUp(self):
        user = User.objects.get(pk=2)
        self.own_ideas_query = '''
        query {
            ownIdeas {
                id,
                title
            }
        }
        '''
        self.headers = {
            'HTTP_AUTHORIZATION': 'JWT {}'.format(get_token(user))
        }

    def test_own_ideas_ok(self):
        response = self.query(
            self.own_ideas_query,
            headers=self.headers
        )
        self.assertEquals(200, response.status_code)
        self.assertEquals(
            3,
            len(response.json().get('data').get('ownIdeas'))
        )

    def test_own_ideas_without_login(self):
        response = self.query(
            self.own_ideas_query,
        )
        self.assertEquals(200, response.status_code)
        self.assertTrue(
            response.json().get('errors', False)
        )
