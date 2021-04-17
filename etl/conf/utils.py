import time
from functools import wraps


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
