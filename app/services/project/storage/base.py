from abc import abstractmethod

from fastapi import UploadFile

@abstractmethod
class StorageService:

    def save_file(
        self,
        project_id: int,
        file: UploadFile,
    ) -> str:
        raise NotImplementedError