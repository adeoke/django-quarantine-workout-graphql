# Quarantine Workout

An approach to testing GraphQL API's in Python (version 3.6), utilising Pipenv.

# Motivation

This project was inspired by the need to keep fit during a quarantine. The intention
is given a pool of exercises a user can provide their exercise requirements and obtain 
a workout tailored to those requirements.

# Screenshot

![workout query](/images/workout_query.gif)

The following libraries are used to both develop and test the application:

```shell script
graphene # The actual library used to build GraphQL API's, there are others, but I like this one.

graphene-django # Abstraction layer on top of Graphene, with the intention of simplyfying GraphQL functionality.

python-graphql-client # GraphQL client for programmatic requests.

invoke # Task runner.

django # Web framework support.

django-graphql-jwt # For JWT tokens.

gql-query-builder # GraphQL query builder.

PyYAML # To parse yaml files.

jsonpath-ng # To parse json strings.

django-cors-headers # Allowing resources to be accessed on other domains.

Faker # For generating random test data.

snapshottest # To run tests against the snapshot (recorded) responses.
```

# Setup Instructions

## Setup with Docker

You will need to have both docker and docker-compose installed.
Provided you do, then navigate to the project root, launch the terminal and input:

```text
$ docker-compose up
```

This will setup and install all the dependencies for the application and start the server on `localhost:8000`.
You can view GraphiQL now in the browser by going to `http://localhost:8000/graphql/`

## Setup locally

You will need to create a virtual environment. In this project I have used `Pipenv`.
To install Pipenv see the instructions here:

```http request
https://pypi.org/project/pipenv/
```

Once installed, launch the terminal (if its not already open), navigate to the project root 
and input `pipenv shell` to change into the virtual environment.

To verify that you are in the pipenv shell environment you should see something similar to the following:

```shell script
$ (djangoapi) user-machine:djangoapi myuser$ 
``` 

In the project root install the dependencies in your environment with the following pipenv command:

```shell script
$ pipenv install -r requirements.txt
```

The installation will install a couple of command line tools. 
You can verify that they are installed by running the following commands on command line:

```shell script
$ django-admin --version
> 3.0.6

$ invoke --version
> 1.4.1
```

*NB: It is also possible to use `invoke` with the shortened word `inv`, so from here on I will refer to the short form name for the task manager.*

# The invoke task manager

Invoke is used for simplifying repetitive tasks run locally on the host machine.

If you are unfamiliar with invoke then please see basic usage here:

```http request
http://docs.pyinvoke.org/en/stable/getting-started.html
```

You can get a list of all the tasks with the command:

```shell script
$ inv -l

> # produces output...

delete-all-migrations         Delete all migration files for all Django apps.
delete-db-from-project-root   Deletes the db with name db from the project root. Default db 'db.sqlite3'.
load-all-data                 Loads seed data for all fixtures directory for all applications.
load-app-data                 Load app data for app supplied by app arg.
make-migrations               Make migrations based on app models for all Django apps in project.
make-migrations-and-migrate   Perform both making migrations for all apps and then migrating them, again for all apps.
migrate                       Migrate the migration files for all the apps in the Django project.
run-all-tests                 Run all tests within the djangoapi/tests directory using unittest test runner.
run-server                    Start the django server on default port 8000, unless another port specified.
```

# Starting the server locally

The application should now be all set up and ready to use. 
Finally, to test your configuration start the Django server (the default port is 8000), with by running:

```shell script
$ inv run-server
```

This will start the server on `localhost:8000` (if you wish to change the default port run the task instead with 
command `inv run-server --port=MY_PORT_HERE`).

Replacing the port with the port of your choice. Note that regardless of the port that you choose, the process will
now run in the terminal window until you end the server by issuing a `control AND c` to cancel the process. So it is *advisable*
to start a new terminal on the project root and ensure that you change into the same environment with the command `pipenv shell` again.

In your browser you can now visit the url `http://localhost:8000/graphql/` to view the GraphiQL editor:

![](/images/graphiql_localhost.png)

