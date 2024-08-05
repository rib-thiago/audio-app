from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()
templates = Jinja2Templates(directory="audio_app/templates")

UPLOAD_DIRECTORY = "audio_app/uploads"

# crie o diretório de uploads se não exitir
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload-audio/")
async def upload_audio(request: Request, file: UploadFile = File(...)):
    file_location = f'audio_app/uploads/{file.filename}'
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    # Aqui, posso adicionar a lógica para processar áudio e gerar metadados
    return {"filename": file.filename}