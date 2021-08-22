import graphene
from api.decorators import login_required_query
from api.types.user import UserType
from django.contrib.auth.models import User
from django.db.models import Q


class Query(graphene.ObjectType):
    user_search = graphene.Field(
        graphene.List(UserType),
        user=graphene.String(required=True)
    )

    @login_required_query
    def resolve_user_search(root, info, user):
        return User.objects.filter(
            Q(username__icontains=user) |
            Q(first_name__icontains=user) |
            Q(last_name__icontains=user)
        )
