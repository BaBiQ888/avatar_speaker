def lip_sync(image_path, audio_path, output_path, model_path):
    import subprocess
    import os
    assert os.path.exists(model_path), f"模型权重未找到: {model_path}"
    assert os.path.exists(image_path), f"图片未找到: {image_path}"
    assert os.path.exists(audio_path), f"音频未找到: {audio_path}"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cmd = [
        'python', 'scripts/wav2lip_inference.py',
        '--checkpoint_path', model_path,
        '--face', image_path,
        '--audio', audio_path,
        '--outfile', output_path
    ]
    subprocess.run(cmd, check=True)
