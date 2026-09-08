
import subprocess

py  = "/home/ubuntu/rayca-runtime/.venv/bin/python3"
cwd = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777"

print("Rendering trajectory GIF (101 frames, ~2 min)...")
r = subprocess.run([py, f"{cwd}/make_traj_video.py"],
                   capture_output=True, text=True, cwd=cwd, timeout=600)
print(r.stdout)
if r.returncode != 0:
    print("STDERR:", r.stderr[-800:])
print(f"rc={r.returncode}")
