import boto3
from fastapi import UploadFile

from app.core.config import settings
from app.core.storage.base import StorageStrategy


class S3StorageStrategy(StorageStrategy):
    def __init__(self):
        self.bucket_name = settings.AWS_BUCKET_NAME
        self.client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
        )

    def save_file(
        self,
        project_id: int,
        file: UploadFile,
    ) -> str:
        object_key = f"projects/{project_id}/{file.filename}"
        self.client.upload_fileobj(file.file, self.bucket_name, object_key)
        return object_key

    def delete_file(
        self,
        file_path: str,
    ) -> None:
        self.client.delete_object(
            Bucket=self.bucket_name,
            Key=file_path,
        )
