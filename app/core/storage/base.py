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