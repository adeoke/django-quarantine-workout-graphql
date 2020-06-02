"""bodyparts schema module"""

import graphene
from graphene_django import DjangoObjectType

from .models import BodyPart


class BodyPartType(DjangoObjectType):
    """bodypart type"""
    class Meta:
        """model mapping to bodypart model"""
        model = BodyPart


class Query(graphene.ObjectType):
    """bodypart query class"""
    body_parts = graphene.List(BodyPartType)

    def resolve_body_parts(self, info):
        """bodyparts resolver method"""
        return BodyPart.objects.all()
