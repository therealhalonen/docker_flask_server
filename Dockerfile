# syntax=docker/dockerfile:1

# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

WORKDIR /python-docker

# Install wget and curl
RUN apt-get update && apt-get install -y wget curl

COPY . .

RUN pip install -r requirements.txt

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

