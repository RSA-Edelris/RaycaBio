
# Verify fpdf2 is available and get version
import subprocess
r = subprocess.run(['pip', 'show', 'fpdf2'], capture_output=True, text=True)
print(r.stdout or r.stderr)
