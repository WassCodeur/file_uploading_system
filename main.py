from typing import Annotated
from fastapi import FastAPI, Form, Request, UploadFile, templating
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
import json

app = FastAPI()

temp = os.path.join(os.path.dirname(__file__), "templates")

templates = Jinja2Templates(directory=temp)
data = os.path.join(os.path.dirname(__file__), "data.json")

images = []


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.post("/items/")
def create_item(item):
    return "Item created"


@app.post("/files/")
async def upload_file(file: UploadFile):
    # return {"file_size": len(file)}
    save_path = os.path.join(os.path.dirname(__file__), "image", file.filename)
    root = os.path.join(os.path.dirname(__file__), "image")
    if not os.path.exists(root):
        os.mkdir(root)

    with open(save_path, "wb") as f:
        f.write(file.file.read())

    with open(data, "r") as f:
        images = json.loads(f.read())
        images.append({"url": file.filename})

    with open(data, "w") as f:
        f.write(json.dumps(images))

    return {
        "filename": file.filename,
        "save_path": save_path,
        "root": root,
        "size": file.size,
        "images": images,
    }


@app.post("/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username}


@app.get("/gallery/")
def gallery():
    with open(data, "r") as f:
        images = json.loads(f.read())
    return {"images": images, "images_count": len(images)}
