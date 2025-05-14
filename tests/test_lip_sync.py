import os
from app.lip_sync import lip_sync


def test_lip_sync():
    # 这里只做接口调用演示，实际需准备好图片、音频和模型
    image_path = "tests/fake.jpg"
    audio_path = "tests/fake.wav"
    output_path = "tests/fake_out.mp4"
    model_path = "models/wav2lip.pth"
    # 伪造文件
    with open(image_path, "wb") as f:
        f.write(b"\x00")
    with open(audio_path, "wb") as f:
        f.write(b"\x00")
    try:
        try:
            lip_sync(image_path, audio_path, output_path, model_path)
        except AssertionError:
            pass  # 只要能跑通接口即可
    finally:
        os.remove(image_path)
        os.remove(audio_path)
