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


def get_duration(file_path):
    result = ffmpeg.probe(file_path, select_streams='a:0', show_entries='format=duration', format='json')
    return float(result['format']['duration'])

def format_duration(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f'{hours:02}:{minutes:02}:{seconds:02}'

def format_size(size):
    return f"{size / (1024 * 1024):.2f} MB"


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload-audio/")
async def upload_audio(request: Request, file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    
    # Gerar metadados usando ffmpeg-python
    duration = get_duration(file_location)
    size = os.path.getsize(file_location)
    mime = file.content_type
    
    metadata = {
        "filename": file.filename,
        "duration": format_duration(duration),
        "mime": mime,
        "size": format_size(size)
    }
    
    return templates.TemplateResponse("metadata.html", {"request": request, "metadata": metadata})