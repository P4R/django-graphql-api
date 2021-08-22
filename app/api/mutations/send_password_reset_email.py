import graphene
from api import mixins
from graphql_auth.bases import DynamicArgsMixin, MutationMixin


class SendPasswordResetEmail(
        MutationMixin, DynamicArgsMixin,
        mixins.SendPasswordResetEmailMixin, graphene.Mutation):
    """
    Send password reset email with link to restore password.
    """
    _required_args = ["email"]
