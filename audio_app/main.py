import os
import ffmpeg
from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


app = FastAPI()
templates = Jinja2Templates(directory="audio_app/templates")

UPLOAD_DIRECTORY = "audio_app/uploads"
STATIC_DIRECTORY = "audio_app/static"

# Criar diretórios se não existirem
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
os.makedirs(STATIC_DIRECTORY, exist_ok=True)


# Servir arquivos das pastas uploads e static
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIRECTORY), name="uploads")
app.mount("/static", StaticFiles(directory=STATIC_DIRECTORY), name="static")

# dicionário para mapear os formatos MIME

MIME_TYPE_MAPPING = {
    "audio/mpeg": "mp3",
    "audio/wav": "wav"
}

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
    format_friendly = MIME_TYPE_MAPPING.get(mime, mime)

    
    metadata = {
        "filename": file.filename,
        "duration": format_duration(duration),
        "mime": mime,
        "format": format_friendly,
        "size": format_size(size)
    }
    
    return templates.TemplateResponse("metadata.html", {"request": request, "metadata": metadata})

@app.get("/selected-audio/{filename}/{format}", response_class=HTMLResponse)
async def get_convert_audio(request: Request, filename: str, format: str):
    # Renderizar o template de conversão com as informações do arquivo e formato atual
    return templates.TemplateResponse("convert_audio.html", {
        "request": request,
        "filename": filename,
        "current_format": format
    })

@app.post("/convert-audio/")
async def convert_audio(request: Request, filename: str = Form(...), format: str = Form(...)):
    file_location = os.path.join(UPLOAD_DIRECTORY, filename)
    base_name, _ = os.path.splitext(filename)
    output_location = os.path.join(UPLOAD_DIRECTORY, f'converted_{base_name}.{format}')

    # Conversão usando o ffmpeg
    ffmpeg.input(file_location).output(output_location).run(quiet=True)

    return templates.TemplateResponse("convert_audio.html", {
        "request": request,
        "filename": filename,
        "current_format": format,
        "converted_file": output_location
    })


