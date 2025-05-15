#!/bin/bash
# 一键下载 Wav2Lip 推理所需文件到 scripts/ 目录
# 用法：bash scripts/download_wav2lip_infer_files.sh

set -e

BASE_URL="https://raw.githubusercontent.com/Rudrabha/Wav2Lip/master"
SCRIPT_DIR="$(dirname "$0")"

cd "$SCRIPT_DIR"

# 下载主文件
curl -O $BASE_URL/inference.py
curl -O $BASE_URL/audio.py
curl -O $BASE_URL/hparams.py
curl -O $BASE_URL/models.py

# 下载 face_detection 目录及其文件
mkdir -p face_detection
for file in __init__.py ssd.py box_utils.py face_detection.py api.py; do
  curl -o face_detection/$file $BASE_URL/face_detection/$file
done

echo "[INFO] Wav2Lip 推理所需文件已全部下载到 scripts/ 目录！"
