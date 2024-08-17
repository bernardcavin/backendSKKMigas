from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import shutil
import os
from datetime import datetime

class FileInfo(BaseModel):
    filename: str
    size: int
    content_type: str
    upload_time: datetime

class UploadResponse(BaseModel):
    message: str
    file_info: FileInfo

class MultiUploadResponse(BaseModel):
    message: str
    files_info: List[FileInfo]