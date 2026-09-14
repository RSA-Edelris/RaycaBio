
import subprocess, sys

r = subprocess.run([sys.executable, '-m', 'boltz', 'predict', '--help'],
                   capture_output=True, text=True, timeout=30)
# help may go to stderr for some CLI frameworks
print("STDOUT:", r.stdout[:2000])
print("STDERR:", r.stderr[:2000])
print("RC:", r.returncode)
