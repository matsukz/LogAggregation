FROM ubuntu:latest

RUN apt-get update
RUN apt upgrade -y
RUN apt-get install python3 python3-pip -y

RUN mkdir /python

WORKDIR /python

COPY ./python/requirements.txt /python

RUN pip install -r requirements.txt