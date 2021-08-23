from api.schema import schema
from django.contrib.auth.models import User
from graphene_django.utils.testing import GraphQLTestCase
from graphql_jwt.shortcuts import get_token


class DeleteIdeaTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema
    fixtures = ['fixtures.json']

    def setUp(self):
        user = User.objects.get(pk=1)
        self.delete_idea_mutation = '''
        mutation deleteIdea($id: ID!) {
            deleteIdea(id: $id){
               success
            }
        }
        '''
        self.headers = {
            'HTTP_AUTHORIZATION': 'JWT {}'.format(get_token(user))
        }

    def test_delete_idea_without_login(self):
        response = self.query(
            self.delete_idea_mutation,
            op_name='deleteIdea',
            variables={
                'id': 1,
            },
        )
        self.assertEquals(200, response.status_code)
        self.assertTrue(
            response.json().get(
                'errors', False)
        )

    def test_delete_idea_ok(self):
        response = self.query(
            self.delete_idea_mutation,
            op_name='deleteIdea',
            variables={
                'id': 1,
            },
            headers=self.headers
        )
        self.assertEquals(200, response.status_code)
        self.assertTrue(
            response.json().get('data').get(
                'deleteIdea').get('success', False)
        )

    def test_delete_idea_no_owner(self):
        response = self.query(
            self.delete_idea_mutation,
            op_name='deleteIdea',
            variables={
                'id': 2,
            },
            headers=self.headers
        )
        self.assertEquals(200, response.status_code)
        self.assertTrue(
            response.json().get(
                'errors', False)
        )
