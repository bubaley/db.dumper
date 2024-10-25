from typing import Literal

from pydantic import BaseModel


class ConfigDatabaseConnection(BaseModel):
    type: Literal['postgres'] = 'postgres'
    name: str = 'postgres'
    host: str = 'localhost'
    port: int = 5432
    user: str = 'postgres'
    password: str = 'postgres'
    docker_container: str | None = None
