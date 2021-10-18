# Dockerfile

# pull the official docker image
FROM python:3.8.2

COPY . .

# set work directory
WORKDIR /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.txt .
COPY cameras.txt .
# COPY app/FairMOT FairMOT

RUN python -m pip install --upgrade pip
RUN pip3.8 install numpy==1.18.4 cython==0.29.24 wheel 
RUN pip3.8 install lap==0.4.0 cython_bbox
RUN pip3.8 install -r requirements.txt
RUN apt-get update && apt-get install -y python3-opencv
RUN apt-get install ffmpeg libsm6 libxext6  -y

# WORKDIR /app/FairMOT/DCNv2
# RUN python3.8 app/FairMOT/DCNv2/setup.py build develop
RUN python3.8 FairMOT/DCNv2/setup.py install develop
ENV PYTHONPATH "${PYTHONPATH}:app/FairMOT/src/lib:app/FairMOT/DCNv2/src:app/FairMOT/DCNv2:app/FairMOT:app/FairMOT"

# set work directory
# WORKDIR /app
