
import subprocess
result = subprocess.run(
    ['/home/ubuntu/rayca-runtime/.venv/bin/python3',
     '/home/ubuntu/rayca-sessions/8b0911d7-7cc1-48cd-ae66-83c2c10d0be3-c43f8bb507fc/mmgbsa_calc.py'],
    capture_output=True, text=True, timeout=600
)
print("STDOUT:\n", result.stdout[-6000:] if len(result.stdout) > 6000 else result.stdout)
print("\nSTDERR:\n", result.stderr[-3000:] if len(result.stderr) > 3000 else result.stderr)
print("\nReturn code:", result.returncode)
