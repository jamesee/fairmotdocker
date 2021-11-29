"""Kombu-based Video Stream Consumer
Written by Minsu Jang
Date: 2018-06-09
Reference
- Building Robust RabbitMQ Consumers With Python and Kombu: Part 1 (https://medium.com/python-pandemonium/building-robust-rabbitmq-consumers-with-python-and-kombu-part-1-ccd660d17271)
- Building Robust RabbitMQ Consumers With Python and Kombu: Part 2 (https://medium.com/python-pandemonium/building-robust-rabbitmq-consumers-with-python-and-kombu-part-2-e9505f56e12e)
"""

import cv2
import numpy as np
import sys
import time
import os
import logging

from kombu import Connection, Exchange, Queue
from kombu.mixins import ConsumerMixin

from .track_lauretta import eval_prop_loop


LOG = logging.getLogger(__name__)

# Default RabbitMQ server URI
# Default RabbitMQ server URI
if os.getenv('RABBITMQ_URL'):
    rabbit_url = os.getenv('RABBITMQ_URL')
else:
    rabbit_url = 'amqp://guest:guest@localhost:5672//'
    
LOG.info(f"rabbit_url :{rabbit_url}")

# Kombu Message Consuming Worker
class Worker(ConsumerMixin):
    def __init__(self, connection, queues):
        self.connection = connection
        self.queues = queues

    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=self.queues,
                         callbacks=[eval_prop_loop],
                         accept=['image/jpeg'])]



def video_run(camera_shift_time, prev_time, timer,results,frame_id):
    exchange = Exchange("video-exchange", type="fanout")
    queues = [Queue("fairmot-queue", exchange, routing_key="video")]
    with Connection(rabbit_url, heartbeat=100) as conn:
            worker = Worker(conn, queues)
            worker.run()

# if __name__ == "__main__":
#     video_run()