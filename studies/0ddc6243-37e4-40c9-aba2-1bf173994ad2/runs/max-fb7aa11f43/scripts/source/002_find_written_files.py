
import os, glob

# Find the written files
for pattern in ['*.yaml', '*.json', '*.py']:
    for f in glob.glob(f'/home/ubuntu/**/{pattern}', recursive=True):
        print(f)

# Also check cwd
print("\ncwd:", os.getcwd())
for f in os.listdir('.'):
    print(f)
