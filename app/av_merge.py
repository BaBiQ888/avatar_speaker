def merge(video_path, audio_path, output_path):
    import subprocess
    import os
    assert os.path.exists(video_path), f"视频未找到: {video_path}"
    assert os.path.exists(audio_path), f"音频未找到: {audio_path}"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cmd = [
        'ffmpeg', '-y',
        '-i', video_path,
        '-i', audio_path,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-strict', 'experimental',
        '-shortest',
        output_path
    ]
    subprocess.run(cmd, check=True)
