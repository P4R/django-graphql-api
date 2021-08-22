from core.models.idea import Idea
from graphene_django import DjangoObjectType


class IdeaType(DjangoObjectType):
    class Meta:
        model = Idea
