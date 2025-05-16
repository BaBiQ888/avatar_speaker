#!/usr/bin/env python3
"""
MuseTalk 安装与配置脚本
此脚本帮助用户设置和配置 MuseTalk
"""

import os
import sys
import argparse
import subprocess
from app.config import MUSETALK_DIR


def setup_musetalk(musetalk_dir=MUSETALK_DIR, version="v1.0", force=False):
    """设置 MuseTalk 环境"""
    print(f"开始设置 MuseTalk (版本: {version})...")

    # 创建外部模块目录
    os.makedirs(os.path.dirname(musetalk_dir), exist_ok=True)

    # 检查目录是否已存在
    if os.path.exists(musetalk_dir) and not force:
        print(f"MuseTalk 目录已存在: {musetalk_dir}")
        print("如需重新安装，请添加 --force 参数")
        return False

    # 克隆仓库
    if force and os.path.exists(musetalk_dir):
        print(f"移除现有 MuseTalk 目录: {musetalk_dir}")
        import shutil
        shutil.rmtree(musetalk_dir)

    print("克隆 MuseTalk 仓库...")
    try:
        subprocess.run([
            "git", "clone", "https://github.com/netease-youdao/MuseTalk.git", musetalk_dir
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"克隆仓库失败: {e}")
        return False

    # 创建模型目录
    if version == "v1.0":
        model_dir = os.path.join(musetalk_dir, "models/musetalk")
    elif version == "v1.5":
        model_dir = os.path.join(musetalk_dir, "models/musetalkV15")
    else:
        print(f"不支持的版本: {version}")
        return False

    os.makedirs(model_dir, exist_ok=True)

    # 提示下载模型文件
    print("\n=== MuseTalk 仓库克隆完成 ===")
    print(f"请从 MuseTalk 官方渠道下载模型文件并放置到: {model_dir}")

    if version == "v1.0":
        print("\n下载模型文件并放置如下文件:")
        print(f" - {model_dir}/pytorch_model.bin")
        print(f" - {model_dir}/musetalk.json")
    elif version == "v1.5":
        print("\n下载模型文件并放置如下文件:")
        print(f" - {model_dir}/unet.pth")
        print(f" - {model_dir}/musetalk.json")

    print("\nMuseTalk 环境设置完成")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="设置 MuseTalk 环境")
    parser.add_argument("--dir", type=str,
                        default=MUSETALK_DIR, help="MuseTalk 安装目录")
    parser.add_argument("--version", type=str, default="v1.0",
                        choices=["v1.0", "v1.5"], help="MuseTalk 版本")
    parser.add_argument("--force", action="store_true", help="强制重新安装")

    args = parser.parse_args()

    result = setup_musetalk(args.dir, args.version, args.force)
    sys.exit(0 if result else 1)
