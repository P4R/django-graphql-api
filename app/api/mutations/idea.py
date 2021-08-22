import graphene
from api.decorators import login_required_mutation
from api.types.idea import IdeaType
from core.models.idea import Idea


class IdeaEditVisibilityMutation(graphene.Mutation):
    '''Changes visibility of idea, user need to be
       logged and the owner of idea.'''
    class Arguments:
        visibility = graphene.String(required=True)
        id = graphene.ID(required=True)

    idea = graphene.Field(IdeaType)

    @classmethod
    @login_required_mutation
    def mutate(cls, root, info, visibility, id):
        user = info.context.user
        idea = Idea.objects.get(pk=id)
        if idea.user != user:
            raise Exception('You are not the owner!')
        idea.visibility = visibility
        idea.save()
        if visibility in ['pub', 'pro']:
            followers = [x.user for x in user.followers.filter(status='a')]  # noqa
            # TODO: Call method to send notification to followers
            # First we need to save device token of user to send notifications
            # See:
            #    - https://github.com/olucurious/PyFCM/
            #    - https://github.com/xtrinch/fcm-django
        return IdeaEditVisibilityMutation(idea=idea)


class IdeaDeleteMutation(graphene.Mutation):
    '''Delete idea, user need to be
       logged and the owner of idea.'''
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Field(graphene.Boolean)

    @classmethod
    @login_required_mutation
    def mutate(cls, root, info, id):
        user = info.context.user
        idea = Idea.objects.get(pk=id)
        if idea.user != user:
            raise Exception('You are not the owner!')
        idea.delete()
        return IdeaDeleteMutation(success=True)


class IdeaCreateMutation(graphene.Mutation):
    '''Create idea, user need to be
       logged and the owner of idea.'''
    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String(required=True)
        visibility = graphene.String(required=True)

    idea = graphene.Field(IdeaType)

    @classmethod
    @login_required_mutation
    def mutate(cls, root, info, title, description, visibility):
        user = info.context.user
        idea = Idea()
        idea.title = title
        idea.description = description
        idea.visibility = visibility
        idea.user = user
        idea.save()
        if visibility in ['pub', 'pro']:
            followers = [x.user for x in user.followers.filter(status='a')]  # noqa
            # TODO: Call method to send notification to followers
            # First we need to save device token of user to send notifications
            # See:
            #    - https://github.com/olucurious/PyFCM/
            #    - https://github.com/xtrinch/fcm-django
        return IdeaCreateMutation(idea=idea)


class Mutation(graphene.ObjectType):
    edit_visibility_idea = IdeaEditVisibilityMutation.Field()
    create_idea = IdeaCreateMutation.Field()
    delete_idea = IdeaDeleteMutation.Field()
