#!/bin/bash

while ! nc -z rabbitmq 5672; do sleep 3; done; 
# while ! nc -z opencv-publisher; do sleep 3; done; 

python3.8 -m monoloco.run predict --webcam --activities social_distance --output_types multi

