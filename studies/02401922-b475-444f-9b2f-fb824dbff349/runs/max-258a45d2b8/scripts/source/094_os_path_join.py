
import subprocess, os, time

wd = "/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a"
script_path = os.path.join(wd, "run_mmgbsa.py")
log_path = os.path.join(wd, "mmgbsa_run.log")

proc = subprocess.Popen(
    ['/usr/bin/python3', script_path],
    stdout=open(log_path, 'w'), stderr=subprocess.STDOUT
)
print(f"PID {proc.pid}, log: {log_path}")

# Wait 30s to confirm first compound starts
time.sleep(30)
with open(log_path) as f:
    print(f.read())
