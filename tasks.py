from invoke import task
import os

current_dir = os.path.dirname(__file__)
django_project_root = os.path.join(current_dir, "quarantineworkout")


@task(optional=['port'])
def run_server(c, port=None):
    run_server_cmd = 'python manage.py runserver'
    if port:
        run_server_cmd = '{} {}'.format(run_server_cmd, port)
    c.run(run_server_cmd)


@task
def make_migrations(c):
    c.run('python quarantineworkout/manage.py makemigrations')


@task
def migrate(c):
    c.run('python quarantineworkout/manage.py migrate')


@task(post=[make_migrations, migrate])
def make_migrations_and_migrate(_c):
    print("Make migrations for all apps, then migrate.")


@task
def run_all_tests(c):
    c.run("python -m unittest tests/**/*.py")


@task(optional=['app'])
def load_app_data(c, app=None):
    if app:
        path = '{}/{}/fixtures/seed.yaml'.format(django_project_root, app)
        c.run('python manage.py loaddata {}'.format(path))
    else:
        print("no app chosen to loaddata from")


@task
def delete_all_migrations(c):
    cmd_one = 'find . -path "*/migrations/*.py" -not -name "__init__.py" -delete'
    cmd_two = 'find . -path "*/migrations/*.pyc"  -delete'
    c.run('{};{}'.format(cmd_one, cmd_two))


@task
def delete_db_from_project_root(c, db_name='db.sqlite3'):
    print('deleting db: {}'.format(db_name))
    c.run('rm {}/{}'.format(django_project_root, db_name))


@task
def load_all_data(c, pty=False):
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
        print('\nloading fixture'.format(fixture))
        c.run('python {}/manage.py loaddata {}'.format(django_project_root,
                                                       fixture), pty=pty)
