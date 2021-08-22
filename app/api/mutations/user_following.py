import graphene
from api.decorators import login_required_mutation
from api.types.user_following import UserFollowingType
from core.models.user_following import UserFollowing
from django.contrib.auth.models import User


class FollowMutation(graphene.Mutation):
    '''Follow user, user need to be
       logged.'''
    class Arguments:
        user_id = graphene.ID(required=True)

    user_following = graphene.Field(UserFollowingType)

    @classmethod
    @login_required_mutation
    def mutate(cls, root, info, user_id):
        user = User.objects.filter(pk=user_id)
        if not user.exists():
            raise Exception('User not found!')
        user = user.first()
        me = info.context.user
        user_following = UserFollowing()
        user_following.user = me
        user_following.following_user = user
        user_following.status = 'p'
        user_following.save()
        return FollowMutation(user_following=user_following)


class UnfollowMutation(graphene.Mutation):
    '''Unfollow user, user need to be
       logged.'''
    class Arguments:
        user_id = graphene.ID(required=True)

    success = graphene.Field(graphene.Boolean)

    @classmethod
    @login_required_mutation
    def mutate(cls, root, info, user_id):
        user = info.context.user
        f_user = User.objects.filter(pk=user_id)
        if not f_user.exists():
            raise Exception("Follwer not found")
        f_user = f_user.first()
        following_user = UserFollowing.objects.filter(
            user=user, following_user=f_user)
        if following_user.exists():
            following_user.first().delete()
        return UnfollowMutation(success=True)


class RemoveFollowerMutation(graphene.Mutation):
    '''Remove follower, user need to be
       logged.'''
    class Arguments:
        user_id = graphene.ID(required=True)

    success = graphene.Field(graphene.Boolean)

    @classmethod
    @login_required_mutation
    def mutate(cls, root, info, user_id):
        f_user = info.context.user
        user = User.objects.filter(pk=user_id)
        if not user.exists():
            raise Exception("User not found")
        user = user.first()
        following_user = UserFollowing.objects.filter(
            user=user, following_user=f_user)
        if following_user.exists():
            following_user.first().delete()
        return RemoveFollowerMutation(success=True)


class AccceptFollowMutation(graphene.Mutation):
    '''Accept or deny follower, user need to be
       logged.'''
    class Arguments:
        id = graphene.ID(required=True)
        accept = graphene.Boolean(required=True)

    user_following = graphene.Field(UserFollowingType)

    @classmethod
    @login_required_mutation
    def mutate(cls, root, info, id, accept):
        user = info.context.user
        user_following = UserFollowing.objects.filter(
            pk=id, following_user=user)
        if not user_following.exists():
            raise Exception('User Following not found!')
        user_following = user_following.first()
        if accept:
            user_following.status = 'a'
        else:
            user_following.status = 'd'
        user_following.save()
        return FollowMutation(user_following=user_following)


class Mutation(graphene.ObjectType):
    follow = FollowMutation.Field()
    unfollow = UnfollowMutation.Field()
    accept_follow = AccceptFollowMutation.Field()
    remove_follower = RemoveFollowerMutation.Field()
