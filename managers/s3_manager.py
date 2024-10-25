import os

import boto3
from botocore.client import BaseClient
from botocore.exceptions import EndpointConnectionError, NoCredentialsError
from loguru import logger

from functions.remove_local_file import remove_local_file
from managers.config_manager import Config


class S3Manager:
    def __init__(self, config: Config):
        self.config = config
        self._client: BaseClient = None
        self._s3 = self.config.s3

    def process(self, file_path: str):
        logger.info({'event': 'START_S3_DUMP', 'config': self.config.name, 'file_path': file_path})
        self._client = boto3.client(
            's3',
            aws_access_key_id=self._s3.access_key,
            aws_secret_access_key=self._s3.secret_key,
            region_name=self._s3.region,
            endpoint_url=self._s3.url,
        )
        try:
            filename = os.path.basename(file_path)
            s3_path = self.get_s3_path(filename)
            self._client.upload_file(file_path, self._s3.bucket, s3_path)
            logger.info({'event': 'S3_DUMP_UPLOADED', 'config': self.config.name, 'file_path': s3_path})
            if not self.config.s3.keep_local_files:
                if remove_local_file(file_path):
                    logger.info({'event': 'S3_LOCAL_DUMP_REMOVED', 'config': self.config.name, 'filename': filename})
        except (NoCredentialsError, EndpointConnectionError) as e:
            logger.error({'event': 'S3_CONNECTION_ERROR', 'config': self.config.name, 'error': str(e)})
        self._remove_old_files()

    def _remove_old_files(self):
        response = self._client.list_objects_v2(Bucket=self._s3.bucket, Prefix=self.get_s3_path('dump_'))
        deleted_count = 0
        if 'Contents' in response:
            sorted_files = sorted(response['Contents'], key=lambda x: x['LastModified'], reverse=True)
            count: int = self.config.settings.max_versions
            old_files = sorted_files[count:]
            for obj in old_files:
                self._client.delete_object(Bucket=self._s3.bucket, Key=obj['Key'])
                deleted_count += 1
        if deleted_count:
            logger.info({'event': 'S3_REMOVED_OLD_FILES', 'config': self.config.name, 'count': deleted_count})

    def get_s3_path(self, filename: str = None):
        s3_path = self.config.name
        if self._s3.root:
            s3_path = f'{self._s3.root}/{s3_path}'
        if filename:
            s3_path = f'{s3_path}/{filename}'
        return s3_path
