
import subprocess

py  = "/home/ubuntu/rayca-runtime/.venv/bin/python3"
cwd = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777"

r = subprocess.run([py, f"{cwd}/extract_final_pose_sdf.py"],
                   capture_output=True, text=True, cwd=cwd, timeout=120)
print(r.stdout)
if r.returncode != 0:
    print("STDERR:", r.stderr[-500:])
print(f"rc={r.returncode}")
