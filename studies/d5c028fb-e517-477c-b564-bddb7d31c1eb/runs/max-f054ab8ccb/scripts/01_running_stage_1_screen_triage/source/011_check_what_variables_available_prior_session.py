
# Check what variables are available from the prior session
print("all_cpds type:", type(all_cpds) if 'all_cpds' in dir() else "NOT IN SCOPE")
print("actives:", type(actives) if 'actives' in dir() else "NOT IN SCOPE")

# List the session files
import os
wd = '/home/ubuntu/rayca-sessions/d5c028fb-e517-477c-b564-bddb7d31c1eb-396fce89620d'
files = sorted(os.listdir(wd))
for f in files:
    sz = os.path.getsize(os.path.join(wd, f))
    print(f"  {f:40s}  {sz:>10,} bytes")
