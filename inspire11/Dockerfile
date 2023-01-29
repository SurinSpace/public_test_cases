FROM ubuntu:20.04 as base

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata

RUN apt-get update && apt-get install -y -qq nano software-properties-common && apt-get update && add-apt-repository ppa:deadsnakes/ppa && apt-get install -y python3.9 python3-pip sqlite3

RUN update-alternatives --install /usr/bin/python3 python /usr/bin/python3.9 1

COPY . /workspace

WORKDIR /workspace

RUN python3.9 -m pip install --upgrade pip && pip install pipenv && pipenv install --system

RUN python3.9 -m pip install -e .