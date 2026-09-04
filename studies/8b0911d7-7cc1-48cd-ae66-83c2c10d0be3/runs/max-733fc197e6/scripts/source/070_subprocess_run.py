
import subprocess, os

src  = '/home/ubuntu/rayca-sessions/8b0911d7-7cc1-48cd-ae66-83c2c10d0be3-c43f8bb507fc/docking_report.md'
dst  = '/home/ubuntu/rayca-artifacts/c43f8bb507fc1b0b669eeb63/files/docking_report.md'

r = subprocess.run(['cp', src, dst], capture_output=True, text=True)
print("cp:", r.returncode, r.stderr)
print("Artifact size:", os.path.getsize(dst), "bytes")
