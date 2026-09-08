
import subprocess, sys

result = subprocess.run(
    ["/home/ubuntu/rayca-runtime/.venv/bin/python3",
     "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777/make_traj_video.py"],
    capture_output=True, text=True, timeout=300
)
print("STDOUT:", result.stdout[-3000:])
print("STDERR:", result.stderr[-1000:])
print("Return code:", result.returncode)
