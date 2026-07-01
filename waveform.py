import librosa
import librosa.display
import matplotlib.pyplot as plt

def save_waveform(audio_path):
    y, sr = librosa.load(audio_path, sr=None)

    plt.figure(figsize=(10, 3))
    librosa.display.waveshow(y, sr=sr)
    plt.title("Audio Waveform")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.tight_layout()

    image_path = "waveform.png"
    plt.savefig(image_path)
    plt.close()

    return image_path