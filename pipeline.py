import os
import argparse
from app.tts import tts
from app.lip_sync import lip_sync
from app.av_merge import merge
from app.config import WAV2LIP_MODEL_PATH


def main(text_path, image_path, output_dir, model_path):
    os.makedirs(output_dir, exist_ok=True)
    tts_out = os.path.join(output_dir, 'tts_output.wav')
    video_out = os.path.join(output_dir, 'wav2lip_output.mp4')
    final_out = os.path.join(output_dir, 'final_output.mp4')

    print("[PIPELINE] 步骤1：文本转语音 (TTS)")
    tts(text_path, tts_out)
    print("[PIPELINE] 步骤2：口型视频生成 (Wav2Lip)")
    lip_sync(image_path, tts_out, video_out, model_path)
    print("[PIPELINE] 步骤3：音视频合成 (ffmpeg)")
    merge(video_out, tts_out, final_out)
    print(f"[PIPELINE] 全部完成！最终视频: {final_out}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="数字人口型视频一键流水线")
    parser.add_argument('--text', type=str,
                        default="input/input_text.txt", help="输入文本文件路径")
    parser.add_argument('--image', type=str,
                        default="input/reference_image.jpg", help="输入图片路径")
    parser.add_argument('--output_dir', type=str,
                        default="output/", help="输出目录")
    parser.add_argument('--model', type=str,
                        default=WAV2LIP_MODEL_PATH, help="Wav2Lip 模型权重路径")
    args = parser.parse_args()

    main(args.text, args.image, args.output_dir, args.model)
