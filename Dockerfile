FROM python:3.8.1-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set config flask
ENV FLASK_APP=main
ENV CONFIGURATION_SETUP="rfactorapp.config.DevelopmentConfig"

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . .

EXPOSE 5000

CMD ["python", "main.py"]
