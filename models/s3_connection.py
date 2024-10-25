from pydantic import BaseModel


class ConfigS3Connection(BaseModel):
    bucket: str
    region: str
    access_key: str
    secret_key: str
    root: str = None
    url: str = None
    keep_local_files: bool = False


class S3Connection(ConfigS3Connection):
    name: str
