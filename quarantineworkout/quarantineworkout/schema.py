"""Application schema module"""
import graphene
import graphql_jwt
import bodyparts.schema
import exercises.schema
import equipment.schema
import reviews.schema
import stars.schema
import levels.schema
import users.schema
import workout.schema


class Query(workout.schema.Query, users.schema.Query,
            reviews.schema.Query,
            stars.schema.Query,
            exercises.schema.Query,
            bodyparts.schema.Query,
            equipment.schema.Query,
            levels.schema.Query, graphene.ObjectType):
    """Root query class"""


class Mutation(users.schema.Mutation,
               reviews.schema.Mutation,
               exercises.schema.Mutation,
               graphene.ObjectType):
    """Root Mutation class"""
    # if user details correct then provide a JWT token.
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    # to verify the token from token_auth we use verify token
    verify_token = graphql_jwt.Verify.Field()
    # refreshToken to obtain a brand new token with renewed expiration time
    refresh_token = graphql_jwt.Refresh.Field()


# Root schema
schema = graphene.Schema(query=Query, mutation=Mutation)
