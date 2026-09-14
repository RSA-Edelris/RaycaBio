
import subprocess, sys, os

# Find boltz binary
venv_bin = os.path.dirname(sys.executable)
boltz_bin = os.path.join(venv_bin, 'boltz')
print(f"Looking for boltz at: {boltz_bin}, exists: {os.path.exists(boltz_bin)}")

# Check session-libs bin
session_lib_root = os.path.dirname(boltz_dir)  # /home/ubuntu/rayca-sessions/.session-libs/...
parent = os.path.dirname(session_lib_root)
print(f"Session lib root: {session_lib_root}")
print(f"Parent: {parent}")
r = subprocess.run(['find', parent, '-name', 'boltz', '-type', 'f'], 
                   capture_output=True, text=True, timeout=10)
print("Found:", r.stdout.strip())

# Also check predict subcommand help directly via Python
r2 = subprocess.run([sys.executable, '-c',
    'from boltz.main import cli; ctx=cli.make_context("boltz", ["predict","--help"])',
    ], capture_output=True, text=True, timeout=10)
print("Help:", r2.stdout[:1500], r2.stderr[:500])
