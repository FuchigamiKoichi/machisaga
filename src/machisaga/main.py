# main.py
# FastAPIによる画像アップロード用Webアプリのエントリポイント
# コメントは日本語で記載

from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import shutil
from uuid import uuid4
from .find import findDifference

app = FastAPI()

# テンプレートと静的ファイルの設定
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploaded", StaticFiles(directory="uploaded"), name="uploaded")

UPLOAD_DIR = Path("uploaded")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    # 画像アップロードフォームを表示
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload", response_class=HTMLResponse)
def upload(
    request: Request,
    file1: UploadFile = File(...),
    file2: UploadFile = File(...),
    v: int = Form(...),
    h: int = Form(...),
    t: int = Form(...)
):
    import cv2
    import numpy as np
    # スライダー値を0~1, 0~1, 0~255に変換
    v_val = v / 100  # 縦方向ブレ補正（0~1）
    h_val = h / 100  # 横方向ブレ補正（0~1）
    t_val = t        # 感度（0~255）
    # 画像ファイルを一時保存せず直接読み込み
    file1.file.seek(0)
    file2.file.seek(0)
    img1_bytes = np.frombuffer(file1.file.read(), np.uint8)
    img2_bytes = np.frombuffer(file2.file.read(), np.uint8)
    img1 = cv2.imdecode(img1_bytes, cv2.IMREAD_COLOR)
    img2 = cv2.imdecode(img2_bytes, cv2.IMREAD_COLOR)
    result_img = findDifference(img1=img1, img2=img2, v=v_val, h=h_val, t=t_val)
    # サイズを揃える（小さい方に合わせる）
    h_min = min(img1.shape[0], img2.shape[0])
    w_min = min(img1.shape[1], img2.shape[1])
    img1 = img1[:h_min, :w_min]
    img2 = img2[:h_min, :w_min]
    # 半分に分割
    w_half = w_min // 2
    left = img1[:, :w_half]
    right = img2[:, w_half:]
    # 新しい画像を生成
    new_img = np.concatenate([left, right], axis=1)
    unique_name = f"merged_{uuid4().hex}.png"
    out_path = UPLOAD_DIR / unique_name
    cv2.imwrite(str(out_path), result_img)
    msg = f"計算が完了しました。縦方向ブレ補正: {v_val*100}, 横方向ブレ補正: {h_val*100}, 感度: {t_val}"
    # 画像を画面に表示
    return templates.TemplateResponse("index.html", {"request": request, "msg": msg, "merged_img": f"/uploaded/{unique_name}"})
