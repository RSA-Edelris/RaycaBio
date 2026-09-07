
# Preview LVY reference and receptor first 5 lines
lvy_ref = (BASE / "4CI2_LVY_ref.pdb").read_text()
print("=== 4CI2_LVY_ref.pdb (first 10 lines) ===")
for l in lvy_ref.splitlines()[:10]:
    print(repr(l))

# Check receptor chain structure
rec = (BASE / "4CI2_receptor_for_docking.pdb").read_text()
chains = set()
for l in rec.splitlines():
    if l.startswith(("ATOM","HETATM")):
        chains.add(l[21])
print(f"\nChains in 4CI2_receptor_for_docking.pdb: {sorted(chains)}")

# How many ATOM/HETATM lines?
atom_lines = [l for l in rec.splitlines() if l.startswith("ATOM")]
hetatm_lines = [l for l in rec.splitlines() if l.startswith("HETATM")]
print(f"ATOM: {len(atom_lines)}, HETATM: {len(hetatm_lines)}")

# Check top1 SDF for a sample
from rdkit import Chem
sample = (BASE / "best_poses2_top1" / "Compound_10_ent2_pose1.sdf")
m = Chem.SDMolSupplier(str(sample), removeHs=False)[0]
print(f"\nSample pose (Compound_10_ent2): {m.GetNumAtoms()} atoms, {m.GetNumConformers()} conformers")
