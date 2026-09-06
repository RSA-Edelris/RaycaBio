#!/usr/bin/env python3
"""Add explicit H to all best-pose SDF files for acpype/GAFF2 compatibility."""
import sys
from pathlib import Path
from rdkit import Chem
from rdkit.Chem import AllChem, SDWriter

WDIR      = Path(__file__).parent
POSES_ALL = WDIR / "poses_all"
POSES_H   = WDIR / "poses_all_H"
POSES_H.mkdir(exist_ok=True)

failed = []
done   = 0
for sdf in sorted(POSES_ALL.glob("*_best_pose.sdf")):
    name = sdf.stem.replace("_best_pose", "")
    out  = POSES_H / f"{name}_best_pose_H.sdf"
    suppl = Chem.SDMolSupplier(str(sdf), removeHs=False, sanitize=True)
    mol = next((m for m in suppl if m is not None), None)
    if mol is None:
        print(f"  WARN: {name} unreadable", flush=True)
        failed.append(name)
        continue
    mol_h = Chem.AddHs(mol, addCoords=True)
    w = SDWriter(str(out))
    w.write(mol_h)
    w.close()
    done += 1

print(f"Done: {done} H-added SDF files written to poses_all_H/")
print(f"Failed: {failed}")

# Verify test compound
test = POSES_H / "CTX-1020732_best_pose_H.sdf"
if test.exists():
    t = test.read_text()
    ls = t.splitlines()
    natoms = int(ls[3].split()[0])
    nH = sum(1 for l in ls[4:4+natoms] if len(l.split()) >= 4 and l.split()[3] == 'H')
    print(f"CTX-1020732: {natoms} atoms total, {nH} H atoms")
