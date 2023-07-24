from utils.configs import get_storage_type
from utils.constants import LOCAL
from utils.storage.local_file_system import LocalFileSystemStorage


def get_storage_instance():
    storage_type = get_storage_type()
    if storage_type == LOCAL:
        return LocalFileSystemStorage()
    else:
        raise ValueError(f"Unsupported storage type {storage_type}")
