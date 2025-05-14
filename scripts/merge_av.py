import argparse
from app.av_merge import merge
import os


def main(video_path, audio_path, output_path):
    assert os.path.exists(video_path), f"视频未找到: {video_path}"
    assert os.path.exists(audio_path), f"音频未找到: {audio_path}"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    merge(video_path, audio_path, output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="合成视频和音频为最终输出视频")
    parser.add_argument('--video', type=str,
                        default="../output/wav2lip_output.mp4", help="输入视频路径")
    parser.add_argument('--audio', type=str,
                        default="../output/tts_output.wav", help="输入音频路径")
    parser.add_argument('--output', type=str,
                        default="../output/final_output.mp4", help="输出视频路径")
    args = parser.parse_args()

    main(args.video, args.audio, args.output)
