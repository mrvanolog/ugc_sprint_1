import time
import logging.config
import json
from datetime import datetime
from clickhouse_driver import Client
from kafka import KafkaConsumer
import clickhouse_driver.errors
import kafka.errors

from conf.utils import backoff
from conf.settings import (
    CH_HOST,
    CH_TABLE,
    KAFKA_TOPIC,
    KAFKA_CONSUMER_GROUP,
    KAFKA_SERVERS,
    FLUSH_SECONDS,
    FLUSH_COUNT,
)
from conf.settings import log_conf


logging.config.dictConfig(log_conf)
logger = logging.getLogger("main")


@backoff
def connect_ch():
    return Client.from_url(CH_HOST)


@backoff
def connect_kafka():
    return KafkaConsumer(KAFKA_TOPIC, group_id=KAFKA_CONSUMER_GROUP,
                         bootstrap_servers=KAFKA_SERVERS,
                         auto_offset_reset='earliest')


def transform(value: dict) -> dict:
    """Преобразует строку данных из Kafka в формат ClickHouse.

    Args:
        value (dict): строка данных из Kafka

    Returns:
        dict: строка данных для ClickHouse
    """
    record = {}
    try:
        record['user_id'] = str(value.get('user_id'))
        record['movie_id'] = str(value.get('movie_id'))
        record['viewed_frame'] = int(value.get('viewed_frame'))
        record['created_at'] = datetime.now()
    except Exception as e:
        logger.error(f'При подготовке сообщения возникла ошибка: {e}')

    return record


def load(client: Client, values: list) -> bool:
    """Загружает батч данных в ClickHouse и обрабатывает возникающие ошибки.

    Args:
        client (Client): клиент ClickHouse
        values (list): список данных для загрузки

    Returns:
        bool: True если данные были успешно загружены, False в противном случае
    """
    logger.debug('Загрузка данных в ClickHouse...')
    try:
        client.execute(f'INSERT INTO {CH_TABLE} VALUES', values, types_check=True)
        logger.debug(f'Успешно загружено {len(values)} строк')
        return True
    except KeyError as e:
        logger.error(f'Ошибка записи в КХ из-за нехватки поля {e.args[0]} в переданной структуре')

    return False


def main():
    values_backup: list = []
    values: list = []
    while True:
        try:
            logger.debug('Подключение к CH')
            client_ch = connect_ch()
            logger.debug('Подключение к Kafka')
            consumer = connect_kafka()
            logger.debug('Базы успешно подключены')

            # восстанавливаем данные из бэкапа
            # или инициализируем пустым списком, если это первый кгруг цикла
            values = values_backup
            flush_start = time.time()
            for msg in consumer:
                value = json.loads(msg.value)
                record = transform(value)
                values.append(record)

                if len(values) >= FLUSH_COUNT or (time.time() - flush_start) >= FLUSH_SECONDS:
                    res = load(client_ch, values)
                    # если не получилось загрузить данные в Клик, пытаемся в следующий раз
                    if not res:
                        continue

                    values = []
                    flush_start = time.time()
        except clickhouse_driver.errors.Error as e:
            logger.error(f'Ошибка в соединении с ClickHouse: {e}')
        except kafka.errors.KafkaError as e:
            logger.error(f'Ошибка в соединении с Kafka: {e}')
        finally:
            values_backup = values


if __name__ == '__main__':
    logger.info('Up\'n\'running')
    main()
