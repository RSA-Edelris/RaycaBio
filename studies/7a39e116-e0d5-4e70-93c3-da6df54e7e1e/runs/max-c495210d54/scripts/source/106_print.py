
import subprocess

py  = "/home/ubuntu/rayca-runtime/.venv/bin/python3"
cwd = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777"

print("Rendering trajectory video (pillow GIF, 101 frames)...")
r2 = subprocess.run([py, f"{cwd}/make_traj_video.py"],
                    capture_output=True, text=True, cwd=cwd, timeout=600)
print("=== Video script output ===")
print(r2.stdout)
if r2.returncode != 0:
    print("STDERR:", r2.stderr[-800:])
print(f"rc={r2.returncode}")
