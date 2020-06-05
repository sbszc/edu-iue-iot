# pull official base image
# FROM python:3.8.0-alpine3.10
FROM python:3.8.0
LABEL mainteiner="jairocuartas@gmail.com"

# set environment variables
# This prevents Python from writing out pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# This keeps Python from buffering stdin/stdout
ENV PYTHONUNBUFFERED 1

#Enviroment variables
ENV USER=desarrollo
ENV HOME=/home/desarrollo
ENV PROJECT_DIR=/home/desarrollo/consumer
ENV SHELL=/bin/sh

RUN adduser $USER --shell $SHELL --disabled-password

COPY ./requirements.txt $HOME

# Create the user desarrollo.
# Install project requirements.
# Set user desarrollo the owner for HOME
RUN pip install --upgrade pip \
    && mkdir -p $HOME/.cache/pip \
    && pip install -r $HOME/requirements.txt \
    && chown -R $USER:$USER $HOME


USER $USER

WORKDIR $PROJECT_DIR
