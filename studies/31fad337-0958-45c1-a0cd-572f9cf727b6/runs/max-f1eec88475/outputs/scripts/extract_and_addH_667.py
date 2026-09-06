"""Extract Pose 1 from gnina_docked.sdf.gz for CTX-1020667 and add explicit H."""
import gzip, sys
from pathlib import Path
from rdkit import Chem

GZ_SDF   = Path("/home/ubuntu/rayca-sessions/31fad337-0958-45c1-a0cd-572f9cf727b6-0505c6de016f/gnina_docked.sdf.gz")
BEST_SDF = Path("/home/ubuntu/rayca-sessions/31fad337-0958-45c1-a0cd-572f9cf727b6-0505c6de016f/cdk2_campaign/poses_all/CTX-1020667_best_pose.sdf")
BEST_H   = Path("/home/ubuntu/rayca-sessions/31fad337-0958-45c1-a0cd-572f9cf727b6-0505c6de016f/cdk2_campaign/poses_all_H/CTX-1020667_best_pose_H.sdf")

BEST_SDF.parent.mkdir(parents=True, exist_ok=True)
BEST_H.parent.mkdir(parents=True, exist_ok=True)

with gzip.open(str(GZ_SDF), "rt") as fh:
    sdf_text = fh.read()

suppl = Chem.SDMolSupplier()
suppl.SetData(sdf_text, removeHs=False)
mols = [m for m in suppl if m is not None]
print(f"Total poses: {len(mols)}")

best_mol = mols[0]
print(f"Pose 1 atoms (pre-H): {best_mol.GetNumAtoms()}")

w = Chem.SDWriter(str(BEST_SDF))
w.write(best_mol)
w.close()
print(f"Written: {BEST_SDF}")

mol_h = Chem.AddHs(best_mol, addCoords=True)
n_H   = sum(1 for a in mol_h.GetAtoms() if a.GetAtomicNum() == 1)
print(f"After AddHs: {mol_h.GetNumAtoms()} atoms, {n_H} explicit H")

w = Chem.SDWriter(str(BEST_H))
w.write(mol_h)
w.close()
print(f"Written: {BEST_H}")
