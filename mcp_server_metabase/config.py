from pydantic_settings import BaseSettings


class Config(BaseSettings):
    metabase_url: str
    metabase_api_key: str


config = Config()
