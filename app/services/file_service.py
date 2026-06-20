from uuid import UUID

from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.models.file import File as FileModel
from app.constants.validations import ALLOWED_CONTENT_TYPES
from app.services.storage_service import delete_file_from_storage, save_file_to_storage


def get_file_record(id: UUID, db: Session):
    file_record = db.get(FileModel, id)
    if not file_record:
        return None
    return file_record


async def save_file(file: UploadFile, db: Session):

    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Content type not allowed")

    storage_info = await save_file_to_storage(file)

    # Save file information to the database
    file_record = FileModel(
        original_filename=file.filename,
        storage_path=storage_info["logical_storage_filepath"],
        content_type=file.content_type,
        size=storage_info["file_size"],
    )

    try:
        db.add(file_record)
        db.commit()
        db.refresh(file_record)

    except Exception as e:
        print(e)
        db.rollback()
        delete_file_from_storage(storage_info["logical_storage_filepath"])

        raise HTTPException(status_code=500, detail="Failed to save file information")

    return file_record
