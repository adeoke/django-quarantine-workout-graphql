import graphene
from graphene_django import DjangoObjectType
from .models import Equipment


class EquipmentType(DjangoObjectType):
    class Meta:
        model = Equipment


class Query(graphene.ObjectType):
    equipment = graphene.List(EquipmentType)

    def resolve_equipment(self, info):
        return Equipment.objects.all()
