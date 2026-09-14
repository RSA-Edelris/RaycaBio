
import subprocess, sys

# Check the entry_points for boltz (console_scripts)
r = subprocess.run([sys.executable, '-c',
    '''
import importlib.metadata
try:
    eps = importlib.metadata.entry_points(group="console_scripts")
    for ep in eps:
        if "boltz" in ep.name.lower() or "boltz" in str(ep.value).lower():
            print(ep.name, "->", ep.value)
except Exception as e:
    print("err:", e)
'''], capture_output=True, text=True)
print("Entry points:", r.stdout.strip())

# Also check main.py head
r2 = subprocess.run(['head', '-80', f'{boltz_dir}/main.py'], capture_output=True, text=True)
print("main.py head:\n", r2.stdout[:2000])
