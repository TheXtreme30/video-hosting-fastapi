import shutil
from typing import List
from fastapi import APIRouter, UploadFile, File


video_router = APIRouter()


@video_router.post('/')
async def upload_video(file: UploadFile = File(...)):
    with open(f'{file.filename}', 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)


@video_router.post('/image')
async def upload_image(files: List[UploadFile] = File(...)):
    for image in files:
        with open(f'{image.filename}', 'wb') as buffer:
            shutil.copyfileobj(image.file, buffer)
