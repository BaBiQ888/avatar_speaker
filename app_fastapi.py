import os
import shutil
import uuid
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from scripts.generate_audio import main as tts_main
from scripts.generate_video import main as wav2lip_main
from scripts.merge_av import main as merge_main

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
    text: str = Form(...),
    image: UploadFile = File(...)
):
    # 创建唯一任务目录
    task_id = str(uuid.uuid4())
    task_dir = os.path.join("output", task_id)
    os.makedirs(task_dir, exist_ok=True)

    # 保存图片
    image_path = os.path.join(task_dir, "input.jpg")
    with open(image_path, "wb") as f:
        shutil.copyfileobj(image.file, f)

    # 保存文本
    text_path = os.path.join(task_dir, "input.txt")
    with open(text_path, "w", encoding="utf-8") as f:
        f.write(text)

    # 路径定义
    tts_out = os.path.join(task_dir, "tts.wav")
    video_out = os.path.join(task_dir, "video.mp4")
    final_out = os.path.join(task_dir, "final.mp4")
    model_path = "models/wav2lip.pth"

    # 步骤1：TTS
    tts_main(text_path, tts_out)
    # 步骤2：Wav2Lip
    wav2lip_main(image_path, tts_out, video_out, model_path)
    # 步骤3：合成
    merge_main(video_out, tts_out, final_out)

    # 返回视频下载链接
    return JSONResponse({
        "task_id": task_id,
        "video_url": f"/download/{task_id}"
    })


@app.get("/download/{task_id}")
def download(task_id: str):
    final_path = os.path.join("output", task_id, "final.mp4")
    if not os.path.exists(final_path):
        return JSONResponse({"error": "视频不存在"}, status_code=404)
    return FileResponse(final_path, media_type="video/mp4", filename="result.mp4")
