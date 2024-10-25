from pydantic import BaseModel


class ConfigSSHConnection(BaseModel):
    host: str
    username: str
    port: int = 22
    password: str | None = None
    private_key: str | None = None
    passphrase: str | int | None = None


class SSHConnection(ConfigSSHConnection):
    name: str
