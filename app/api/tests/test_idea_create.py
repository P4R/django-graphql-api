from api.schema import schema
from django.contrib.auth.models import User
from graphene_django.utils.testing import GraphQLTestCase
from graphql_jwt.shortcuts import get_token


class CreateIdeaTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema
    fixtures = ['fixtures.json']

    def setUp(self):
        user = User.objects.get(pk=1)
        self.create_idea_mutation = '''
        mutation createIdea(
            $title: String!,
            $description: String!,
            $visibility: String!) {
            createIdea(
                title: $title,
                description: $description,
                visibility: $visibility
            ){
               idea{
                   id
               }
            }
        }
        '''
        self.headers = {
            'HTTP_AUTHORIZATION': 'JWT {}'.format(get_token(user))
        }

    def test_create_idea_ok(self):
        response = self.query(
            self.create_idea_mutation,
            op_name='createIdea',
            variables={
                'title': 'Idea Test',
                'description': 'Idea Test Description',
                'visibility': 'pub'
            },
            headers=self.headers
        )
        self.assertEquals(200, response.status_code)
        self.assertTrue(
            'pri',
            response.json().get('data').get('createIdea').get(
                'idea').get('id', False)
        )

    def test_create_idea_without_login(self):
        response = self.query(
            self.create_idea_mutation,
            op_name='createIdea',
            variables={
                'title': 'Idea Test',
                'description': 'Idea Test Description',
                'visibility': 'pub'
            },
        )
        self.assertEquals(200, response.status_code)
        self.assertTrue(
            response.json().get('errors', False)
        )

    def test_create_idea_without_title(self):
        response = self.query(
            self.create_idea_mutation,
            op_name='createIdea',
            variables={
                'description': 'Idea Test Description',
                'visibility': 'pub'
            },
            headers=self.headers
        )
        self.assertEquals(400, response.status_code)
        self.assertTrue(
            response.json().get('errors', False)
        )
