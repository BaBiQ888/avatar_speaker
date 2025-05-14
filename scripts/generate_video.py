import argparse
from app.lip_sync import lip_sync
import os


def main(image_path, audio_path, output_path, model_path):
    """
    调用 Wav2Lip 推理脚本，将图片和音频合成为视频。
    这里假设你已下载 Wav2Lip 官方仓库的 inference.py 脚本到 scripts/wav2lip_inference.py
    """
    assert os.path.exists(model_path), f"模型权重未找到: {model_path}"
    assert os.path.exists(image_path), f"图片未找到: {image_path}"
    assert os.path.exists(audio_path), f"音频未找到: {audio_path}"

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    lip_sync(image_path, audio_path, output_path, model_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="图片+音频生成口型视频 (Wav2Lip)")
    parser.add_argument('--image', type=str,
                        default="../input/reference_image.jpg", help="输入图片路径")
    parser.add_argument('--audio', type=str,
                        default="../output/tts_output.wav", help="输入音频路径")
    parser.add_argument('--output', type=str,
                        default="../output/wav2lip_output.mp4", help="输出视频路径")
    parser.add_argument('--model', type=str,
                        default="../models/wav2lip.pth", help="Wav2Lip 模型权重路径")
    args = parser.parse_args()

    main(args.image, args.audio, args.output, args.model)
