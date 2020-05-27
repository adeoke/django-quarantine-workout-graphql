import graphene
from django.db.models import Q
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from .models import Exercise
from bodyparts.models import BodyPart
from bodyparts.schema import BodyPartType
from equipment.models import Equipment
from levels.models import Level
from users.schema import UserType


class ExerciseType(DjangoObjectType):
    class Meta:
        model = Exercise


class Query(graphene.ObjectType):
    exercises = graphene.List(ExerciseType, search=graphene.Int())

    def resolve_exercises(self, info, search=None):
        all_exercises = Exercise.objects.all()

        if search:
            all_exercises = all_exercises.filter(id=search)

        return all_exercises


class CreateExercise(graphene.Mutation):
    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()
    body_part = graphene.String()
    name = graphene.String()
    equipment = graphene.String()
    level = graphene.String()
    # now returning the user that made the request to create the exercise.
    posted_by = graphene.Field(UserType)

    class Arguments:
        url = graphene.String(required=True)
        description = graphene.String()
        name = graphene.String(required=True)
        body_part = graphene.String(required=True)
        equipment = graphene.String(required=True)
        level = graphene.String(required=True)

    def mutate(self, info, **kwargs):
        level = kwargs.get('level').lower()
        body_part = kwargs.get('body_part').lower()
        equipment = kwargs.get('equipment').lower()

        user = info.context.user

        # unable to post an exercise unless you are authenticated.
        if user.is_anonymous:
            raise GraphQLError('You must be logged in post an Exercise!')

        body_part_type = BodyPart.objects.filter(
            name=body_part).first()

        if not body_part_type:
            raise GraphQLError(
                'No body part with name {}'.format(body_part))

        equipment_type = Equipment.objects.filter(
            name=equipment).first()

        if not equipment_type:
            raise GraphQLError(
                'No equipment with name {}'.format(equipment))

        level_type = Level.objects.filter(
            difficulty=level).first()

        if not level_type:
            raise GraphQLError(
                'No Level matching level {}'.format(level))

        exercise = Exercise(url=kwargs.get('url'),
                            description=kwargs.get('description'),
                            name=kwargs.get('name'),
                            body_part=body_part_type,
                            equipment=equipment_type,
                            posted_by=user,
                            level=level_type)
        exercise.save()

        return CreateExercise(
            id=exercise.id,
            description=exercise.description,
            url=exercise.url,
            name=exercise.name,
            equipment=exercise.equipment,
            body_part=exercise.body_part,
            level=exercise.level,
            posted_by=exercise.posted_by
        )


class Mutation(graphene.ObjectType):
    create_exercise = CreateExercise.Field()
