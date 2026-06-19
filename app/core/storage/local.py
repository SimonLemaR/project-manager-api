from pathlib import Path
import shutil

from fastapi import UploadFile

from app.core.storage.base import StorageStrategy


class LocalStorageStrategy(StorageStrategy):

    UPLOAD_DIR = Path("/app/uploads")

    def save_file(
        self,
        project_id: int,
        file: UploadFile,
    ) -> str:

        project_folder = (
            self.UPLOAD_DIR
            / f"{project_id}_project"
        )

        project_folder.mkdir(
            parents=True,
            exist_ok=True,
        )

        file_path = project_folder / file.filename
        counter = 1
        while file_path.exists():

            original_name = file_path.stem
            extension = file_path.suffix

            file_path = (
                project_folder
                / f"{original_name}_{counter}{extension}"
            )

            counter += 1

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer
            )

        return str(file_path)