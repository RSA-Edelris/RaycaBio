
# Create clean minimal SDF files for gbsa (no extra metadata, just coordinates + name)
from rdkit.Chem import SDWriter, MolFromMolBlock
import gzip

# Re-read from the raw gnina SDF
clean_paths = {}
for i, block in enumerate(blocks[:5]):
    mol = MolFromMolBlock(block, removeHs=True, sanitize=True)  # strip H for acpype
    if mol:
        mol.SetProp("_Name", f"pose_{i+1}")
        # Regenerate Hs properly (needed for charge calc)
        from rdkit.Chem import AddHs
        mol_h = AddHs(mol, addCoords=True)
        path = f"{WS}/clean_pose_{i+1}.sdf"
        w = SDWriter(path)
        w.write(mol_h)
        w.close()
        clean_paths[f"clean_pose_{i+1}.sdf"] = path
        print(f"clean_pose_{i+1}.sdf: {mol_h.GetNumAtoms()} atoms, {mol_h.GetNumBonds()} bonds")

# Also copy receptor
import shutil
clean_paths["1Z5M_receptor_pH7.4.pdb"] = f"{ART}/1Z5M_receptor_pH7.4.pdb"

# Try single pose with em mode and gas charges first
print("\nDispatching gbsa (single pose, em mode, gas charges)...")
result_test = dispatch("gbsa", {
    "task": "protein-ligand",
    "mode": "em",
    "method": "gb",
    "proteinFile": "1Z5M_receptor_pH7.4.pdb",
    "ligandFile": "clean_pose_1.sdf",
    "proteinForceField": "amber03",
    "ligandForceField": "gaff2",
    "ligandCharge": "gas",
    "threads": 8,
    "decompose": False
}, files=clean_paths, gpu=True, timeout=600)

print("rc:", result_test.get("rc"))
print("summary:", result_test.get("summary",""))
out_t = result_test.get("output", {})
print("best_dG:", out_t.get("best_dG_kcal_per_mol"))
print("results:", out_t.get("results","")[:500] if out_t.get("results") else "none")
print("error detail:", result_test.get("error","")[:800])
