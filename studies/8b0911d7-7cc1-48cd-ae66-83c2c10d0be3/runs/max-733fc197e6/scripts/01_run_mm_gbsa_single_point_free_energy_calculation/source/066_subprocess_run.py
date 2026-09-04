
import subprocess
result = subprocess.run(
    ['/home/ubuntu/rayca-runtime/.venv/bin/python3',
     '/home/ubuntu/rayca-sessions/8b0911d7-7cc1-48cd-ae66-83c2c10d0be3-c43f8bb507fc/mmgbsa_calc.py'],
    capture_output=True, text=True, timeout=900
)
print("STDOUT (last 4000):\n", result.stdout[-4000:])
print("\nSTDERR (last 3000):\n", result.stderr[-3000:])
print("\nReturn code:", result.returncode)
