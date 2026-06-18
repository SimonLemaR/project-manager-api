# services/storage/factory.py

from app.services.project.storage.base import StorageService
from app.services.project.storage.local import LocalStorageService


def get_storage_service()-> StorageService:
    return LocalStorageService()