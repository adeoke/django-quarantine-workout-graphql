# Quarantine Workout


An approach to testing GraphQL API's in Python 3.6, utilising Pipenv.

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

**Remove/UPDATE**
2) Only a logged in user can create an exercise.
3) Only a logged in user can give a workout a review (where ONE is poor upto a review of FIVE, which represents a perfect exercise, only five choices,
ONE to FIVE, inclusive are permitted).
4) Any user can obtain all the reviews for a workout.
5) Only return the email address and username when querying all reviews, if you are the user who made that review.
All other reviews posted from other users should not include the username or email address.
6) Only a user with admin access can get all user details from a query to users.
7) Only a users username is returned when an authenticated user makes a request to query Users.


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

# Task manager
I have used `invoke` for tasks when running locally, but can also be used on a container itself.

If you are unfamiliar with invoke see basic usage here:

```http request
http://docs.pyinvoke.org/en/stable/getting-started.html
```

Purely for my convenience I have added a couple of tasks to speed up my development and testing.
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

The application should now be all set up and ready to use. Finally, to test your configuration start the Django server
(the default port is 8000), with by running:

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
To do so ensure that you already have the container running (if you dont then type `docker-compose up` from the project root). In another terminal wiindow, again from the project root
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

You are now at the point where you can run the tests. Unfortunetely, without additional apk packages you cannot run the invoke task (bash is **NOT** installed on alpine).
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

# Example of how to perform a query

If you are familiar with graphql then you ignore this section.
If you are new to graphql it is advisable to do some research into how to perform queries.
Failing that for whatever reason I shall provide a couple of quick examples of how to interact with the API using graphql 
queries.

TODO

# Example of how to perform a mutation

TODO

# High level acceptance criteria

In order to flesh out the functionality of the api I have followed these criteria (you can assume your 
own implied criteria from the ones listed here).

1. Any user is able to retrieve all workouts.
2. A workout is a collection of exercises that match a given criteria (by filtering).
3. If no filter is specified when making a request for a workout then all exercises are returned.
4. Filtering on a workout should only return exercises that match the filter criteria.
5. TODO complete 



# Anatomy of an end to end test

TODO

> query building help:

> client info

```http request
https://stackoverflow.com/questions/48693825/making-a-graphql-mutation-from-my-python-code-getting-error
```

> builder

```http request
https://gist.github.com/gbaman/b3137e18c739e0cf98539bf4ec4366ad
```


# Anatomy of a snapshot test

TODO


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

To exit from the virtual environment type `exit`. Which takes you back to the terminal, still on the container. 
Type `exit` to return to the terminal on your host machine. 

## License

[MIT License](https://github.com/adeoke/django-quarantine-workout-graphql/blob/master/LICENSE)
