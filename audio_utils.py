import librosa

def load_audio(audio_path):
    audio, sr = librosa.load(audio_path, sr=None)
    return audio, sr

def extract_features(audio_path):
    audio, sr = load_audio(audio_path)

    duration = librosa.get_duration(y=audio, sr=sr)

    zcr = librosa.feature.zero_crossing_rate(audio).mean()

    rms = librosa.feature.rms(y=audio).mean()

    return {
        "Duration": duration,
        "Zero Crossing Rate": zcr,
        "RMS Energy": rms
    }