import os

from fastapi import APIRouter, UploadFile, File, Depends, Path, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.file_service import save_file, get_file_record
from app.schemas.file import FileUploadResponse

from uuid import UUID

router = APIRouter()


@router.post("/files", status_code=201, response_model=FileUploadResponse)
async def upload_file(
    file: UploadFile = File(...), db: Session = Depends(get_db)
):  # ... means it's a required field

    return await save_file(file, db)


@router.get("/files/{id}")
async def download_file(id: UUID = Path(...), db: Session = Depends(get_db)):

    file_record = get_file_record(id, db)
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")

    logical_storage_filepath = file_record.storage_path
    physical_storage_filepath = os.path.abspath((logical_storage_filepath))

    print(f"Logical storage filepath: {logical_storage_filepath}")
    print(f"Physical storage filepath: {physical_storage_filepath}")

    if not os.path.exists(physical_storage_filepath):
        raise HTTPException(status_code=404, detail="Physical file not found")

    return FileResponse(
        path=physical_storage_filepath, filename=file_record.original_filename
    )
