from pathlib import Path

from pydantic import Field, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    dumps_folder: str
    redis_dsn: RedisDsn = Field(default='redis://localhost:6379/1')
    debug: bool = Field(True)

    model_config = SettingsConfigDict(env_file=Path(Path(__name__).parent.parent, '.env'))
