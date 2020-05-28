FROM python:3.6-alpine
MAINTAINER A Tester

EXPOSE 8000 8000

RUN mkdir /djangoapi

#change to the djangoapi dir
WORKDIR /djangoapi

#copy all content from host directory to image directory.
ADD . /djangoapi/

# Set environment variables
ENV PYTHONUNBUFFERED 1

RUN apk update
RUN apk add openssh-server
RUN apk add --virtual build-deps gcc musl-dev \
    && apk add jpeg-dev zlib-dev libjpeg \
    && pip install pipenv \
    && pipenv install -r requirements.txt --skip-lock --dev \
    && apk del build-deps

CMD ["pipenv", "run", "python3", "quarantineworkout/manage.py", "makemigrations"]
CMD ["pipenv", "run", "python3", "quarantineworkout/manage.py", "migrate"]
CMD ["pipenv", "run", "python3", "quarantineworkout/manage.py", "runserver", "0.0.0.0:8000"]

