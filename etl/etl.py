import time
import logging.config
from pathlib import Path
import yaml
from clickhouse_driver import Client
from kafka import KafkaConsumer
import clickhouse_driver.errors
import kafka.errors

from settings import backoff
from settings import (
    CH_HOST,
    CH_TABLE,
    KAFKA_TOPIC,
    KAFKA_CONSUMER_GROUP,
    KAFKA_SERVERS,
    FLUSH_SECONDS,
    FLUSH_COUNT,
)

# инициализируем logging
path_log_conf = Path(__file__).parent.joinpath("log_conf.yaml")
with path_log_conf.open("r") as f:
    log_conf = yaml.safe_load(f)

logging.config.dictConfig(log_conf)
logger = logging.getLogger("main")


@backoff
def connect_ch():
    return Client(host=CH_HOST)


@backoff
def connection_kafka():
    return KafkaConsumer(KAFKA_TOPIC, group_id=KAFKA_CONSUMER_GROUP,
                         bootstrap_servers=KAFKA_SERVERS,
                         auto_offset_reset='earliest')


def transform(value):
    """Преобразует строку данных из Kafka в формат ClickHouse.

    Args:
        value ([type]): строка данных из Kafka

    Returns:
        [type]: строка данных для ClickHouse
    """
    return value


def load(client: Client, values: list) -> bool:
    """Загружает батч данных в ClickHouse и обрабатывает возникающие ошибки.

    Args:
        client (Client): клиент ClickHouse
        values (list): список данных для загрузки

    Returns:
        bool: True если данные были успешно загружены, False в противном случае
    """
    try:
        client.execute(f'INSERT INTO {CH_TABLE} VALUES', values, types_check=True)
        return True
    except KeyError as e:
        logging.error(f'Ошибка записи в КХ из-за нехватки поля {e.args[0]} в переданной структуре')

    return False


def main():
    values_backup: list = []
    while True:
        try:
            client_ch = connect_ch()
            consumer = connection_kafka()

            # восстанавливаем данные из бэкапа
            # или инициализируем пустым списком, если это первый кгруг цикла
            values: list = values_backup
            flush_start = time.time()
            for msg in consumer:
                record = transform(msg.value)
                values.append(record)

                if values >= FLUSH_COUNT or (time.time() - flush_start) >= FLUSH_SECONDS:
                    res = load(client_ch, values)
                    # если не получилось загрузить данные в Клик, пытаемся в следующий раз
                    if not res:
                        continue

                    values = []
                    flush_start = time.time()
        except clickhouse_driver.errors.Error or kafka.errors.KafkaError:
            values_backup = values
            continue


if __name__ == '__main__':
    main()
