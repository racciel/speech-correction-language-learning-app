import whisper
import sounddevice as sd
import wave
import librosa
import librosa.display
import matplotlib.pyplot as plt
import subprocess
import torch
import numpy as np

def record_audio(filename="./recording/user_audio.wav", duration=5, samplerate=16000):
    """Records audio from the microphone."""
    print("🎤 Recording... Speak now!")
    audio_data = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    print("✅ Recording complete!")

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        wf.writeframes(audio_data.tobytes())

    return filename

def transcribe_audio(filename):
    """Transcribes speech to text using Whisper."""
    model = whisper.load_model("large", device="cpu") #device="cuda" if torch.cuda.is_available() else "cpu")
    result = model.transcribe(filename, language="hr")
    return result["text"]

def text_to_phonemes(text, lang="hr"):
    """Converts text to phonemes using espeak-ng."""
    command = f'espeak-ng -v {lang} -x -s 100 "{text}"'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def compare_pronunciation(correct, user):
    """Compares the correct phonemes with the user's phonemes."""
    correct = correct.split()
    user = user.split()

    errors = [word for word in user if word not in correct]
    accuracy = 100 - (len(errors) / len(correct) * 100) if correct else 0

    return accuracy, errors

def plot_spectrogram(filename):
    """Plots the spectrogram of the recorded speech."""
    y, sr = librosa.load(filename, sr=16000)

    S = librosa.feature.melspectrogram(y=y, sr=sr)
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max),
                             sr=sr, x_axis="time", y_axis="mel")
    plt.colorbar(format="%+2.0f dB")
    plt.title("Spectrogram of Pronunciation")
    plt.show()

if __name__ == "__main__":
    audio_file = record_audio()

    transcribed_text = transcribe_audio(audio_file)
    print(f"📝 You said: {transcribed_text}")

    correct_text = "Dobar dan!"
    correct_phonemes = text_to_phonemes(correct_text, lang="hr")
    user_phonemes = text_to_phonemes(transcribed_text, lang="hr")

    print(f"✅ Correct Pronunciation: {correct_phonemes}")
    print(f"❌ Your Pronunciation: {user_phonemes}")

    accuracy, mistakes = compare_pronunciation(correct_phonemes, user_phonemes)
    print(f"🎯 Pronunciation Accuracy: {accuracy:.2f}%")
    
    if mistakes:
        print(f"⚠️ Mistakes: {mistakes}")
    else:
        print("🎉 Perfect pronunciation!")

    plot_spectrogram(audio_file)
