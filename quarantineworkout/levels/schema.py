"""Levels schema module"""
import graphene
from graphene_django import DjangoObjectType
from .models import Level


class LevelType(DjangoObjectType):
    """Level type class"""
    class Meta:
        """model mapping to Level ORM class"""
        model = Level


class Query(graphene.ObjectType):
    """Levels query class"""
    levels = graphene.List(LevelType)

    def resolve_levels(self, info):
        """resolver function for levels query"""
        return Level.objects.all()
