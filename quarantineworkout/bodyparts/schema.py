import graphene
from graphene_django import DjangoObjectType

from .models import BodyPart


class BodyPartType(DjangoObjectType):
    class Meta:
        model = BodyPart


class Query(graphene.ObjectType):
    body_parts = graphene.List(BodyPartType)

    def resolve_body_parts(self, info):
        return BodyPart.objects.all()
