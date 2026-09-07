
import subprocess
VENV_PY = "/home/ubuntu/rayca-runtime/.venv/bin/python3"
BASE    = "/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e"

r = subprocess.run(
    [VENV_PY, f"{BASE}/prep_enantio2.py"],
    capture_output=True, text=True, timeout=600
)
print(r.stdout)
if r.stderr:
    print("STDERR:", r.stderr[-600:])
print("return code:", r.returncode)
