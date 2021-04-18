import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import views
from db.events_storage import get_event_storage, KafkaEventStorage

app = FastAPI(
    title='kafka-producer',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

app.include_router(
    views.router,
    prefix="/api/v1",
)


@app.get("/healthCheck")
async def healthCheck():
    return {"message": "Hello!"}


@app.on_event("startup")
async def startup_event():
    await get_event_storage()


@app.on_event("shutdown")
async def shutdown_event():
    event_storage: KafkaEventStorage = await get_event_storage()
    await event_storage.producer.stop()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)