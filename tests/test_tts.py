import os
from app.tts import tts


def test_tts():
    test_text = "你好，世界！"
    text_path = "tests/test_input.txt"
    output_path = "tests/test_output.wav"
    with open(text_path, "w", encoding="utf-8") as f:
        f.write(test_text)
    tts(text_path, output_path)
    assert os.path.exists(output_path)
    assert os.path.getsize(output_path) > 1000  # 简单判断音频文件非空
    os.remove(text_path)
    os.remove(output_path)
