
import subprocess

# ── Check converters ──────────────────────────────────────────────────────────
for name in ['meeko', 'openbabel', 'vina', 'AutoDockTools']:
    try:
        __import__(name)
        print(f"  {name}: importable")
    except ImportError:
        pass

# Check obabel command
r = subprocess.run(['which', 'obabel'], capture_output=True, text=True)
print(f"obabel: {r.stdout.strip() or 'not found'}")

# Check meeko command-line tools
for cmd in ['prepare_receptor', 'mk_prepare_ligand.py', 'mk_prepare_receptor.py']:
    r = subprocess.run(['which', cmd], capture_output=True, text=True)
    if r.returncode == 0:
        print(f"  {cmd}: {r.stdout.strip()}")

# vina binary version
vina_bin = '/home/ubuntu/rayca-runtime/.mamba/envs/rayca/bin/vina'
r = subprocess.run([vina_bin, '--version'], capture_output=True, text=True)
print(f"\nVina version: {r.stdout.strip() or r.stderr.strip()}")

# ── Try run_aidd_tool with gnina (test first ligand) ─────────────────────────
print("\nTrying run_aidd_tool for gnina ...")
try:
    r_gnina = run_aidd_tool('gnina', {
        'proteinFile':    trimmed_noh_path,
        'ligandFile':     lig_sdf_paths[0][1],
        'boxX':           pocket_cx,
        'boxY':           pocket_cy,
        'boxZ':           pocket_cz,
        'width':          BOX_SZ,
        'height':         BOX_SZ,
        'depth':          BOX_SZ,
        'numModes':       5,
        'exhaustiveness': 16,
        'cnnScoring':     'rescore',
        'seed':           42,
    })
    print(f"run_aidd_tool gnina rc: {r_gnina.get('rc')}")
    print(f"best_affinity: {r_gnina.get('best_affinity_kcal_mol')}")
except Exception as e:
    print(f"run_aidd_tool gnina failed: {e}")
