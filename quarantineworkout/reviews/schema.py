import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from .models import Review
from exercises.models import Exercise
from exercises.schema import ExerciseType
from stars.models import Star
from stars.schema import StarType


class ReviewType(DjangoObjectType):
    class Meta:
        model = Review


class Query(graphene.ObjectType):
    reviews = graphene.List(ReviewType)

    def resolve_reviews(self, info):
        return Review.objects.all()


class CreateReview(graphene.Mutation):
    exercise = graphene.Field(ExerciseType)
    star = graphene.Field(StarType)

    class Arguments:
        exercise_id = graphene.Int(required=True)
        star_review = graphene.Int(required=True)

    def mutate(self, info, exercise_id, star_review):
        user = info.context.user

        # unable to create a review unless you are authenticated
        if user.is_anonymous:
            raise GraphQLError('You must be logged in to Post a review!')

        exercise = Exercise.objects.filter(id=exercise_id).first()
        if not exercise:
            raise GraphQLError('Invalid Exercise!')

        star = Star.objects.filter(number=star_review).first()

        if not star:
            raise GraphQLError('Invalid star review!')

        review = Review(
            user=user,
            exercise=exercise,
            star=star,
        )

        review.save()

        return CreateReview(exercise=review.exercise,
                            star=review.star)


class Mutation(graphene.ObjectType):
    create_review = CreateReview.Field()
