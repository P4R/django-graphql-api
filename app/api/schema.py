import graphene
from graphql_auth import mutations as mutations_auth

from api.mutations import idea, send_password_reset_email, user_following
from api.queries.idea import Query as IdeaQuery
from api.queries.user import Query as UserQuery
from api.queries.user_following import Query as UserFollowingQuery


class Query(IdeaQuery, UserQuery, UserFollowingQuery, graphene.ObjectType):
    pass


class AuthMutation(graphene.ObjectType):
    register = mutations_auth.Register.Field()
    login = mutations_auth.ObtainJSONWebToken.Field()
    password_change = mutations_auth.PasswordChange.Field()

    # This not generate a link to reset password, this generate a link
    # that contain a token, with this token is possible to call
    # passwordChange to reset password.
    # password_reset = mutations_auth.SendPasswordResetEmail.Field()

    # This sends email using default django form to reset password.
    password_reset = send_password_reset_email.SendPasswordResetEmail().Field()

    token_auth = mutations_auth.ObtainJSONWebToken.Field()
    verify_token = mutations_auth.VerifyToken.Field()
    refresh_token = mutations_auth.RefreshToken.Field()
    revoke_token = mutations_auth.RevokeToken.Field()


class Mutation(idea.Mutation, user_following.Mutation,
               AuthMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
