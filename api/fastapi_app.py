import os
import shutil
import uuid
from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.tts import tts
# from app.lip_sync import lip_sync
from app.musetalk_sync import musetalk_sync
from app.av_merge import merge
from app.config import OUTPUT_DIR

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/generate")
async def generate(
    request: Request,
    text: str = Form(...),
    image: UploadFile = File(...)
):
    print("[API] /generate called")
    print(f"[API] Request headers: {request.headers}")
    print(f"[API] text field: {text}")
    print(
        f"[API] image filename: {image.filename}, content_type: {image.content_type}")

    # 创建唯一任务目录
    task_id = str(uuid.uuid4())
    task_dir = os.path.join(OUTPUT_DIR, task_id)
    os.makedirs(task_dir, exist_ok=True)
    print(f"[API] Created task_dir: {task_dir}")

    # 保存图片
    image_path = os.path.join(task_dir, "input.jpg")
    with open(image_path, "wb") as f:
        shutil.copyfileobj(image.file, f)
    print(f"[API] Saved image to: {image_path}")

    # 保存文本
    text_path = os.path.join(task_dir, "input.txt")
    with open(text_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"[API] Saved text to: {text_path}")

    # 路径定义
    tts_out = os.path.join(task_dir, "tts.wav")
    video_out = os.path.join(task_dir, "musetalk_output.mp4")
    final_out = os.path.join(task_dir, "final.mp4")

    # 步骤1：TTS
    print("[API] Step 1: TTS start")
    tts(text_path, tts_out)
    print(f"[API] Step 1: TTS done, output: {tts_out}")

    # 步骤2：MuseTalk
    print("[API] Step 2: MuseTalk start")
    musetalk_sync(image_path, tts_out, video_out)
    print(f"[API] Step 2: MuseTalk done, output: {video_out}")

    # 步骤3：合成
    print("[API] Step 3: AV merge start")
    merge(video_out, tts_out, final_out)
    print(f"[API] Step 3: AV merge done, output: {final_out}")

    # 返回视频下载链接
    print(f"[API] Task {task_id} finished, video_url: /download/{task_id}")
    return JSONResponse({
        "task_id": task_id,
        "video_url": f"/download/{task_id}"
    })


@app.get("/download/{task_id}")
def download(task_id: str):
    final_path = os.path.join(OUTPUT_DIR, task_id, "final.mp4")
    if not os.path.exists(final_path):
        return JSONResponse({"error": "视频不存在"}, status_code=404)
    return FileResponse(final_path, media_type="video/mp4", filename="result.mp4")
