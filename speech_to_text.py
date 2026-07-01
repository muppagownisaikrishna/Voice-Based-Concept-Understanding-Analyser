import whisper

model = None

def transcribe_audio(audio_path):
    global model

    if model is None:
        model = whisper.load_model("base")

    result = model.transcribe(audio_path)
    return result["text"]