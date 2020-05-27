# Quarantine Workout

An approach to testing GraphQL API's in Python 3.6, utilising Pipenv.

The following libraries are used to both develop and test the application:

```
graphene #=> The actual library used to build GraphQL API's, there are others, but I like this one.

graphene-django #=> Abstraction layer on top of Graphene, with the intention of simplyfying GraphQL functionality.

python-graphql-client #=> GraphQL client for programmatic requests.

invoke #=> Task runner.

django #=> Not really required, butI may add functionality to make a full blown web app.

django-graphql-jwt #=> For JWT tokens.

gql-query-builder #=> GraphQL query builder.

PyYAML #=> To parse yaml files.

jsonpath-ng #=> To parse json strings.
```

# Installation:

It is assumed that you have Pipenv installed. If not then see the installation 
instructions here:

```
https://pypi.org/project/pipenv/
```

Once Pipenv is installed, input the following on the command line from the project root:
```
pipenv install -r requirements.txt
```

If you choose to not install Pipenv, then technically that should also be okay.
You should be able to install the dependencies using Pip for example, but I have not tried
so feel free to give it a go if you want.

NB: before starting the application, I have included some data to seed the database to ensure that 
when testing is performed there is data to work with. You can seed the data with the invoke task:

```python
invoke seed-all-data
```

Note that omitting this step will still start the application, but you will need to create your own initial data
via mutations to enable any querying of the service.

You are now ready to start the application. Start the service by launching the django server with invoke command:

```
invoke run-server
```

Which will start the django app on localhost port 8000. Note also that the terminal instance that this service 
is running on is no longer usable and logging will only be displayed from there onwards. You will need to open a new terminal window
to perform any other action.

NB: It should also be noted that you can change he port that the server starts on if you do not want to start on port 8000.
For example the following command will start the django server on port 8900:

```python
invoke run-server --port=8900
```


In the new terminnal window you can now run all the tests against the live application with command:

```python
invoke run-all-tests
```

Which will run the tests against the live service and not the tests against the mocks.

# High level acceptance criteria

In order to flesh out the functionality of the api Ihave followed these criteria (you can assume your 
own implied criteria from the ones listed here).

1) Any user is able to retrieve all workouts.
2) Only a logged in user can create a workout.
3) Only a logged in user can give a workout a review (where ONE is poor upto a review of FIVE, which represents a perfect exercise, only five choices,
ONE to FIVE, inclusive are permitted).
4) Any user can obtain all the reviews for a workout.
5) Only return the email address and username when querying all reviews, if you are the user who made that review.
All other reviews posted from other users should not include the username or email address.
6) Only a user with admin access can get all user details from a query to users.
7) Only a users username is returned when an authenticated user makes a request to query Users.


#TODO provide tests against mocks.

#some points to consider:
ip whitelisting
rate limiting
access logs

see here for more on the topic:
https://blog.papertrailapp.com/common-api-vulnerabilities-and-how-to-secure-them/

TODO: Seed user, invoke task to completely wipe db, another task to setup db and 
load data for the various app models, ready for e2e testing again.