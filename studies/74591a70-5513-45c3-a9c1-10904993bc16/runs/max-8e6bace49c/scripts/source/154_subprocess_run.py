
import subprocess
BASE = "/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e"
VENV_PY = "/home/ubuntu/rayca-runtime/.venv/bin/python3"

result = subprocess.run(
    [VENV_PY, f"{BASE}/build_final_outputs.py"],
    capture_output=True, text=True, cwd=BASE
)
# Print last lines (summary)
lines = result.stdout.strip().splitlines()
for l in lines[-8:]:
    print(l)
if result.returncode != 0:
    print("STDERR:", result.stderr[-500:])
print("RC:", result.returncode)
