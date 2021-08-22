from api.schema import schema
from django.contrib.auth.models import User
from graphene_django.utils.testing import GraphQLTestCase
from graphql_jwt.shortcuts import get_token


class EditVibilityIdeaTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema
    fixtures = ['fixtures.json']

    def setUp(self):
        user = User.objects.get(pk=1)
        self.edit_idea_visibility_mutation = '''
        mutation editVisibilityIdea($id: ID!, $visibility: String!) {
            editVisibilityIdea(id: $id, visibility: $visibility) {
               idea{
                   visibility
               }
            }
        }
        '''
        self.headers = {
            'HTTP_AUTHORIZATION': 'JWT {}'.format(get_token(user))
        }

    def test_edit_idea_visibility_ok(self):
        response = self.query(
            self.edit_idea_visibility_mutation,
            op_name='editVisibilityIdea',
            variables={'id': 1, 'visibility': 'pri'},
            headers=self.headers
        )
        self.assertEquals(200, response.status_code)
        self.assertEquals(
            'pri',
            response.json().get('data').get('editVisibilityIdea').get(
                'idea').get('visibility').lower()
        )

    def test_edit_idea_visibility_without_login(self):
        response = self.query(
            self.edit_idea_visibility_mutation,
            op_name='editVisibilityIdea',
            variables={'id': 1, 'visibility': 'pri'},
        )
        self.assertEquals(200, response.status_code)
        self.assertTrue(
            response.json().get('errors', False)
        )

    def test_edit_idea_visibility_other_user(self):
        response = self.query(
            self.edit_idea_visibility_mutation,
            op_name='editVisibilityIdea',
            variables={'id': 2, 'visibility': 'pri'},
        )
        self.assertEquals(200, response.status_code)
        self.assertTrue(
            response.json().get('errors', False)
        )
