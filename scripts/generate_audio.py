import argparse
from app.tts import tts
import os


def main(text_path, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    tts(text_path, output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="文本转语音 (Bark)")
    parser.add_argument('--text', type=str,
                        default="../input/input_text.txt", help="输入文本文件路径")
    parser.add_argument('--output', type=str,
                        default="../output/tts_output.wav", help="输出音频文件路径")
    args = parser.parse_args()
    main(args.text, args.output)
