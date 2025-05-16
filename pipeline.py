import os
import argparse
from app.tts import tts
from app.musetalk_sync import musetalk_sync
from app.av_merge import merge
# from app.lip_sync import lip_sync  # 已切换为 MuseTalk
from app.config import WAV2LIP_MODEL_PATH, MUSETALK_DIR, MUSETALK_VERSION, MUSETALK_INFERENCE


def main(text_path, image_path, output_dir, model_path, use_musetalk=True,
         musetalk_dir=MUSETALK_DIR, musetalk_version=MUSETALK_VERSION,
         bbox_shift=MUSETALK_INFERENCE['bbox_shift'],
         use_float16=MUSETALK_INFERENCE['use_float16'],
         fps=MUSETALK_INFERENCE['fps']):
    os.makedirs(output_dir, exist_ok=True)
    tts_out = os.path.join(output_dir, 'tts_output.wav')
    video_out = os.path.join(output_dir, 'musetalk_output.mp4')
    final_out = os.path.join(output_dir, 'final_output.mp4')

    print("[PIPELINE] 步骤1：文本转语音 (TTS)")
    tts(text_path, tts_out)
    print("[PIPELINE] 步骤2：口型视频生成")

    if use_musetalk:
        print(f"[PIPELINE] 使用 MuseTalk {musetalk_version}")
        print(
            f"[PIPELINE] 参数: bbox_shift={bbox_shift}, use_float16={use_float16}, fps={fps}")
        musetalk_sync(image_path, tts_out, video_out,
                      musetalk_dir=musetalk_dir,
                      version=musetalk_version,
                      bbox_shift=bbox_shift,
                      use_float16=use_float16,
                      fps=fps)
    else:
        print("[PIPELINE] 使用 Wav2Lip")
        from app.lip_sync import lip_sync
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
    parser.add_argument('--lip_model', type=str,
                        default="musetalk", help="口型模型类型[musetalk|wav2lip]")
    parser.add_argument('--musetalk_dir', type=str,
                        default=MUSETALK_DIR, help="MuseTalk 目录路径")
    parser.add_argument('--musetalk_version', type=str,
                        default=MUSETALK_VERSION, help="MuseTalk 版本[v1.0|v1.5]")
    parser.add_argument('--bbox_shift', type=int,
                        default=MUSETALK_INFERENCE['bbox_shift'], help="嘴部区域调整，正值增加嘴部开度，负值减少嘴部开度")
    parser.add_argument('--use_float16', action='store_true',
                        default=MUSETALK_INFERENCE['use_float16'], help="是否使用半精度推理以节省显存")
    parser.add_argument('--fps', type=int,
                        default=MUSETALK_INFERENCE['fps'], help="生成视频的帧率")
    args = parser.parse_args()

    # 根据模型类型选择不同的处理流程
    use_musetalk = args.lip_model.lower() == "musetalk"

    main(args.text, args.image, args.output_dir, args.model,
         use_musetalk=use_musetalk,
         musetalk_dir=args.musetalk_dir,
         musetalk_version=args.musetalk_version,
         bbox_shift=args.bbox_shift,
         use_float16=args.use_float16,
         fps=args.fps)
