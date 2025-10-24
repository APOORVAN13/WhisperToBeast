import whisper
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import subprocess
import os
import time
from datetime import datetime
from commands import simulated_actions as sim

# Load Whisper model
model = whisper.load_model("base")
DURATION = 4
SAMPLE_RATE = 16000
TEMP_WAV = "temp.wav"
LOGFILE = "logs/command_log.txt"

keyword_actions = {
    "reverse connection": lambda: subprocess.call(["/bin/bash", "commands/payload.sh"]),
    "scan network": lambda: subprocess.call(["python3", "commands/scan_network.py"]),
    "start keylogger": lambda: subprocess.call(["python3", "commands/keylogger.py"]),
    "shutdown system": lambda: subprocess.call(["shutdown", "now"]),
    "simulate credential dump": sim.simulate_credential_dump,
    "simulate privilege escalate": sim.simulate_privilege_escalation,
    "simulate persistence": sim.simulate_persistence,
    "simulate exfiltrate data": sim.simulate_data_exfiltration,
    "simulate ransomware": sim.simulate_ransomware,
    "decrypt files": sim.simulated_decrypt_ransomware,
    "simulate usb keylogger": sim.simulate_usb_keylogger,
    "simulate screen capture": sim.simulate_screen_capture,
    "simulate clipboard hijack": sim.simulate_clipboard_hijack,

}

def log(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    os.makedirs("logs", exist_ok=True)
    with open(LOGFILE, "a") as f:
        f.write(f"{timestamp} {message}\n")
    print(f"{timestamp} {message}")

def record_audio():
    audio = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='float32')
    sd.wait()
    write(TEMP_WAV, SAMPLE_RATE, np.squeeze(audio))

def transcribe():
    result = model.transcribe(TEMP_WAV)
    return result["text"].strip().lower()

def match_command(text):
    for keyword in keyword_actions:
        if keyword in text:
            log(f"🎯 Triggered: {keyword}")
            try:
                keyword_actions[keyword]()
                log(f"✅ Executed: {keyword}")
            except Exception as e:
                log(f"❌ Error: {e}")
            return
    log("⚠️ No matching command")

def main():
    log("🟢 Voice trigger listener started")
    try:
        while True:
            record_audio()
            command = transcribe()
            log(f"🎙️ Transcribed: {command}")
            match_command(command)
            time.sleep(1)
    except KeyboardInterrupt:
        log("🔴 Listener stopped")

if __name__ == "__main__":
    main()
