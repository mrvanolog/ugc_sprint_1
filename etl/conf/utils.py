import logging
import time
from functools import wraps

from conf.settings import log_conf


logging.config.dictConfig(log_conf)
logger = logging.getLogger("backoff")


def backoff(func):
    @wraps(func)
    def inner(*args, **kwargs):
        t = 0.1
        border_sleep_time = 10

        while True:
            logger.debug('Попытка подключения к БД...')
            if t < border_sleep_time:
                t *= 2

            try:
                conn = func(*args, **kwargs)
                return conn
            except Exception as e:
                logger.error(f'Ошибка подключения: {e}')
                logger.info(f'Повторная попытка через {t} секунд')
                time.sleep(t)

    return inner
