
import re
from pathlib import Path

# Read formal charges from V2000 SDF files
# V2000 SDF: charge is encoded in atom block column 39 (CHG field in the M  CHG line)
# Also check Atom charge field in atom block (column 38-39 in fixed-width format)

def read_net_charge_sdf(sdf_path):
    """Read net formal charge from a V2000 or V3000 SDF file."""
    text = Path(sdf_path).read_text()
    # V2000: M  CHG lines: M  CHGnn aa cc bb dd ...  (aa=atom, cc=charge pairs)
    chg_lines = [l for l in text.split("\n") if l.startswith("M  CHG")]
    if chg_lines:
        total = 0
        for line in chg_lines:
            parts = line.split()
            # M  CHG  n  a1 c1 a2 c2 ...
            n = int(parts[2])
            for i in range(n):
                total += int(parts[4 + i*2])
        return total
    # V3000: M  V30 ATOM ... CHG=n
    chg3 = re.findall(r'CHG=(-?\d+)', text)
    if chg3:
        return sum(int(c) for c in chg3)
    return 0

# Check all 32 best-pose SDF files for formal charges
print(f"{'Ligand':<30} {'nc':>3}  {'electrons note'}")
print("-"*55)
for name in names:
    sdf = f"{WORK}/best_poses/{name}_pose1.sdf"
    nc = read_net_charge_sdf(sdf)
    # Count total electrons: C=6,N=7,O=8,H=1,S=16,F=9,Cl=17,Br=35
    text = Path(sdf).read_text()
    # Count atom symbols from SDF atom block (V2000 format, col 31-33)
    elem_count = {}
    in_atom_block = False
    atom_count = 0
    for line in text.split("\n"):
        if re.match(r'^\s*\d+\s+\d+\s+', line) and len(line) > 38:
            # Atom line in V2000 block
            elem = line[31:34].strip()
            elem_count[elem] = elem_count.get(elem, 0) + 1
    # Use simpler rdkit approach
    try:
        from rdkit import Chem
        mol = Chem.SDMolSupplier(sdf, sanitize=False, removeHs=False)[0]
        if mol:
            from rdkit.Chem import Descriptors
            ne = sum(atom.GetAtomicNum() for atom in mol.GetAtoms())
            ne += nc  # electrons = sum(Z) - charge (for neutral: sum(Z)=n_electrons)
            odd = "ODD" if (ne - nc) % 2 != 0 else ""
            print(f"{name:<30} {nc:>3}  e={ne-nc} {odd}")
    except Exception as e:
        print(f"{name:<30} {nc:>3}  rdkit err: {e}")
