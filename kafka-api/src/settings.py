from pydantic import BaseSettings


class Settings(BaseSettings):
    kafka_bootstrap_servers: str = ['localhost:9092']


settings = Settings()
