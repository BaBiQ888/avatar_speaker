import subprocess
import os
import sys


def musetalk_sync(image_path, audio_path, output_path, musetalk_dir="external/MuseTalk"):
    result_dir = os.path.dirname(output_path)
    os.makedirs(result_dir, exist_ok=True)
    cmd = [
        sys.executable, os.path.join(musetalk_dir, "app.py"),
        "--inference",
        "--source_image", image_path,
        "--driven_audio", audio_path,
        "--result_dir", result_dir
    ]
    print(f"[MuseTalk] Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
    # MuseTalk 默认输出名为 result.mp4，可重命名为 output_path
    result_file = os.path.join(result_dir, "result.mp4")
    if os.path.exists(result_file):
        os.rename(result_file, output_path)
    else:
        raise FileNotFoundError(f"MuseTalk output not found: {result_file}")
