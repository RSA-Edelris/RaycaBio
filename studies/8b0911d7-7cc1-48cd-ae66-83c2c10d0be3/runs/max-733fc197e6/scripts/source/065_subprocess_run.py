
import subprocess
result = subprocess.run(
    ['/home/ubuntu/rayca-runtime/.venv/bin/python3',
     '/home/ubuntu/rayca-sessions/8b0911d7-7cc1-48cd-ae66-83c2c10d0be3-c43f8bb507fc/mmgbsa_calc.py'],
    capture_output=True, text=True, timeout=900
)
print("STDOUT:\n", result.stdout[-12000:] if len(result.stdout) > 12000 else result.stdout)
print("\nSTDERR (last 1000):\n", result.stderr[-1000:] if len(result.stderr) > 1000 else result.stderr)
print("\nReturn code:", result.returncode)
