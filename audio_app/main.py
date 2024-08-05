import os
import ffmpeg
from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


app = FastAPI()
templates = Jinja2Templates(directory="audio_app/templates")

UPLOAD_DIRECTORY = "audio_app/uploads"

# crie o diretório de uploads se não exitir
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

# Servir arquivos da pasta download
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIRECTORY), name="uploads")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload-audio/")
async def upload_audio(request: Request, file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    
    # Gerar metadados usando ffmpeg-python
    probe = ffmpeg.probe(file_location)
    duration = float(probe['format']['duration'])
    size = os.path.getsize(file_location)
    mime = file.content_type
    
    metadata = {
        "filename": file.filename,
        "duration": duration,
        "mime": mime,
        "size": size
    }
    
    return templates.TemplateResponse("metadata.html", {"request": request, "metadata": metadata})