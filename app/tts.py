def tts(text_path, output_path):
    from bark import SAMPLE_RATE, generate_audio
    import soundfile as sf
    with open(text_path, 'r', encoding='utf-8') as f:
        text = f.read().strip()
    audio_array = generate_audio(text)
    sf.write(output_path, audio_array, SAMPLE_RATE)
