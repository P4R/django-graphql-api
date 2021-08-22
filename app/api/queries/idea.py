import graphene
from api.decorators import login_required_query
from api.types.idea import IdeaType
from core.models.idea import Idea
from django.contrib.auth.models import User


class Query(graphene.ObjectType):
    own_ideas = graphene.List(IdeaType)
    user_ideas = graphene.Field(graphene.List(
        IdeaType), user_id=graphene.ID(required=True))
    timeline = graphene.List(IdeaType)

    @login_required_query
    def resolve_own_ideas(root, info):
        # We can use user_ideas sending current user_id
        user = info.context.user
        return Idea.objects.filter(user=user).order_by('-pub_date')

    @login_required_query
    def resolve_user_ideas(root, info, user_id):
        user_query = User.objects.filter(pk=user_id)
        if not user_query.exists():
            raise Exception('User not found!')

        user = info.context.user
        user_query = user_query.first()
        visibility = ['pub']
        followers = [x.user for x in user_query.followers.filter(status='a')]
        if user in followers:
            visibility.append('pro')
        elif user.id == user_id:
            visibility.append('pri')
            visibility.append('pro')
        filt = {
            'user__id': user_id,
            'visibility__in': visibility
        }
        return Idea.objects.filter(**filt).order_by('-pub_date')

    @login_required_query
    def resolve_timeline(root, info):
        user = info.context.user
        following = [
            x.following_user for x in user.following.filter(status='a')]
        ideas = Idea.objects.filter(visibility='pub')
        ideas |= Idea.objects.filter(user=user, visibility__in=['pri', 'pro'])
        ideas |= Idea.objects.filter(user__in=following, visibility='pro')
        return ideas.order_by('-pub_date')
