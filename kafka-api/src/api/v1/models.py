from pydantic.main import BaseModel


class AddViewProgress(BaseModel):
    movie_id: str
    viewed_frame: str
