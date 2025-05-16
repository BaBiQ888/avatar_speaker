#!/usr/bin/env python3
import os
import sys
import argparse
from app.config import MUSETALK_DIR


def check_musetalk_installation(musetalk_dir=MUSETALK_DIR, version="v1.0"):
    """检查 MuseTalk 安装是否正确"""
    print(f"检查 MuseTalk 安装 (版本: {version})...")

    # 检查目录
    if not os.path.exists(musetalk_dir):
        print(f"错误: MuseTalk 目录不存在: {musetalk_dir}")
        print("提示: 请运行 `git clone https://github.com/netease-youdao/MuseTalk.git external/MuseTalk`")
        return False

    # 检查基本目录结构
    required_dirs = [
        "configs",
        "scripts",
    ]

    for d in required_dirs:
        path = os.path.join(musetalk_dir, d)
        if not os.path.exists(path):
            print(f"错误: 目录不存在: {path}")
            print("提示: MuseTalk 可能未正确克隆，请尝试重新克隆仓库")
            return False

    # 检查版本相关文件
    if version == "v1.0":
        model_dir = os.path.join(musetalk_dir, "models/musetalk")
        model_file = os.path.join(model_dir, "pytorch_model.bin")
        config_file = os.path.join(model_dir, "musetalk.json")
    elif version == "v1.5":
        model_dir = os.path.join(musetalk_dir, "models/musetalkV15")
        model_file = os.path.join(model_dir, "unet.pth")
        config_file = os.path.join(model_dir, "musetalk.json")
    else:
        print(f"错误: 不支持的版本: {version}")
        return False

    # 检查模型目录
    if not os.path.exists(model_dir):
        print(f"错误: 模型目录不存在: {model_dir}")
        print("提示: 请下载 MuseTalk 模型权重并放置到正确位置")
        return False

    # 检查模型文件
    if not os.path.exists(model_file):
        print(f"错误: 模型文件不存在: {model_file}")
        print("提示: 请从官方渠道下载模型权重")
        return False

    # 检查配置文件
    if not os.path.exists(config_file):
        print(f"错误: 配置文件不存在: {config_file}")
        return False

    # 检查推理配置
    inference_config = os.path.join(
        musetalk_dir, "configs/inference/test.yaml")
    if not os.path.exists(inference_config):
        print(f"错误: 推理配置文件不存在: {inference_config}")
        return False

    print("✓ MuseTalk 安装检查完成，未发现问题")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="检查 MuseTalk 安装")
    parser.add_argument("--dir", type=str,
                        default=MUSETALK_DIR, help="MuseTalk 目录路径")
    parser.add_argument("--version", type=str, default="v1.0",
                        choices=["v1.0", "v1.5"], help="MuseTalk 版本")

    args = parser.parse_args()

    result = check_musetalk_installation(args.dir, args.version)
    sys.exit(0 if result else 1)
