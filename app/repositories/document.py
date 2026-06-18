from sqlalchemy.orm import Session

from app.models.document import Document


class DocumentRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_document(
        self,
        project_id: int,
        file_name: str,
        file_path: str,
        file_type: str,
    ) -> Document:

        document = Document(
            project_id=project_id,
            file_name=file_name,
            file_path=file_path,
            file_type=file_type,
        )

        self.db.add(document)

        return document
