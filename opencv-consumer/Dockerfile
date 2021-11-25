# Dockerfile.opencv-publisher

FROM python:3.8.12

WORKDIR /lauretta

RUN apt-get update && apt-get upgrade -y
# RUN apt-get install -y python3-opencv
RUN apt-get install netcat ffmpeg libsm6 libxext6  -y


RUN python3.8 -m pip install --upgrade pip
# RUN pip3.8 install numpy==1.18.4 cython==0.29.24 wheel 

# install dependencies
COPY requirements.txt .
RUN pip3.8 install -r requirements.txt

COPY . .
# RUN chmod +x entrypoint.sh

ENTRYPOINT [ "/bin/bash", "entrypoint.sh" ]

