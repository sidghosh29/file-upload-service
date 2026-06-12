from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.api.files import router as files_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    yield
    print("Shutting down...")


app = FastAPI(lifespan = lifespan)

@app.get("/")
@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/db-check")
def db_check(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1"))
    return {"result": result.scalar()}

app.include_router(files_router)