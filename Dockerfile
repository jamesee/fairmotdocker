# Dockerfile

# pull the official docker image
FROM python:3.8.12

COPY . .

# set work directory
WORKDIR /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements-web.txt .
COPY cameras.txt .

RUN python -m pip install --upgrade pip
RUN pip3.8 install -r requirements-web.txt
RUN apt-get update && apt-get install -y netcat



# WORKDIR /app/FairMOT/DCNv2
ENV PYTHONPATH "${PYTHONPATH}:app/FairMOT/src/lib:app/FairMOT/DCNv2/src:app/FairMOT/DCNv2:app/FairMOT:app/FairMOT"
# set work directory
# WORKDIR /app
