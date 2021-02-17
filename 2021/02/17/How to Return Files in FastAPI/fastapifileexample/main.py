import os

from fastapi import FastAPI 
from fastapi.responses import FileResponse

app = FastAPI()

path = "/home/anthony/fastapifileexample"

@app.get("/")
def index():
    return {"Hello": "World"}

@app.get("/cat", responses={200: {"description": "A picture of a cat.", "content" : {"image/jpeg" : {"example" : "No example available. Just imagine a picture of a cat."}}}})
def cat():
    file_path = os.path.join(path, "files/cat.jpg")
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="image/jpeg", filename="mycat.jpg")
    return {"error" : "File not found!"}