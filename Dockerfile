FROM python:3.7.4

# set work directory
WORKDIR /onestore

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install project dependencies
RUN pip install pipenv
COPY ./Pipfile /onestore/Pipfile
COPY ./Pipfile.lock /onestore/Pipfile.lock
RUN pipenv lock --requirements > /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY ./ /onestore/
