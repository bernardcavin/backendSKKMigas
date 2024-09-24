from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import shutil
import os
from datetime import datetime

class FileInfo(BaseModel):
    id: str
    filename: str
    file_location: str

    class Config:
        from_attributes = True

class UploadResponse(BaseModel):
    message: str
    file_info: FileInfo

class MultiUploadResponse(BaseModel):
    message: str
    files_info: List[FileInfo]

class TabularData(BaseModel):
    headers: List[str]
    records: List[dict]