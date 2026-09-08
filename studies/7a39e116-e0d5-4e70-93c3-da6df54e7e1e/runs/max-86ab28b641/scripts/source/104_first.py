
import subprocess

py  = "/home/ubuntu/rayca-runtime/.venv/bin/python3"
cwd = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777"

# Run SDF extraction first (fast)
r1 = subprocess.run([py, f"{cwd}/extract_final_pose_sdf.py"],
                    capture_output=True, text=True, cwd=cwd, timeout=120)
print("=== SDF extraction ===")
print(r1.stdout)
if r1.returncode != 0:
    print("STDERR:", r1.stderr[-500:])
print(f"rc={r1.returncode}")
