import os
import re
import subprocess
import time

# 1. Download Cloudflare Tunnel binary if missing
if not os.path.exists("cloudflared"):
  print("Downloading Cloudflare Tunnel client...")
  subprocess.run([
      "wget",
      "-q",
      "-O",
      "cloudflared",
      "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64",
  ])
  subprocess.run(["chmod", "+x", "cloudflared"])

# 2. Start Streamlit Server in Background
print("Launching Streamlit Server...")
subprocess.Popen([
    "streamlit",
    "run",
    "app.py",
    "--server.port=8501",
    "--server.enableCORS=false",
    "--server.enableXsrfProtection=false",
])
time.sleep(3)

# 3. Expose via Cloudflare Tunnel
print("Establishing Public Tunnel...")
proc = subprocess.Popen(
    ["./cloudflared", "tunnel", "--url", "http://localhost:8501"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
)

for line in proc.stdout:
  match = re.search(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", line)
  if match:
    print(
        f"\n======================================================\n🎉 YOUR"
        f" LIVE DASHBOARD IS AT:\n{match.group(0)}\n======================================================\n"
    )
    break
