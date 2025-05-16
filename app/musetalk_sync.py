import subprocess
import os
import sys
from scripts.check_musetalk import check_musetalk_installation


def musetalk_sync(image_path, audio_path, output_path, musetalk_dir="external/MuseTalk", version="v1.0"):
    """
    基于 MuseTalk 官方 inference.sh 优化实现的口型同步函数

    Args:
        image_path (str): 输入图片路径
        audio_path (str): 输入音频路径
        output_path (str): 输出视频路径
        musetalk_dir (str): MuseTalk 目录路径
        version (str): 版本, v1.0 或 v1.5
    """
    # 检查 MuseTalk 安装
    if not check_musetalk_installation(musetalk_dir, version):
        raise RuntimeError("MuseTalk 安装检查失败，请确保正确安装")

    result_dir = os.path.dirname(output_path)
    os.makedirs(result_dir, exist_ok=True)

    # 切换工作目录到 MuseTalk 目录
    current_dir = os.getcwd()
    musetalk_abs_dir = os.path.abspath(musetalk_dir)

    # 检查 MuseTalk 目录是否存在
    if not os.path.exists(musetalk_abs_dir):
        raise FileNotFoundError(f"MuseTalk 目录未找到: {musetalk_abs_dir}")

    # 设置版本相关路径
    if version == "v1.0":
        model_dir = "models/musetalk"
        unet_model_path = f"{model_dir}/pytorch_model.bin"
        unet_config = f"{model_dir}/musetalk.json"
        version_arg = "v1"
    elif version == "v1.5":
        model_dir = "models/musetalkV15"
        unet_model_path = f"{model_dir}/unet.pth"
        unet_config = f"{model_dir}/musetalk.json"
        version_arg = "v15"
    else:
        raise ValueError("版本必须是 v1.0 或 v1.5")

    # 检查输入文件
    print(
        f"[MuseTalk] 检查输入: image={os.path.exists(image_path)}, audio={os.path.exists(audio_path)}")

    # 复制输入文件到 MuseTalk 目录
    temp_image = os.path.join(musetalk_abs_dir, "temp_input.jpg")
    temp_audio = os.path.join(musetalk_abs_dir, "temp_input.wav")

    try:
        import shutil
        shutil.copy(image_path, temp_image)
        shutil.copy(audio_path, temp_audio)

        # 切换到 MuseTalk 目录
        os.chdir(musetalk_abs_dir)

        # 准备命令参数
        config_path = "./configs/inference/test.yaml"
        result_dir_arg = "./temp_result"
        os.makedirs(result_dir_arg, exist_ok=True)

        # 构建命令
        cmd = [
            sys.executable,
            "-m", "scripts.inference",
            "--inference_config", config_path,
            "--result_dir", result_dir_arg,
            "--unet_model_path", unet_model_path,
            "--unet_config", unet_config,
            "--version", version_arg,
            "--source_image", "./temp_input.jpg",
            "--driven_audio", "./temp_input.wav"
        ]

        print(f"[MuseTalk] 运行命令: {' '.join(cmd)}")

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

        # 查找结果视频并复制回原位置
        result_mp4 = os.path.join(result_dir_arg, "result.mp4")
        if os.path.exists(result_mp4):
            shutil.copy(result_mp4, output_path)
            print(f"[MuseTalk] 成功生成视频: {output_path}")
        else:
            # 查找目录下是否有其他视频文件
            mp4_files = []
            for root, _, files in os.walk(result_dir_arg):
                mp4_files.extend([os.path.join(root, f)
                                 for f in files if f.endswith('.mp4')])

            if mp4_files:
                print(f"[MuseTalk] 找到其他视频文件: {mp4_files}")
                # 使用第一个找到的视频文件
                shutil.copy(mp4_files[0], output_path)
                print(f"[MuseTalk] 使用替代文件: {mp4_files[0]} -> {output_path}")
            else:
                print(f"[MuseTalk] 目录内容: {os.listdir(result_dir_arg)}")
                raise FileNotFoundError(f"MuseTalk 没有生成任何视频文件")

    finally:
        # 清理临时文件
        for temp_file in [temp_image, temp_audio]:
            if os.path.exists(temp_file):
                os.remove(temp_file)

        # 恢复原工作目录
        os.chdir(current_dir)
