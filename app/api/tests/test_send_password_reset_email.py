from api.schema import schema
from graphene_django.utils.testing import GraphQLTestCase


class SendPasswordResetTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema
    fixtures = ['fixtures.json']

    def setUp(self):
        self.password_reset_mutation = '''
        mutation passwordReset($email: String!) {
            passwordReset(email: $email) {
                success
                errors
            }
        }
        '''

    def test_password_reset_ok(self):
        response = self.query(
            self.password_reset_mutation,
            op_name='passwordReset',
            variables={'email': 'pere@test.com'}
        )
        self.assertEquals(200, response.status_code)
        self.assertTrue(response.json().get(
            'data').get('passwordReset').get('success'))

    def test_password_reset_ko(self):
        response = self.query(
            self.password_reset_mutation,
            op_name='passwordReset',
            variables={'email': 'invalidad_email@email.com'}
        )
        self.assertEquals(200, response.status_code)
        self.assertFalse(response.json().get(
            'data').get('passwordReset').get('success'))
