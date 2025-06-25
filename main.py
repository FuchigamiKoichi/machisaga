# main.py
# FastAPIによる画像アップロード用Webアプリのエントリポイント
# コメントは日本語で記載

from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import shutil

app = FastAPI()

# テンプレートと静的ファイルの設定
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

UPLOAD_DIR = Path("uploaded")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    # 画像アップロードフォームを表示
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload", response_class=HTMLResponse)
def upload(request: Request, file1: UploadFile = File(...), file2: UploadFile = File(...)):
    # 画像ファイル2つを保存
    for idx, file in enumerate([file1, file2], 1):
        dest = UPLOAD_DIR / f"image{idx}_{file.filename}"
        with dest.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    msg = "画像2枚を受け付けました。"
    return templates.TemplateResponse("index.html", {"request": request, "msg": msg})
