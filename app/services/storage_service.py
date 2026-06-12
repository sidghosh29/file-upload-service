from fastapi import UploadFile, HTTPException
from app.utils import generate_storage_filename
from app.config import settings
import os
from pathlib import PurePosixPath
from app.constants.validations import MAX_FILE_SIZE


async def save_file_to_storage(file: UploadFile):
    uploads_dir = settings.UPLOAD_DIR
    print(f"Uploads directory: {uploads_dir}")

    os.makedirs(uploads_dir, exist_ok=True)

    storage_filename = generate_storage_filename(file.filename)

    # logical_storage_filepath = uploads_dir+"/"+storage_filename
    logical_storage_filepath = str(PurePosixPath(uploads_dir) / storage_filename)

    physical_storage_filepath = os.path.join(
        os.path.abspath(uploads_dir), storage_filename
    )

    file_size = 0

    with open(physical_storage_filepath, "wb") as f:
        while True:
            chunk = await file.read(1024 * 1024)  # Read in 1MB chunks
            if not chunk:
                break
            file_size += len(chunk)
            if file_size > MAX_FILE_SIZE:
                f.close()
                await file.close()
                os.remove(physical_storage_filepath)
                raise HTTPException(
                    status_code=400,
                    detail="File size exceeds the maximum allowed limit",
                )
            f.write(chunk)
    await file.close()

    return {
        "logical_storage_filepath": logical_storage_filepath,
        "file_size": file_size,
    }


def delete_file_from_storage(storage_path: str):
    physical_storage_filepath = os.path.abspath((storage_path))
    if os.path.exists(physical_storage_filepath):
        os.remove(physical_storage_filepath)
