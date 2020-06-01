from invoke import task
import os

current_dir = os.path.dirname(__file__)
django_project_root = os.path.join(current_dir, "quarantineworkout")


@task(optional=['port'], help={'port': "port to start the Django server on"})
def run_server(c, port=None):
    """
    Start the django server on default port 8000, unless another port specified.

    :param c: Context object
    :param port: Optional port. Default port is 8000 (Django default is 8000).
    :return: None
    """
    run_server_cmd = 'python quarantineworkout/manage.py runserver'
    if port:
        run_server_cmd = '{} {}'.format(run_server_cmd, port)
    c.run(run_server_cmd)


@task
def make_migrations(c):
    """
    Make migrations based on app models for all Django apps in project.

    :param c: context object
    :return: None
    """
    c.run('python quarantineworkout/manage.py makemigrations')


@task
def migrate(c):
    """
    Migrate the migration files for all the apps in the Django project.

    :param c: Context object
    :return: None
    """
    c.run('python quarantineworkout/manage.py migrate')


@task(post=[make_migrations, migrate])
def make_migrations_and_migrate(_c):
    """
    Perform both making migrations for all apps and then migrating them, again for all apps.

    :param _c: unused, but required context object.
    :return: None
    """
    print("Make migrations for all apps, then migrate.")


@task
def run_all_tests(c):
    """
    Run all tests within the djangoapi/tests directory.

    :param c: Context object
    :return: None
    """
    c.run("python -m unittest tests/**/*.py")


@task(optional=['app'], help={'app': "App name to load data for."})
def load_app_data(c, app=None):
    """
    Load app data for app supplied by app arg.

    :param c: Context object
    :param app: Optional argument app. Supply for loading data for certain app.
    :return: None.
    """
    if app:
        path = '{}/{}/fixtures/seed.yaml'.format(django_project_root, app)
        c.run('python quarantineworkout/manage.py loaddata {}'.format(path))
    else:
        print("no app chosen to loaddata from")


@task
def delete_all_migrations(c):
    """
    Delete all migration files for all Django apps.

    :param c: Context object.
    :return: None
    """
    cmd_one = 'find . -path "*/migrations/*.py" -not -name "__init__.py" -delete'
    cmd_two = 'find . -path "*/migrations/*.pyc"  -delete'
    c.run('{};{}'.format(cmd_one, cmd_two))


@task
def delete_db_from_project_root(c, db_name='db.sqlite3'):
    """
    Deletes the db with name db from the project root. Default db 'db.sqlite3'.

    :param c: Context object.
    :param db_name: remove db name from Django project root (quarantineworkout).
    :return:
    """
    print('deleting db: {}'.format(db_name))
    c.run('rm {}/{}'.format(django_project_root, db_name))


@task
def load_all_data(c):
    """
    Loads seed data for all fixtures directory for all applications.

    :param c: Context object
    :return: None
    """

    fixtures = []
    for root, directory, filename in os.walk('quarantineworkout'):
        if 'seed.yaml' in filename:
            fixtures.append('{}/{}'.format(os.path.abspath(root), filename[0]))

    # exercises then reviews need to be the last tables seeded.
    for index in range(len(fixtures)):
        if 'reviews' in fixtures[index] and fixtures[index] != fixtures[-1]:
            fixtures[index], fixtures[-1] = fixtures[-1], fixtures[index]
        if 'exercises' in fixtures[index] and fixtures[index] != fixtures[-2]:
            fixtures[index], fixtures[-2] = fixtures[-2], fixtures[index]

    for fixture in fixtures:
        print('\nloading fixture {}'.format(fixture))
        c.run('python {}/manage.py loaddata {}'.format(django_project_root,
                                                       fixture))
