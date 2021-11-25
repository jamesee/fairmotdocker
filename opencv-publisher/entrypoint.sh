#!/bin/bash

# while !</dev/tcp/rabbitmq/5672; 
# do sleep 3; 
# done; 

while ! nc -z rabbitmq 5672; do sleep 3; done; 

python3.8 publisher.py

