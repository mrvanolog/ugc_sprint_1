import abc
import asyncio
import logging
from typing import Optional

from aiokafka import AIOKafkaProducer

from settings import settings


class AbstractEventStorage(abc.ABC):
    @abc.abstractmethod
    def send(self, *args, **kwargs):
        pass


logger = logging.getLogger(__name__)


class KafkaEventStorage(AbstractEventStorage):
    def __init__(self, producer: AIOKafkaProducer):
        self.producer = producer

    async def send(self, topic: str, value: str, key: str, *args, **kwargs):
        try:
            await self.producer.send_and_wait(topic, value)
        except Exception as e:
            logger.exception(e)


event_storage: Optional[AbstractEventStorage]


async def get_event_storage() -> AbstractEventStorage:
    global event_storage
    if not event_storage:
        loop = asyncio.get_event_loop()
        # Set max_batch_size and linger_ms to manage batch sending
        kafka_producer = AIOKafkaProducer(loop=loop,
                                          bootstrap_servers=settings.kafka_bootstrap_servers)
        await kafka_producer.start()
        event_storage = KafkaEventStorage(producer=kafka_producer)
    return event_storage
