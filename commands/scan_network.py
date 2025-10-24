import os
print("[SCAN] Running Nmap scan on local subnet...")
os.system("nmap -sP 192.168.1.0/24")
