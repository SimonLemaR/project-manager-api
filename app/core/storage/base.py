from abc import ABC, abstractmethod

from fastapi import UploadFile


class StorageStrategy(ABC):
    @abstractmethod
    def save_file(
        self,
        project_id: int,
        file: UploadFile,
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    def delete_file(
        self,
        file_path: str,
    ) -> None:
        raise NotImplementedError
