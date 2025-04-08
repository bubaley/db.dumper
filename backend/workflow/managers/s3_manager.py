from pathlib import Path

import boto3
from botocore.client import BaseClient
from botocore.exceptions import EndpointConnectionError, NoCredentialsError

from workflow.functions.remove_local_file import remove_local_file
from workflow.managers.dump_exception import DumpException
from workflow.managers.workflow_event_manager import WorkflowEventManager
from workflow.models import Workflow


class S3Manager:
    def __init__(self, workflow: Workflow):
        self.config = workflow.config
        self.workflow: Workflow = workflow
        self._e: WorkflowEventManager | None = None
        self._client: BaseClient = None
        self._s3 = self.config.s3_connection

    def process(self, file_path: Path):
        self._e = WorkflowEventManager(self.workflow)
        self._e.add_event(name='S3_UPLOAD_PREPARED')
        self._connect()
        self._e.add_event(name='S3_CONNECTED')
        try:
            s3_path = self.get_s3_path(file_path.name)
            # self._client
            self._client.upload_file(file_path, self._s3.bucket, s3_path)
            self._e.add_event('S3_DUMP_UPLOADED', f'Filename: "{file_path.name}"')
            self._remove_local_file(file_path)
        except (NoCredentialsError, EndpointConnectionError) as e:
            self._remove_local_file(file_path)
            raise DumpException(name='S3_CONNECTION_ERROR', text=str(e))
        self._remove_old_files()

    def _remove_local_file(self, file_path):
        if remove_local_file(file_path):
            self._e.add_event('S3_LOCAL_DUMP_REMOVED', f'Filename: "{file_path.name}"')

    def _remove_old_files(self):
        response = self._client.list_objects_v2(Bucket=self._s3.bucket, Prefix=self.get_s3_path('dump_'))
        deleted_count = 0
        if 'Contents' in response:
            sorted_files = sorted(response['Contents'], key=lambda x: x['LastModified'], reverse=True)
            count: int = self.config.max_versions
            old_files = sorted_files[count:]
            for obj in old_files:
                self._client.delete_object(Bucket=self._s3.bucket, Key=obj['Key'])
                deleted_count += 1
        if deleted_count:
            self._e.add_event('S3_REMOVED_OLD_DUMPS', text=f'Count: {deleted_count}')

    def get_s3_path(self, filename: str = None):
        s3_path = self.config.key
        if self._s3.root:
            s3_path = f'{self._s3.root}/{s3_path}'
        if filename:
            s3_path = f'{s3_path}/{filename}'
        return s3_path

    def get_file_url(self):
        if not self.workflow.filename or not self.workflow.active:
            return None
        self._connect()
        prefix = self.get_s3_path(self.workflow.filename)
        response = self._client.list_objects_v2(Bucket=self._s3.bucket, Prefix=prefix)
        if 'Contents' in response:
            return self._client.generate_presigned_url(
                'get_object', Params={'Bucket': self._s3.bucket, 'Key': prefix}, ExpiresIn=7200
            )
        return None

    def _connect(self):
        self._client = boto3.client(
            's3',
            aws_access_key_id=self._s3.access_key,
            aws_secret_access_key=self._s3.secret_key,
            region_name=self._s3.region,
            endpoint_url=self._s3.url,
        )
