
import subprocess, os

# ── Check for gnina/vina binaries on PATH ─────────────────────────────────────
for binary in ['gnina', 'smina', 'vina', 'qvina']:
    r = subprocess.run(['which', binary], capture_output=True, text=True)
    if r.returncode == 0:
        print(f"Found: {r.stdout.strip()}")
    else:
        # check common locations
        for loc in [f'/usr/bin/{binary}', f'/usr/local/bin/{binary}',
                    f'/opt/{binary}', f'/opt/rayca/bin/{binary}']:
            if os.path.isfile(loc):
                print(f"Found at: {loc}")

# ── Check run_aidd_tool availability ─────────────────────────────────────────
print("\nChecking run_aidd_tool ...")
try:
    print(f"run_aidd_tool available: {callable(run_aidd_tool)}")
except NameError:
    print("run_aidd_tool not in namespace")
    # try importing
    try:
        from modulon.governance.toolkit import run_aidd_tool as raat
        print(f"Imported from modulon: {callable(raat)}")
    except Exception as e:
        print(f"Import failed: {e}")

# ── Check rayca_toolkit ───────────────────────────────────────────────────────
print("\nrayca_toolkit methods:")
print([m for m in dir(rayca_toolkit) if not m.startswith('_')][:20])
print("\nrayca_tools type:", type(rayca_tools))
