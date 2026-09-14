
import subprocess, time

# Wait 20s for imports to load, then check log
time.sleep(20)

with open(LOG_FILE) as f:
    content = f.read()

print(f"Log so far ({len(content)} chars):\n{content[:3000]}")

# Check if process still alive
import psutil
try:
    p = psutil.Process(3597666)
    print(f"\nProcess status: {p.status()}, CPU%: {p.cpu_percent(interval=1)}")
except Exception as e:
    print(f"Process check error: {e}")
