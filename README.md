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
│   ├── wav2lip_inference.py    # Wav2Lip 官方脚本（需手动下载）
│   └── audio.py                # Wav2Lip 官方依赖（需手动下载）
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
请从 [Wav2Lip 官方仓库](https://github.com/Rudrabha/Wav2Lip) 下载 `inference.py` 和 `audio.py` 到 `scripts/` 目录：
```bash
curl -o scripts/wav2lip_inference.py https://raw.githubusercontent.com/Rudrabha/Wav2Lip/master/inference.py
curl -o scripts/audio.py https://raw.githubusercontent.com/Rudrabha/Wav2Lip/master/audio.py
```

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

### 1. inference.py 下载后报 HTML/语法错误？
- 你下载的是网页不是源码。请用 `curl` 或在 GitHub "Raw" 页面右键另存为。

### 2. `ModuleNotFoundError: No module named 'audio'`？
- 你缺少 Wav2Lip 的 audio.py 文件。请用如下命令下载：
  ```bash
  curl -o scripts/audio.py https://raw.githubusercontent.com/Rudrabha/Wav2Lip/master/audio.py
  ```

### 3. `FileNotFoundError: No such file or directory: 'python'` 或 `'sys.executable'`？
- 推荐在 subprocess 里用 `sys.executable` 变量（不要加引号），保证用当前 Python 解释器。

### 4. Bark 报权重加载或 pickle 错误？
- PyTorch 2.6+ 默认 `weights_only=True`，Bark 兼容性差。请降级 torch/torchaudio：
  ```bash
  pip uninstall torch torchaudio
  pip install torch==2.5.1 torchaudio==2.5.0 --index-url https://download.pytorch.org/whl/cpu
  ```

### 5. `ffmpeg`、`libsndfile1` 报错？
- Linux 下需安装：
  ```bash
  sudo apt install ffmpeg libsndfile1
  ```

### 6. 口型推理慢/CPU-only 慢？
- 纯 CPU 环境下为正常现象，建议小批量测试。

### 7. 其它依赖冲突？
- 保证 torch、torchaudio 版本一致，requirements.txt 里如无特殊需求可不装 torchaudio。

---

如需进一步开发建议或功能扩展，欢迎联系！

# 数字人口型同步视频生成系统

本项目实现了一个简单的口型同步视频生成系统，支持 Wav2Lip 和 MuseTalk 两种口型同步引擎。

## 特性

- 文本转语音 (TTS)
- 口型同步视频生成 (支持 Wav2Lip 和 MuseTalk)
- 音频和视频合成
- 命令行和 API 接口

## 安装

### 1. 克隆仓库

```bash
git clone <repository-url>
cd avatar_speaker
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 设置 MuseTalk（推荐）

我们强烈推荐使用 MuseTalk 作为口型同步引擎，质量比 Wav2Lip 更佳。

```bash
# 设置 MuseTalk v1.0
python -m scripts.setup_musetalk --version v1.0

# 或设置 MuseTalk v1.5 (推荐)
python -m scripts.setup_musetalk --version v1.5
```

按照脚本提示从官方渠道获取模型文件。

### 4. 检查 MuseTalk 安装

```bash
python -m scripts.check_musetalk --version v1.0
```

## 使用方法

### 命令行

```bash
# 使用 MuseTalk (默认)
python pipeline.py --text input/input_text.txt --image input/reference_image.jpg --output_dir output/

# 使用 Wav2Lip
python pipeline.py --text input/input_text.txt --image input/reference_image.jpg --output_dir output/ --lip_model wav2lip

# 使用 MuseTalk v1.5
python pipeline.py --text input/input_text.txt --image input/reference_image.jpg --musetalk_version v1.5
```

#### MuseTalk 参数调整

MuseTalk 支持多种参数来微调生成效果：

```bash
# 调整嘴部区域 (正值增加嘴部开度，负值减少嘴部开度)
python pipeline.py --text input/input_text.txt --image input/reference_image.jpg --bbox_shift -5

# 使用半精度推理 (节省显存)
python pipeline.py --text input/input_text.txt --image input/reference_image.jpg --use_float16

# 设置输出视频帧率
python pipeline.py --text input/input_text.txt --image input/reference_image.jpg --fps 30
```

### API 服务

```bash
# 启动 API 服务
uvicorn api.fastapi_app:app --host 0.0.0.0 --port 8000
```

## API 文档

启动服务后，访问 http://localhost:8000/docs 查看 API 文档。

### 生成视频

POST `/generate`

参数:
- `text`: 文本内容 
- `image`: 图像文件
- `musetalk_version`: MuseTalk 版本，可选 `v1.0` 或 `v1.5`
- `bbox_shift`: 嘴部区域调整，正值增加嘴部开度，负值减少嘴部开度
- `use_float16`: 是否使用半精度推理以节省显存
- `fps`: 生成视频的帧率

响应:
```json
{
  "task_id": "uuid",
  "video_url": "/download/uuid"
}
```

### 下载视频

GET `/download/{task_id}`

## 系统要求

- Python 3.8+
- 建议：CUDA 支持的 GPU（用于 MuseTalk 和 Wav2Lip 推理）
- 内存：至少 8GB（MuseTalk 比 Wav2Lip 内存占用更低）

## 调整 MuseTalk 配置

可以通过编辑 `app/config.py` 文件来调整 MuseTalk 的默认配置：

```python
# MuseTalk 推理参数
MUSETALK_INFERENCE = {
    'fps': 25,
    'bbox_shift': 0,  # 嘴部区域调整参数，正值增加嘴部开度，负值减少嘴部开度
    'use_float16': True,  # 是否使用半精度推理以节省显存
}
```

## 注意事项

- MuseTalk 官方项目：https://github.com/netease-youdao/MuseTalk
- 如遇到内存问题，请优先使用 MuseTalk，它比 Wav2Lip 更高效
- 嘴型同步效果不佳时，尝试调整 `bbox_shift` 参数
