import uuid
from pathlib import Path

def generate_storage_filename(filename: str) -> str:
    file_uuid = str(uuid.uuid4())
    file_extension = ''.join(Path(filename).suffixes)
    return f"{file_uuid}{file_extension}"