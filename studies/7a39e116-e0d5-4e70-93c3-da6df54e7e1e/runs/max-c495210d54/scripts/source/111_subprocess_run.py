
import subprocess, sys

result = subprocess.run(
    ["/home/ubuntu/rayca-runtime/.venv/bin/python3",
     "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777/extract_final_pose_sdf.py"],
    capture_output=True, text=True, timeout=120
)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr[-500:] if result.stderr else "")
print("Return code:", result.returncode)
