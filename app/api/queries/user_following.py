import graphene
from api.decorators import login_required_query
from api.types.user import UserType
from api.types.user_following import UserFollowingType
from core.models.user_following import UserFollowing


class Query(graphene.ObjectType):
    to_approve_following = graphene.List(UserFollowingType)
    followers = graphene.List(UserType)
    following = graphene.List(UserType)

    @login_required_query
    def resolve_to_approve_following(root, info):
        user = info.context.user
        return UserFollowing.objects.filter(following_user=user, status='p')

    @login_required_query
    def resolve_followers(root, info):
        user = info.context.user
        return [x.user for x in user.followers.filter(status='a')]

    @login_required_query
    def resolve_following(root, info):
        user = info.context.user
        return [x.following_user for x in user.following.filter(status='a')]
