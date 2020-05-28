import graphene
from exercises.schema import ExerciseType
from exercises.models import Exercise


class Query(graphene.ObjectType):
    workout = graphene.List(ExerciseType,
                            body_part=graphene.String(),
                            name=graphene.String(),
                            equipment=graphene.String(),
                            level=graphene.String())

    def resolve_workout(self, info, **kwargs):
        all_exercises = Exercise.objects

        if kwargs.get('body_part'):
            all_exercises = all_exercises.select_related('body_part').filter(
                body_part__name=kwargs.get('body_part').lower())

        if kwargs.get('level'):
            all_exercises = all_exercises.select_related('level').filter(
                level__difficulty=kwargs.get('level').lower())

        if kwargs.get('name'):
            all_exercises = all_exercises.filter(
                name__icontains=kwargs.get('name').lower())

        if kwargs.get('equipment'):
            all_exercises = all_exercises.select_related('equipment').filter(
                equipment__name=kwargs.get('equipment').lower())

        return all_exercises
