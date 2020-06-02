"""Stars Schema module"""
import graphene
from graphene_django import DjangoObjectType
from .models import Star


class StarType(DjangoObjectType):
    """Stars Object type"""
    class Meta:
        """Mapping model to Star ORM class"""
        model = Star


class Query(graphene.ObjectType):
    """Star query class"""
    stars = graphene.List(StarType)

    def resolve_stars(self, info):
        """resolve stars query function"""
        return Star.objects.all()
