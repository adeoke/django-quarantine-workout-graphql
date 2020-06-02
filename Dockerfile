FROM python:3.6-alpine
MAINTAINER A Tester

# make port 8000 available from this container.
EXPOSE 8000

RUN mkdir /djangoapi

#change to the djangoapi dir
WORKDIR /djangoapi

#copy all content from host directory to image directory.
COPY . /djangoapi/

# Set environment variables
ENV PYTHONUNBUFFERED 1

# execute immediately
RUN apk update \
    && apk add openssh-server \
    && apk add --virtual build-deps gcc musl-dev \
    && apk add jpeg-dev zlib-dev libjpeg \
    && pip3 install pipenv \
    && pipenv install -r requirements.txt --deploy --ignore-pipfile \
    && apk del build-deps

# commonly used variables
ARG app_name='quarantineworkout'

# set migrations based on models for app.
RUN pipenv run python3 $app_name/manage.py makemigrations

# create the db and tables based on models for the app (migrations).
RUN pipenv run python3 $app_name/manage.py migrate

# Load data into sqlite3 db in certain order.
RUN pipenv run python3 $app_name/manage.py loaddata $PWD/$app_name/stars/fixtures/seed.yaml
RUN pipenv run python3 $app_name/manage.py loaddata $PWD/$app_name/bodyparts/fixtures/seed.yaml
RUN pipenv run python3 $app_name/manage.py loaddata $PWD/$app_name/users/fixtures/seed.yaml
RUN pipenv run python3 $app_name/manage.py loaddata $PWD/$app_name/levels/fixtures/seed.yaml
RUN pipenv run python3 $app_name/manage.py loaddata $PWD/$app_name/equipment/fixtures/seed.yaml
RUN pipenv run python3 $app_name/manage.py loaddata $PWD/$app_name/exercises/fixtures/seed.yaml
RUN pipenv run python3 $app_name/manage.py loaddata $PWD/$app_name/reviews/fixtures/seed.yaml
