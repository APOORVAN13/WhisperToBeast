import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write

DURATION = 4  # seconds
SAMPLE_RATE = 16000
FILENAME = "temp.wav"

print("🎙️ Recording...")
audio = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='float32')
sd.wait()
write(FILENAME, SAMPLE_RATE, np.squeeze(audio))
print(f"✅ Saved as {FILENAME}")
