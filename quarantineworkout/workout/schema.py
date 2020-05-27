import graphene

from exercises.schema import ExerciseType
from exercises.models import Exercise


class Query(graphene.ObjectType):
    workouts = graphene.List(ExerciseType)

    def resolve_workouts(self, info):
        # just a test, then comes the logic and filtering
        return Exercise.objects.all()