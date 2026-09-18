
import subprocess, os

# Check SSH keys
r = subprocess.run('ls ~/.ssh/ 2>/dev/null', shell=True, capture_output=True, text=True)
print("SSH keys:", r.stdout.strip())

# Check git credential store
r2 = subprocess.run('git config --global --list 2>/dev/null | grep -E "credential|user|url"', 
                    shell=True, capture_output=True, text=True)
print("Git config:", r2.stdout.strip()[:500])

# Try SSH test to GitHub
r3 = subprocess.run('ssh -T -o StrictHostKeyChecking=no -o ConnectTimeout=5 git@github.com 2>&1 | head -3',
                    shell=True, capture_output=True, text=True, timeout=10)
print("SSH GitHub test:", r3.stdout.strip(), r3.stderr.strip())

# Check .netrc / credentials
for f in ['/home/ubuntu/.netrc', '/home/ubuntu/.git-credentials']:
    if os.path.exists(f):
        print(f"Found: {f}")
    else:
        print(f"Not found: {f}")
