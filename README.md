# Quarantine Workout

An approach to testing GraphQL API's in Python (version 3.6), utilising Pipenv.

# Motivation

This project was inspired by the need to keep fit during a quarantine. Given
a pool of exercises a user can provide their workout criteria and obtain 
a tailored set of exercises that matches those conditions.

# Demo

![workout query](/images/workout_query.gif)

# Tech/Libraries Used

* [graphene](https://github.com/graphql-python/graphene)
Used to build GraphQL API.

* [graphene-django](https://graphene-python.org/)
Abstraction layer on top of Graphene, with the intention of simplyfying GraphQL functionality.

* [python-graphql-client](https://github.com/prodigyeducation/python-graphql-client)
GraphQL client for programmatic requests.

* [invoke](http://www.pyinvoke.org/)
Task runner.

* [django](https://www.djangoproject.com/)
Web framework support.

* [django-graphql-jwt](https://django-graphql-jwt.domake.io/en/latest/)
For JWT tokens.

* [gql-query-builder](https://github.com/youyo/gql-query-builder)
GraphQL query builder.

* [PyYAML](https://github.com/yaml/pyyaml)
Yaml parser.

* [jsonpath-ng](https://github.com/h2non/jsonpath-ng)
JSON parser.

* [django-cors-headers](https://github.com/adamchainz/django-cors-headers)
Allowing resources to be accessed on other domains.

* [Faker](https://faker.readthedocs.io/en/master/)
For generating random test data.

* [snapshottest](https://pypi.org/project/snapshottest/)
Run tests against the snapshot (recorded) responses.

# Setup Instructions:

## Setup with Docker

**Note you will need to have both `docker` and `docker compose` installed.**

1. Launch terminal at project root
2. Input the following to start the container:

```text
$ docker-compose up
```

- Once the installation process completes you will be able to navigate to `http://localhost:8000/graphql/`
to see the GraphiQL web browser interface.

## Setup locally

If you do not have Python installed, check the installation instructions for your platform
here:

```http request
https://www.python.org/downloads/`
```

**Note that this project was built with Python 3.6 in mind.**

Once installed verify the installation on the terminal by typing:

```shell script
$ python --version # Python 3.6
```

**You will need to create a virtual environment.**

- This project uses `Pipenv` for the virtual environment.
    - If you do not already have Pipenv installed see the following link for a guide:
    
    ```http request
    https://pypi.org/project/pipenv/
    ```
  
After successfully installing Pipenv you are required to change into the pipenv virtual environment.

- In the project root input:

```shell script
$ pipenv shell
```

You should now be in the virtual environment and you will similar output to the following:

```shell script
$ (djangoapi) user-machine:djangoapi myuser$ 
``` 

Time to install the dependencies into the virtual environment.

- In the project root on the terminal input:
 
```shell script
$ pipenv install -r requirements.txt
```

To verify all tools are correctly installed you can type into the terminal:

```shell script
$ invoke --version 
# output should be 1.4.1
```

# The invoke task manager

Invoke is used for simplifying repetitive tasks run locally on the host machine.

If you are unfamiliar with invoke then please see basic usage here:

```http request
http://docs.pyinvoke.org/en/stable/getting-started.html
```

You can get a list of all the tasks from the project root by typing into the terminal:

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

It is assumed that you have all the dependencies installed locally at this point. If not then read
[Setup Locally](#setup-locally) to do so.

- In a terminal go to the project root start and the server with command:

```shell script
$ inv run-server
```

This will start the server on `localhost:8000` (if you wish to change the default port run the task instead with 
command `inv run-server --port=MY_PORT_HERE`) replacing the port with the port of your choice. 

**The server will continue to run until you input key combination `CONTROL AND c`. Also its good to note that the process will 
run in the terminal until its stopped. For that reason I recommend opening another terminal window at the project root for further commands.**

You can now view the GraphiQL web browser interface by going to url `http://localhost:8000/graphql/`.

See screenshot below for an example output:

![](/images/graphiql_localhost.png)

# Running the tests locally

Now  the application running you can now run tests against it.

Ensure that you are in the project root and within the virtual environment
(open the terminal at the project root and input `pipenv shell`).

Run all tests with command:

```shell script
$ inv run-all-tests
```

*NB: If it wasn't already obvious, the tests will **NOT** run within the browser session. Instead the tests use a client to make the API requests.* 

# Running the tests on the container

You can also run the tests directly on the container.
Wou will need to ensure that you have the container already up and running.

- On the terminal get a list of all the running containers:

```shell script
$ docker ps -a # To get the list of running containers. Get the container name or id that is returned in the output from the command.
```

You should see output similar to the following:

```text
    CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
**377e4cafe15c**        djangoapi_app       "sh -c 'pipenv run p…"   22 seconds ago      Up 22 seconds       0.0.0.0:8000->8000/tcp   **djangoapi_app_1**
```

- To connect to execute commands on the running container type in the terminal:

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

You are now at the point where you can run the tests. Unfortunately, without additional apk packages you cannot run invoke tasks (bash is **NOT** installed on alpine).
So instead run the tests directly using unittest.

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

To exit from the virtual environment type `exit`. Which takes you back to the terminal, still on the container. 
Type `exit` to return to the terminal on your host machine. 

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

Exposed graphene/graphql types include:
    
```text
bodyparts
equipment
exercises
levels
reviews
stars
users
```

Let us examine `users` to perform queries against, but before we do its a good point to note that the user
model has a number of subfields available on it. This includes, but is not limited to the following:

```text
email
username
password
...
date_joined
```

There is no filtering applied to what subfields are returned from the users query (all of the default
user fields are available options to retrieve)  .

On initialisation of the project I seeded the database with 2 users, each with a username, password and email address.
See an example representation below:

```text
user_1:
    username: testertest90
    email: testertesting1@example.com
user_2:
    username: newtestertest
    email: testertesting2@example.com
```

If we perform a query for `users` with subfields `email` and `username` we will see the details for the users returned
in the response data set. See the example request and response following:

![](/images/users_query_response.png)

We can see that the JSON response data contains the exact fields that we requested, only this time with the values populated.

# Example of how to perform a mutation

Skip this section if you are familiar with GraphQL.

Mutations represent what would typically be performed by a POST/PUT/DELETE request in a Rest API (non idempotent requests).

We will look at how to create a user. See screenshot for an example:

![](/images/create_user_mutation_response.png)

In this example we provided arguments for `email`, `password` and `username` to `createUser`:

```text
createUser(email: "test@example.com",
  					password: "password1234",
  					username: "testuser")
```

We also requested that the subfields we want in the response should contain the users `username`, `email` and `dateJoined` properties:

```text
user{
      username
      email
      dateJoined
    }
``` 

Initiating this request we see the following response data:

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
