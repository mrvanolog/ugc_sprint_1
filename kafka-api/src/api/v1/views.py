from services.events import EventSender, get_event_sender
from services.models import ViewProgress
from fastapi import APIRouter, Depends

router = APIRouter()


@router.post('/view_progress')
async def send_view_progress(viewed_progress: ViewProgress, event_sender:
EventSender = Depends(get_event_sender)):
    await event_sender.send_viewed_progress(viewed_progress)
