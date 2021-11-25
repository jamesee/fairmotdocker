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

from .webcam_lauretta import webcam

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
    def __init__(self, connection, queues, args):
        self.connection = connection
        self.queues = queues
        self.args = args

    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=self.queues,
                         callbacks=[self.on_message],
                         accept=['image/jpeg'])]

    def on_message(self, body, message):
        # get the original jpeg byte array size
        if sys.getsizeof(body) < 33:
            return 0
        size = sys.getsizeof(body) - 33
        # size = sys.getsizeof(body.tobytes()) - 33
        # jpeg-encoded byte array into numpy array
        np_array = np.frombuffer(body, dtype=np.uint8)
        # np_array = np.frombuffer(body.tobytes(), dtype=np.uint8)
        np_array = np_array.reshape((size, 1))
        # decode jpeg-encoded numpy array 
        image = cv2.imdecode(np_array, 1)

        # show image
        # cv2.imshow("image", image)
        # cv2.waitKey(1)

        webcam(self.args, image)
        # time.sleep(2)

        # send message ack
        message.ack()

def video_run(args):
    exchange = Exchange("video-exchange", type="direct")
    queues = [Queue("video-queue", exchange, routing_key="video")]
    # with Connection(rabbit_url, heartbeat=20) as conn:
    with Connection(rabbit_url) as conn:
            worker = Worker(conn, queues, args)
            worker.run()

# if __name__ == "__main__":
#     run()