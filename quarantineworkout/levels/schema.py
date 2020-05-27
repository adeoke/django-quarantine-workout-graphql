import graphene
from graphene_django import DjangoObjectType
from .models import Level


class LevelType(DjangoObjectType):
    class Meta:
        model = Level


class Query(graphene.ObjectType):
    levels = graphene.List(LevelType)

    def resolve_levels(self, info):
        return Level.objects.all()
