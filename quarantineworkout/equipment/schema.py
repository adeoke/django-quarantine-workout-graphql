"""equipment schema module"""
import graphene
from graphene_django import DjangoObjectType
from .models import Equipment


class EquipmentType(DjangoObjectType):
    """Equipment class type"""
    class Meta:
        """model mapping to Equipment orm class"""
        model = Equipment


class Query(graphene.ObjectType):
    """Equipment query class"""
    equipment = graphene.List(EquipmentType)

    def resolve_equipment(self, info):
        """equipment query resolver"""
        return Equipment.objects.all()