# Running the tests locally

A good place to start to make sure that the application is up and running is to run the end to end and snapshot tests.
Again, go to the project root in the terminal change to the pipenv environment (`pipenv shell`) and input: 

```shell script
$ inv run-all-tests
```

*NB: If it wasn't already obvious, the tests will **NOT** run within the browser session. Instead the tests use a client to make the API requests.* 

# Running the tests on the container

If for whatever reason, be it you do not want to install Python locally, or do not want to install pipenv locally then you can also run the tests on the container directly.
To do so ensure that you already have the container running (if you dont then type `docker-compose up` from the project root). In another terminal window, again from the project root
input the following:

```shell script
$ docker ps -a # To get the list of running containers. Get the container name or id that is returned in the output from the command.
```

You should see output similar to the following:

```text
    CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
**377e4cafe15c**        djangoapi_app       "sh -c 'pipenv run p…"   22 seconds ago      Up 22 seconds       0.0.0.0:8000->8000/tcp   **djangoapi_app_1**
```
to connect to execute commands on the running container type in the terminal:

```shell script
$ docker exec -it <CONTAINER_NAME_OR_ID> /bin/sh
```

Which will place you in the containers shell. 
Once connected you need to change into the pipenv virtual environment. You can do this by typing:

```shell script
$ pipenv shell
```

The output of which should be similar to the following:

```text
Launching subshell in virtual environment…
/djangoapi #  . /root/.local/share/virtualenvs/djangoapi-RQslU66b/bin/activate
```

You are now at the point where you can run the tests. Unfortunately, without additional apk packages you cannot run the invoke task (bash is **NOT** installed on alpine).
So instead run the tests directly using unittest.


To exit from the virtual environment type `exit`. Which takes you back to the terminal, still on the container. 
Type `exit` to return to the terminal on your host machine. 

```shell script
$ python3 -m unittest tests/**/*.py
```

Which will run all the tests. If the tests run successfully then you should see output similar to the following:

```text
........
----------------------------------------------------------------------
Ran 8 tests in 0.710s

OK
```

# Example of how to perform a query

If you are familiar with GraphQL then you ignore this section.

For newcomers to GraphQL it is advisable to do some research into how to perform queries.
See the following for a quick guide:

```http request
https://graphql.org/learn/queries/
```

Failing that for whatever reason I shall provide a couple of *quick* examples of how to interact with this API using GraphQL 
queries.

It's also good to note that query requests are *idempotent*, in that performing the same request over and over will not 
create a different side effect (you can also think of this is a request that will not change the state of a resource).

There are a number of models that have direct access to them via resolvers in this API.
This includes:
    
```http request
bodyparts
equipment
exercises
levels
reviews
stars
users
```

Let us use `users` to perform queries against. Before we delve into performing the query it is a good point to note that the user
model has a number of fields available to it. This includes, but is not limited to the following:

```text
email
username
password (this is a hashed value)
...
date_joined
```

There's actually loads more, not all of which are actually required or return any meaningful information for the purposes of this application.
However, I decided to keep them in to illustrate a point. A query is going to expose the data from the backend, unless there is some logic that says to either 
only `include` the following fields, or to `exclude` the following fields (typically defined by a list of what to either include or exclude in the graphql output).
With that being said I seeded the database with a few users. The users email address and username's were defined (representation of details follows):

```text
user_1:
    username: testertest90
    email: testertesting1@example.com
user_2:
    username: newtestertest
    email: testertesting2@example.com
```

So with that being said if we now launch the GraphiQL web client and make a query to get all users, and return each users email address and username, then
we should see at least the 2 users that we created returned in the response data. What follows is the request and response for that that request.

![](/images/users_query_response.png)

We can see that the response data contains the exact fields that we requested as a json response in the shape of the request that we made.

# Example of how to perform a mutation

Skip this section if you are familiar with GraphQL.

Mutations represent what would typically be performed by a POST/PUT/DELETE request in a Rest API (non idempotent requests). The following example shows how to create a user and the
response data returned shows the fields that we requested to be returned from the result of issuing that request.

