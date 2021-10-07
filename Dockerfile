# Dockerfile

# pull the official docker image
FROM python:3.8.2-slim

# set work directory
WORKDIR /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip3 install numpy==1.18.4 cython==0.29.24 wheel
RUN pip3 install lap==0.4.0
RUN pip3 install -r requirements.txt
RUN sh FairMOT/DCNv2/make.sh

# copy project
COPY . .
