import subprocess
import os
import sys


def musetalk_sync(image_path, audio_path, output_path, musetalk_dir="external/MuseTalk"):
    result_dir = os.path.dirname(output_path)
    os.makedirs(result_dir, exist_ok=True)

    # 检查 MuseTalk 是否存在
    app_path = os.path.join(musetalk_dir, "app.py")
    if not os.path.exists(app_path):
        raise FileNotFoundError(
            f"MuseTalk app.py 未找到: {app_path}，请确认 external/MuseTalk 目录已正确下载")

    cmd = [
        sys.executable, app_path,
        "--inference",
        "--cpu_only",
        "--source_image", image_path,
        "--driven_audio", audio_path,
        "--result_dir", result_dir
    ]
    print(f"[MuseTalk] Running: {' '.join(cmd)}")
    print(f"[MuseTalk] 检查目录: musetalk_dir={os.path.abspath(musetalk_dir)}")
    print(
        f"[MuseTalk] 检查输入: image={os.path.exists(image_path)}, audio={os.path.exists(audio_path)}")

    try:
        result = subprocess.run(
            cmd, check=True, capture_output=True, text=True)
        print(f"[MuseTalk] 命令执行成功")
        if result.stdout:
            print(f"[MuseTalk] 输出: {result.stdout[:500]}...")
    except subprocess.CalledProcessError as e:
        print(f"[MuseTalk] 错误: {e}")
        print(f"[MuseTalk] 输出: {e.stdout}")
        print(f"[MuseTalk] 错误输出: {e.stderr}")
        raise RuntimeError(f"MuseTalk 执行失败: {e.stderr}")

    # MuseTalk 默认输出名为 result.mp4，可重命名为 output_path
    result_file = os.path.join(result_dir, "result.mp4")
    if os.path.exists(result_file):
        os.rename(result_file, output_path)
        print(f"[MuseTalk] 成功生成视频: {output_path}")
    else:
        print(f"[MuseTalk] 警告: 预期输出文件不存在: {result_file}")
        # 查找目录下是否有其他视频文件
        mp4_files = [f for f in os.listdir(result_dir) if f.endswith('.mp4')]
        if mp4_files:
            print(f"[MuseTalk] 找到其他视频文件: {mp4_files}")
            # 使用第一个找到的视频文件
            alt_file = os.path.join(result_dir, mp4_files[0])
            os.rename(alt_file, output_path)
            print(f"[MuseTalk] 使用替代文件: {alt_file} -> {output_path}")
        else:
            print(f"[MuseTalk] 目录内容: {os.listdir(result_dir)}")
            raise FileNotFoundError(f"MuseTalk 没有生成任何视频文件: {result_dir}")
