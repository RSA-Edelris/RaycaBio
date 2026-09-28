
# Check all env vars for GitHub/git-related tokens
import os
for k, v in sorted(os.environ.items()):
    if any(x in k.upper() for x in ['GIT', 'TOKEN', 'AUTH', 'CRED', 'SECRET', 'KEY', 'RAYCA']):
        print(f"{k}={v[:40]}{'...' if len(v)>40 else ''}")
