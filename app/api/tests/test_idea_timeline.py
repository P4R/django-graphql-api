from api.schema import schema
from django.contrib.auth.models import User
from graphene_django.utils.testing import GraphQLTestCase
from graphql_jwt.shortcuts import get_token


class IdeaTimelineTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema
    fixtures = ['fixtures.json']

    def setUp(self):
        user = User.objects.get(pk=1)
        self.timeline_query = '''
        query {
            timeline {
                id,
                title,
                description
            }
        }
        '''
        self.headers = {
            'HTTP_AUTHORIZATION': 'JWT {}'.format(get_token(user))
        }

    def test_own_ideas_ok(self):
        response = self.query(
            self.timeline_query,
            headers=self.headers
        )
        self.assertEquals(200, response.status_code)
        self.assertEquals(
            3,
            len(response.json().get('data').get('timeline'))
        )

    def test_own_ideas_without_login(self):
        response = self.query(
            self.timeline_query,
        )
        self.assertEquals(200, response.status_code)
        self.assertTrue(
            response.json().get('errors', False)
        )
