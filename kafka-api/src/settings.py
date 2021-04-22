from typing import List

from pydantic import BaseSettings


class Settings(BaseSettings):
    kafka_bootstrap_servers: List = ['broker:29092']

    secret_key: str
    algorithm: str = 'HS256'


settings = Settings()
