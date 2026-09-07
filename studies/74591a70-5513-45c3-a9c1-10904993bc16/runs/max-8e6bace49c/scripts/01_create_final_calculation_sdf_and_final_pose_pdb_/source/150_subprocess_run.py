
import subprocess, sys
BASE = "/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e"
VENV_PY = "/home/ubuntu/rayca-runtime/.venv/bin/python3"
result = subprocess.run(
    [VENV_PY, f"{BASE}/build_final_outputs.py"],
    capture_output=True, text=True, cwd=BASE
)
print(result.stdout[-4000:] if len(result.stdout) > 4000 else result.stdout)
if result.stderr:
    print("STDERR:", result.stderr[-2000:])
print("RC:", result.returncode)
