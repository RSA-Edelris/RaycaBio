
import subprocess, os

# Check for GitHub token
for var in ['GITHUB_TOKEN', 'GH_TOKEN', 'GITHUB_PAT']:
    val = os.environ.get(var, '')
    print(f"{var}: {'SET (' + str(len(val)) + ' chars)' if val else 'not set'}")

# Check for existing RaycaBio clone
r = subprocess.run('find /home/ubuntu -maxdepth 4 -name ".git" -type d 2>/dev/null', 
                   shell=True, capture_output=True, text=True, timeout=10)
print("\nGit repos found:")
print(r.stdout[:1000])
