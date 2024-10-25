from pydantic import BaseModel


class ConfigSSHConnection(BaseModel):
    host: str
    username: str
    port: int = 22
    password: str | None = None


class SSHConnection(ConfigSSHConnection):
    name: str
