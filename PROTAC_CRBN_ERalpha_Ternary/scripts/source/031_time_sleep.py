
import time, os

time.sleep(60)   # give boltz time to import + start processing

with open(LOG_FILE) as f:
    content = f.read()

print(f"Log ({len(content)} bytes):\n{content[:3000]}")

# Check process alive
import subprocess
r = subprocess.run(['ps', '-p', '3601076', '-o', 'pid,stat,etime,cmd', '--no-headers'],
                   capture_output=True, text=True)
print("\nProcess:", r.stdout.strip() or "NOT FOUND")

# List output dir
if os.path.exists(OUT_DIR):
    for root, dirs, files in os.walk(OUT_DIR):
        for fn in files:
            fp = os.path.join(root, fn)
            print(f"  {fp} ({os.path.getsize(fp)} bytes)")
