
import subprocess
for cmd in ['which git', 'which gh', 'ls /usr/local/bin/ | grep -E "git|gh"', 'ls /home/ubuntu/.local/bin/ | grep -E "git|gh"']:
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(f"{cmd}: '{r.stdout.strip()}' err='{r.stderr.strip()}'")
