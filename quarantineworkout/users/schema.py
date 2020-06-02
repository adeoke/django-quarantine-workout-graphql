"""Users schema module"""
import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model


class UserType(DjangoObjectType):
    """User type class"""

    class Meta:
        """model mapping to user models"""
        model = get_user_model()


class CreateUser(graphene.Mutation):
    """User mutation/creation class"""
    user = graphene.Field(UserType)

    class Arguments:
        """user creation arguments class"""
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        """user mutation logic function"""
        user = get_user_model()(
            username=username,
            email=email,
        )
        # you must set the password separately.
        user.set_password(password)
        user.save()

        return CreateUser(
            user=user
        )


class Mutation(graphene.ObjectType):
    """User mutation class"""
    create_user = CreateUser.Field()


class Query(graphene.ObjectType):
    """Users query class"""
    users = graphene.List(UserType)

    def resolve_users(self, info):
        """Resolve users function"""
        # TODO: only display certain fields for user based on authentication criteria
        return get_user_model().objects.all()
