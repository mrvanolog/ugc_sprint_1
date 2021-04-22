from api.v1.models import AddViewProgress
from services.events import EventSender, get_event_sender
from fastapi import APIRouter, Depends, Security

from api.v1.utils import auth
from services.models import ViewProgress

router = APIRouter()


@router.post('/view_progress')
async def send_view_progress(
        viewed_progress_data: AddViewProgress,
        event_sender: EventSender = Depends(get_event_sender),
        user_id: str = Security(auth)):
    viewed_progress = ViewProgress(user_id=user_id, movie_id=viewed_progress_data.movie_id,
                                   viewed_frame=viewed_progress_data.viewed_frame)
    await event_sender.send_viewed_progress(viewed_progress)
