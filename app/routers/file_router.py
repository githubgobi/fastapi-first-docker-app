from fastapi import APIRouter, UploadFile, File
from services.file_service import save_file
from core.logger import logger
import os

router = APIRouter()

UPLOAD_DIR = "uploads"

# ensure folder exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    logger.info(f"Saving file to {file_path}")
    save_file(file, file_path)
    return {"path": file_path}