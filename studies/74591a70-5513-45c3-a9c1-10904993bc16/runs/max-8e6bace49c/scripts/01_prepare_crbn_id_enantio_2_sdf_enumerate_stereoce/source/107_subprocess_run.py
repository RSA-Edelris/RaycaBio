
import subprocess
BASE = "/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e"
r = subprocess.run(
    ['python3', f'{BASE}/prep_enantio2.py'],
    capture_output=True, text=True, timeout=300
)
print(r.stdout[-4000:] if len(r.stdout) > 4000 else r.stdout)
if r.stderr:
    print("STDERR:", r.stderr[-1000:])
print("return code:", r.returncode)
