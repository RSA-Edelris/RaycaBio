
import sys, subprocess
print("Session Python:", sys.executable)
print("Version:", sys.version)
# Try running prep script with session python directly
r = subprocess.run([sys.executable, '--version'], capture_output=True, text=True)
print(r.stdout, r.stderr)
