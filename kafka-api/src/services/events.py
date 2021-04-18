import json
import logging

from fastapi import Depends

from db.events_storage import AbstractEventStorage, get_event_storage
from services.models import ViewProgress

logger = logging.getLogger(__name__)


class EventSender:
    def __init__(self, storage: AbstractEventStorage):
        self.storage = storage

    async def send_viewed_progress(self, view_progress: ViewProgress):
        value = json.dumps(view_progress.to_dict()).encode()
        key = f'{view_progress.user_id}:{view_progress.movie_id}'.encode()
        await self.storage.send(topic='views', value=value, key=key)


def get_event_sender(
        event_storage: AbstractEventStorage = Depends(get_event_storage),
) -> EventSender:
    return EventSender(storage=event_storage)
