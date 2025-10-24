# Whispertobeast 🔊🧠

> Voice-Driven Lab Automation & Attack Simulation Toolkit  
> A local AI-powered prototype using OpenAI Whisper to demonstrate simulated offensive cybersecurity workflows — strictly for demo, education, and defensive research.

# Overview

Whispertobeast is an offline, air-gapped, lab-safe project that listens for short voice commands, transcribes them using Whisper, and triggers simulated cybersecurity actions.  
It is built to demonstrate voice-triggered automation, simulation of offensive techniques, and modular threat demos in ethical, controlled environments (e.g., Kali Linux VMs for red team practice or intern showcases).

## 🚨 Disclaimer

This repository includes code capable of performing potentially destructive actions (e.g., file encryption, fake persistence, simulated data exfiltration).  
.Use responsibly and only in safe, offline environments like sandboxed VMs with snapshots.



## ✅ Key Features

- 🎤 Offline voice command listener using OpenAI Whisper
- 🧠 Robust short keyword matching (e.g., `simulate usb keylogger`, `simulate clipboard hijack`, `simulate screen capture`, `simulate credential dump`)
- 💻 Modular simulated actions (screen capture, fake keylog playback, shadow dump, clipboard hijack)
- 📊 Simple Flask dashboard for viewing logs and triggering safe actions manually
- 🗃️ Centralized logging to `logs/command_log.txt`
- 🧪 Completely lab-contained and safe by default

---
## How to View
The full source code is available in `WTB.zip`.
Download and extract to explore.
