from app.models.base import Base
from app.models.file import File  # noqa: F401
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import get_db

from app.config import settings

settings.UPLOAD_DIR = settings.TEST_UPLOAD_DIR

test_engine = create_engine(settings.TEST_DATABASE_URL)

Base.metadata.create_all(bind=test_engine)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def cleanup_database():
    yield

    db = TestSessionLocal()

    try:
        db.query(File).delete()
        db.commit()
    finally:
        db.close()


@pytest.fixture(autouse=True)
def cleanup_uploads():
    yield

    from app.utils import empty_folder, quick_empty_folder

    try:
        empty_folder(settings.TEST_UPLOAD_DIR)
    except Exception as e:
        print(f"Failed to clean up uploads directory. Reason: {e}")
        quick_empty_folder(settings.TEST_UPLOAD_DIR)
