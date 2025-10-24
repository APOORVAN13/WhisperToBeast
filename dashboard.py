# dashboard.py
from flask import Flask, render_template, jsonify
from commands.simulated_actions import (
    simulate_credential_dump,
    simulate_privilege_escalation,
    simulate_persistence,
    simulate_data_exfiltration,
    simulate_ransomware,
    simulated_decrypt_ransomware,
    simulate_usb_keylogger,
    simulate_screen_capture,
    simulate_clipboard_hijack
)
import os

app = Flask(__name__)
LOGFILE = "logs/command_log.txt"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/logs")
def logs():
    if not os.path.exists(LOGFILE):
        return jsonify([])
    with open(LOGFILE, "r") as f:
        lines = f.readlines()[-100:]
    return jsonify(lines)

@app.route("/trigger/<action>")
def trigger(action):
    try:
        match action:
            case "credential_dump":
                simulate_credential_dump()
            case "privilege_escalation":
                simulate_privilege_escalation()
            case "persistence":
                simulate_persistence()
            case "data_exfiltration":
                simulate_data_exfiltration()
            case "ransomware":
                simulate_ransomware()
            case "decrypt":
                simulated_decrypt_ransomware()
            case "usb_keylogger":
                simulate_usb_keylogger()
            case "screen_capture":
                simulate_screen_capture()
            case "clipboard_hijack":
                simulate_clipboard_hijack()
            case _:
                return jsonify({"status": "unknown"})
        return jsonify({"status": "ok", "action": action})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
