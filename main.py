import shutil
from fastapi import FastAPI, UploadFile, File


app = FastAPI()


@app.post('/')
async def upload_video(file: UploadFile = File(...)):
    with open(f'{file.filename}', 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {'file_name': file.filename}