![](/images/create_mutation_response.png)

So, to create the user we first provided the arguments for email, password and username:

```text
createUser(email: "test@example.com",
  					password: "password1234",
  					username: "testuser")
```

We also indicated that we want the response to contain the users username, email and dateJoined properties:

```text
user{
      username
      email
      dateJoined
    }
``` 

This resulted in the response:

```text
{
  "data": {
    "createUser": {
      "user": {
        "username": "testuser",
        "email": "test@example.com",
        "dateJoined": "2020-06-02T00:35:47.860278+00:00"
      }
    }
  }
}
```

# High level acceptance criteria

In order to flesh out the functionality of the API I used the following criteria (you can assume your 
own implied criteria from the ones listed here).

1. Any user is able to retrieve all workouts.
2. A workout is a collection of exercises that match the filtered criteria.
3. Performing a workout query request, without any filtering returns all the exercises in the response data.
5. Only an authenticated user can create an exercise.
6. Only an authenticated user can create a review.
7. Performing a query request to levels returns all levels (provided a sub field is specified).
8. Performing a query request to bodyparts returns all the body parts.
9. Performing a query request to equipment returns all the equipment types.
9. Performing a query request to reviews returns all the reviews.
10. Performing a query request to stars returns all the stars types.
11. Performing a query request to users returns all the users.
12. Any mutation that requires a field should not be persisted without that field being supplied.

# Anatomy of an end to end test

A GraphQL test includes the following:

```shell script
A client # which makes the GraphQL request.
A query # be it both mutation and query are queries. In essense what you send in the request is the query.
A JSON response data object # which is parsed with jsonpath in the tests.
```

You have the option of supplying a raw string as the query in a test, however, all the tests used in this project use a query builder to
generate the queries.

A GraphQL client takes in a query and/or variables as arguments and returns the response data.
JSONPath is then used to parse the response for specific data.

Here is an example:

```python
    def test_should_get_body_parts(self):
        expected_body_parts = ['upper body', 'lower body', 'cardio']

        query = GqlQuery().fields(['name']).query(
            'bodyParts').operation().generate()
        data = self.client.execute(query=query)

        jsonpath_expr = parse('data.bodyParts[*].name')
        actual_body_parts = [match.value for match in jsonpath_expr.find(data)]

        self.assertEqual(sorted(actual_body_parts),
                         sorted(expected_body_parts),
                         'expected body parts to be the same, but were not')
```

Use the following resources as guides if you need more information:

> GraphQL client guide:

```http request
https://github.com/prodigyeducation/python-graphql-client
```

> Query building guide:

```http request
https://github.com/youyo/gql-query-builder
```
> JSONPath guide:

```http request
https://restfulapi.net/json-jsonpath/
```

# Anatomy of a snapshot test

Snapshottest is useful for replaying tests that will yield the same result.
Snapshot test records the response from a request and uses that response to compare all subsequent tests against.

See an example from the tests within the project following:

```python
 def test_equipment_against_snapshot(self):
        """Testing equipment response data"""
        query = GqlQuery().fields(['difficulty']).query(
            'levels').operation().generate()

        equipment_resp = self.client.execute(query=query)
        self.assertMatchSnapshot(equipment_resp, 'equipment_snapshot_resp')
```

A directory is created listing all the snapshots. On subsequent requests the resposes will be checked against these response.

# Suggested Improvements

1) Only return all user information for the currently authenticated user.
At present the currently logged in user, or unauthenticated user will retrieve all 
user data in the response data. An improvement would be hide the sensitive data for all users other than the 
currently authenticated user.
2) Add rate limiting.
3) Use relay for pagination.
4) Use logging.
5) IP whitelisting.

See here for more on some of the suggested improvements:

```http request
https://blog.papertrailapp.com/common-api-vulnerabilities-and-how-to-secure-them/
```

## License

[MIT License](https://github.com/adeoke/django-quarantine-workout-graphql/blob/master/LICENSE)
