
import subprocess, sys

result = subprocess.run(
    [sys.executable, '/home/ubuntu/rayca-modulon-dev/modulon-max/gen_session_pdf_brd4_protac.py'],
    capture_output=True, text=True, timeout=120
)
print("STDOUT:", result.stdout[-3000:] if len(result.stdout) > 3000 else result.stdout)
if result.returncode != 0:
    print("STDERR:", result.stderr[-2000:])
print("Return code:", result.returncode)
