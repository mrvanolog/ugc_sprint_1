import os
import time
from functools import wraps


CH_HOST = os.environ.get('CH_HOST', default='localhost')
CH_TABLE = os.environ.get('CH_TABLE', default='analysis.viewed_progress')

KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC')
KAFKA_CONSUMER_GROUP = os.environ.get('KAFKA_CONSUMER_GROUP')
KAFKA_SERVERS = os.environ.get('KAFKA_SERVERS')

FLUSH_SECONDS = float(os.environ.get('FLUSH_SECONDS', default='30'))
FLUSH_COUNT = int(os.environ.get('FLUSH_COUNT', default='1000'))


def backoff(func):
    @wraps(func)
    def inner(*args, **kwargs):
        t = 0.1
        border_sleep_time = 10

        while True:
            if t < border_sleep_time:
                t *= 2

            try:
                conn = func(*args, **kwargs)
                return conn
            except Exception:
                time.sleep(t)

    return inner
