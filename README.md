# Digital Human Talker

> 一个基于 Python 实现的数字人自动口型视频生成系统，支持文本转语音（TTS）、图像驱动口型视频，并一键合成视频。支持 **Linux/CPU-only** 环境，无需 GPU，适合培训、小型应用。

---

## 结构化目录

```
digital_human_talker/
│
├── app/                        # 业务核心代码包
│   ├── __init__.py
│   ├── tts.py                  # 文本转语音
│   ├── lip_sync.py             # 口型合成
│   ├── av_merge.py             # 音视频合成
│   └── config.py               # 配置管理
│
├── api/                        # 服务接口
│   ├── __init__.py
│   └── fastapi_app.py          # FastAPI 服务主入口
│
├── scripts/                    # 兼容 CLI 脚本（调用 app/）
│   ├── generate_audio.py
│   ├── generate_video.py
│   └── merge_av.py
│
├── tests/                      # 基础测试用例
│   ├── test_tts.py
│   ├── test_lip_sync.py
│   └── test_av_merge.py
│
├── input/                      # 用户输入
├── output/                     # 输出结果
├── models/                     # 模型权重
│
├── pipeline.py                 # CLI 一键流水线入口
├── requirements.txt
├── setup.sh
└── README.md
```

**目录说明：**
- `app/`：核心功能模块，便于扩展和服务化
- `api/`：FastAPI 服务接口
- `scripts/`：兼容 CLI 脚本
- `tests/`：基础测试用例
- `input/`、`output/`、`models/`：输入、输出、模型权重

---

## 快速开始

### 1. 安装依赖（推荐 CPU-only 环境）
```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
sudo apt update && sudo apt install ffmpeg libsndfile1
```

### 2. 下载模型权重
- Wav2Lip: 下载 wav2lip.pth 到 models/
- Bark: 首次运行自动下载

### 3. 准备 Wav2Lip 脚本
请从 [Wav2Lip 官方仓库](https://github.com/Rudrabha/Wav2Lip) 下载 `inference.py` 到 `scripts/wav2lip_inference.py`。

### 4. 命令行一键生成
```bash
python pipeline.py \
  --text input/input_text.txt \
  --image input/reference_image.jpg \
  --output_dir output/
```

### 5. 单步运行（兼容原 scripts/）
```bash
python scripts/generate_audio.py --text input/input_text.txt --output output/tts_output.wav
python scripts/generate_video.py --image input/reference_image.jpg --audio output/tts_output.wav --output output/wav2lip_output.mp4 --model models/wav2lip.pth
python scripts/merge_av.py --video output/wav2lip_output.mp4 --audio output/tts_output.wav --output output/final_output.mp4
```

### 6. 启动 API 服务
```bash
uvicorn api.fastapi_app:app --host 0.0.0.0 --port 8000
```
- POST /generate  上传文本和图片，返回视频下载链接
- GET /download/{task_id}  下载生成视频

#### API Python 示例
```python
import requests
with open('input/reference_image.jpg', 'rb') as img:
    resp = requests.post(
        'http://localhost:8000/generate',
        data={'text': '你好，欢迎体验数字人口型视频！'},
        files={'image': img}
    )
print(resp.json())
```

---

## 测试

```bash
pytest tests/
```

---

## 开发建议
- 业务逻辑全部集中在 app/，便于后续扩展和服务化。
- config.py 统一管理路径和模型配置。
- 支持 CLI、API、后续可扩展前端。
- 推荐逐步废弃 scripts/，直接用 app/ 和 pipeline.py。

---

## 贡献&扩展
- 支持 XTTS、SadTalker 等模型可插拔。
- 可扩展为 Flask/FastAPI/Streamlit 前端。
- 支持 Docker 部署。

---

## 运行环境说明
- 推荐 Linux (Ubuntu 22.04) + CPU-only，无需 GPU。
- Windows/Mac 兼容性良好，但推理速度依赖硬件。

---

## 常见问题（FAQ）
- **Bark 报错找不到 libsndfile1？**
  `sudo apt install libsndfile1`
- **Wav2Lip 口型合成报错？**
  检查 models/wav2lip.pth 和 scripts/wav2lip_inference.py 是否存在。
- **推理速度慢？**
  CPU-only 环境下为正常现象，建议小批量测试。

如需进一步开发建议或功能扩展，欢迎联系！
