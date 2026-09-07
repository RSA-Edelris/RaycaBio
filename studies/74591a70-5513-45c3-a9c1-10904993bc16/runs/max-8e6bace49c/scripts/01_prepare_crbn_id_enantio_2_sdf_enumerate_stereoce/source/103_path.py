
from pathlib import Path
import subprocess

BASE = "/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e"
INPUT_SDF = "/home/ubuntu/rayca-artifacts/aa94c8cd626e84050ef1e8e8/files/CRBN_lig_results_2.sdf"

# Count compounds and stereocenters
text = Path(INPUT_SDF).read_text()
compounds = [b for b in text.split("$$$$") if b.strip()]
print(f"Input compounds: {len(compounds)}")
for c in compounds:
    name = c.split('\n')[0].strip()
    sterac_lines = [l for l in c.split('\n') if 'STERAC1' in l]
    cfg_atoms = [l for l in c.split('\n') if 'CFG=' in l]
    print(f"  {name}: STERAC1={sterac_lines[0].strip() if sterac_lines else 'none'}, CFG atoms={len(cfg_atoms)}")

# Check what tools are available
print("\n--- Tool check ---")
for tool in ['obabel']:
    r = subprocess.run(['which', tool], capture_output=True, text=True)
    print(f"  {tool}: {r.stdout.strip() or 'NOT FOUND'}")

# Check rdkit
try:
    from rdkit import Chem
    print(f"  rdkit: available")
except ImportError:
    print(f"  rdkit: NOT available")

# Check LVY ref ligand for box definition
lvy_path = Path(f"{BASE}/4CI2_LVY_ref.pdb")
if lvy_path.exists():
    lvy_text = lvy_path.read_text()
    # Parse atom coordinates
    coords = []
    for line in lvy_text.split('\n'):
        if line.startswith('ATOM') or line.startswith('HETATM'):
            try:
                x, y, z = float(line[30:38]), float(line[38:46]), float(line[46:54])
                coords.append((x,y,z))
            except:
                pass
    if coords:
        cx = sum(c[0] for c in coords)/len(coords)
        cy = sum(c[1] for c in coords)/len(coords)
        cz = sum(c[2] for c in coords)/len(coords)
        print(f"\nLVY center: ({cx:.2f}, {cy:.2f}, {cz:.2f})")
        print(f"LVY atom count: {len(coords)}")
