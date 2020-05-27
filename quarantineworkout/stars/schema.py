import graphene
from graphene_django import DjangoObjectType
from .models import Star


class StarType(DjangoObjectType):
    class Meta:
        model = Star


class Query(graphene.ObjectType):
    stars = graphene.List(StarType)

    def resolve_stars(self, info):
        return Star.objects.all()
