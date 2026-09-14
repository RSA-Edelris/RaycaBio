
import subprocess, sys

# Check CLI help for available options
r = subprocess.run([sys.executable, '-m', 'boltz', 'predict', '--help'],
                   capture_output=True, text=True, timeout=30)
print(r.stdout[:3000])
