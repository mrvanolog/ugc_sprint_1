from pydantic.main import BaseModel


class ViewProgress(BaseModel):
    user_id: str
    movie_id: str
    viewed_frame: str

    def to_dict(self) -> dict:
        return {
            'user_id': self.user_id,
            'movie_id': self.movie_id,
            'viewed_frame': self.viewed_frame
        }
