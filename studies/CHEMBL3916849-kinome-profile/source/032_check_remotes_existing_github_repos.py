
import subprocess

# Check remotes of existing GitHub repos
for repo in ['Rayca-Discovery-Scientist-Agents', 'RaycaTIDE', 'Rayca-Agent-Registry']:
    r = subprocess.run(f'git -C /home/ubuntu/{repo} remote -v 2>/dev/null | head -3',
                       shell=True, capture_output=True, text=True)
    print(f"{repo}: {r.stdout.strip()}")

# Check git credential helper globally
r2 = subprocess.run('git config --global credential.helper 2>/dev/null', 
                    shell=True, capture_output=True, text=True)
print(f"\nCredential helper: '{r2.stdout.strip()}'")

# Check if there's a GitHub App token or machine user token in common locations
import os
for loc in ['/etc/github', '/home/ubuntu/.github', '/run/secrets', '/home/ubuntu/.config/gh']:
    if os.path.exists(loc):
        print(f"Found: {loc}: {os.listdir(loc)[:5]}")
