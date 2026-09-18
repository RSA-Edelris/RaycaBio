
import os, glob

print("cwd:", os.getcwd())
cwd_files = os.listdir('.')
print("files in cwd:", cwd_files[:30])

# Look for the yaml/json specifically
for pattern in ['gspt1*.yaml', 'gspt1*.json', '001_run*.py']:
    found = glob.glob(f'./{pattern}') + glob.glob(f'/tmp/{pattern}')
    print(pattern, "->", found)
