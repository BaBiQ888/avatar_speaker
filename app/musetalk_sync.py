import subprocess
import os
import sys
import shutil
from scripts.check_musetalk import check_musetalk_installation
from app.config import MUSETALK_CONFIG, MUSETALK_INFERENCE


def musetalk_sync(image_path, audio_path, output_path, musetalk_dir="external/MuseTalk", version="v1.0",
                  bbox_shift=None, use_float16=None, fps=None):
    """
    基于 MuseTalk 官方 inference.sh 优化实现的口型同步函数

    Args:
        image_path (str): 输入图片路径
        audio_path (str): 输入音频路径
        output_path (str): 输出视频路径
        musetalk_dir (str): MuseTalk 目录路径
        version (str): 版本, v1.0 或 v1.5
        bbox_shift (int, optional): 嘴部区域调整，正值增加嘴部开度，负值减少嘴部开度
        use_float16 (bool, optional): 是否使用半精度推理以节省显存
        fps (int, optional): 生成视频的帧率
    """
    # 检查 MuseTalk 安装
    if not check_musetalk_installation(musetalk_dir, version):
        raise RuntimeError("MuseTalk 安装检查失败，请确保正确安装")

    # 检查版本并获取配置
    if version not in MUSETALK_CONFIG:
        raise ValueError(
            f"不支持的 MuseTalk 版本: {version}，支持的版本: {list(MUSETALK_CONFIG.keys())}")

    # 获取版本特定配置
    version_config = MUSETALK_CONFIG[version]

    # 获取推理参数，优先使用传入的参数
    bbox_shift = bbox_shift if bbox_shift is not None else MUSETALK_INFERENCE['bbox_shift']
    use_float16 = use_float16 if use_float16 is not None else MUSETALK_INFERENCE[
        'use_float16']
    fps = fps if fps is not None else MUSETALK_INFERENCE['fps']

    result_dir = os.path.dirname(output_path)
    os.makedirs(result_dir, exist_ok=True)

    # 切换工作目录到 MuseTalk 目录
    current_dir = os.getcwd()
    musetalk_abs_dir = os.path.abspath(musetalk_dir)

    # 检查 MuseTalk 目录是否存在
    if not os.path.exists(musetalk_abs_dir):
        raise FileNotFoundError(f"MuseTalk 目录未找到: {musetalk_abs_dir}")

    try:
        # 准备输入目录
        data_dir = os.path.join(musetalk_abs_dir, "data")
        video_dir = os.path.join(data_dir, "video")
        audio_dir = os.path.join(data_dir, "audio")

        os.makedirs(video_dir, exist_ok=True)
        os.makedirs(audio_dir, exist_ok=True)

        # 结果目录
        results_dir = os.path.join(musetalk_abs_dir, "results", "test")
        os.makedirs(results_dir, exist_ok=True)

        # 提取文件名，不包含扩展名
        image_basename = os.path.splitext(os.path.basename(image_path))[0]
        audio_basename = os.path.splitext(os.path.basename(audio_path))[0]

        # 复制输入文件到 MuseTalk 目录结构
        input_image = os.path.join(video_dir, f"{image_basename}.jpg")
        input_audio = os.path.join(audio_dir, f"{audio_basename}.wav")

        print(f"[MuseTalk] 复制输入文件: {image_path} -> {input_image}")
        shutil.copy(image_path, input_image)
        print(f"[MuseTalk] 复制输入文件: {audio_path} -> {input_audio}")
        shutil.copy(audio_path, input_audio)

        # 创建或修改配置文件 - 使用官方格式
        config_dir = os.path.join(musetalk_abs_dir, "configs", "inference")
        os.makedirs(config_dir, exist_ok=True)

        test_config = os.path.join(config_dir, "test.yaml")
        with open(test_config, 'w', encoding='utf-8') as f:
            f.write('task_0:\n')
            f.write(f' video_path: "data/video/{image_basename}.jpg"\n')
            f.write(f' audio_path: "data/audio/{audio_basename}.wav"\n')

            # 添加可选参数
            if bbox_shift != 0:  # 只有当非零时才添加
                f.write(f' bbox_shift: {bbox_shift}\n')

            if fps != 25:  # 只有当不是默认帧率时才添加
                f.write(f' fps: {fps}\n')

        # 设置版本相关路径
        model_dir = version_config['model_dir']
        unet_model_path = f"{model_dir}/{version_config['model_file']}"
        unet_config = f"{model_dir}/{version_config['config_file']}"
        version_arg = version_config['version_arg']

        # 切换到 MuseTalk 目录
        os.chdir(musetalk_abs_dir)

        # 构建命令 - 使用官方推荐的命令格式
        cmd = []
        if os.name == 'nt':  # Windows
            cmd = [
                sys.executable,
                "-m", "scripts.inference",
                "--inference_config", "configs/inference/test.yaml",
                "--result_dir", "results/test",
                "--unet_model_path", unet_model_path,
                "--unet_config", unet_config,
                "--version", version_arg
            ]

            # 添加半精度选项
            if use_float16:
                cmd.append("--use_float16")

        else:  # Linux
            # 使用 bash 脚本运行
            shell_script_path = os.path.join(musetalk_abs_dir, "inference.sh")
            if os.path.exists(shell_script_path):
                # 使用脚本时不能直接传递额外参数，所以只能使用一个脚本
                cmd = ["bash", "inference.sh",
                       version.lower().replace("v", ""), "normal"]
            else:
                # 如果没有 shell 脚本，直接调用 Python 模块
                cmd = [
                    sys.executable,
                    "-m", "scripts.inference",
                    "--inference_config", "configs/inference/test.yaml",
                    "--result_dir", "results/test",
                    "--unet_model_path", unet_model_path,
                    "--unet_config", unet_config,
                    "--version", version_arg
                ]

                # 添加半精度选项
                if use_float16:
                    cmd.append("--use_float16")

        print(f"[MuseTalk] 运行命令: {' '.join(cmd)}")

        try:
            result = subprocess.run(
                cmd, check=True, capture_output=True, text=True)
            print(f"[MuseTalk] 命令执行成功")
            if result.stdout:
                print(f"[MuseTalk] 输出: {result.stdout[:500]}...")
        except subprocess.CalledProcessError as e:
            print(f"[MuseTalk] 错误: {e}")
            if e.stdout:
                print(f"[MuseTalk] 输出: {e.stdout}")
            if e.stderr:
                print(f"[MuseTalk] 错误输出: {e.stderr}")
            raise RuntimeError(f"MuseTalk 执行失败: {e.stderr}")

        # 查找结果视频
        result_mp4 = os.path.join(results_dir, "result.mp4")
        if os.path.exists(result_mp4):
            shutil.copy(result_mp4, output_path)
            print(f"[MuseTalk] 成功生成视频: {output_path}")
        else:
            # 如果没有 result.mp4，查找其他可能的输出文件
            mp4_files = []
            for root, _, files in os.walk(results_dir):
                mp4_files.extend([os.path.join(root, f)
                                 for f in files if f.endswith('.mp4')])

            if mp4_files:
                print(f"[MuseTalk] 找到其他视频文件: {mp4_files}")
                shutil.copy(mp4_files[0], output_path)
                print(f"[MuseTalk] 使用替代文件: {mp4_files[0]} -> {output_path}")
            else:
                raise FileNotFoundError(
                    f"MuseTalk 没有生成任何视频文件，检查 {results_dir} 目录")

    finally:
        # 恢复原工作目录
        os.chdir(current_dir)

        # 可以选择清理临时文件，取决于是否需要保留调试信息
        # 如果需要清理，取消下面的注释
        # shutil.rmtree(os.path.join(video_dir, image_basename + ".jpg"), ignore_errors=True)
        # shutil.rmtree(os.path.join(audio_dir, audio_basename + ".wav"), ignore_errors=True)
