from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class FileUploadResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: UUID
    original_filename: str
    content_type: str
    size: int
    uploaded_at: datetime