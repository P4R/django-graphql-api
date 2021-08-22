from core.models.user_following import UserFollowing
from graphene_django import DjangoObjectType


class UserFollowingType(DjangoObjectType):

    class Meta:
        model = UserFollowing
