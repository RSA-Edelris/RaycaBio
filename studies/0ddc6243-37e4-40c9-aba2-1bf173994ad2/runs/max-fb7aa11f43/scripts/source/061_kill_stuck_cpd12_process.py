
import subprocess, time, os
from rdkit import Chem
from rdkit.Chem import AllChem

# Kill stuck CPD12 process
subprocess.run(["kill", "636224"], capture_output=True)

# Diagnose: check H count in each failed SDF
print("H-count audit for failed ligands:")
for lig in fail_ligs:
    sdf = LIG_DIR / f"{lig}_top.sdf"
    mol = next(Chem.SDMolSupplier(str(sdf), removeHs=False, sanitize=True), None)
    if mol is None:
        print(f"  {lig}: parse failed")
        continue
    n_total = mol.GetNumAtoms()
    n_H     = sum(1 for a in mol.GetAtoms() if a.GetAtomicNum() == 1)
    n_heavy = n_total - n_H
    # Expected Hs from valence
    mol_noH = Chem.RemoveHs(mol)
    mol_allH = Chem.AddHs(mol_noH)
    n_H_expected = sum(1 for a in mol_allH.GetAtoms() if a.GetAtomicNum() == 1)
    print(f"  {lig:<10}: {n_heavy} heavy + {n_H} explicit H (expected {n_H_expected} H)")

# Write H-complete SDFs for failed ligands and retry antechamber
print("\nWriting H-complete SDFs and retrying antechamber...")
retry_procs = {}
for lig in fail_ligs:
    sdf_in  = LIG_DIR / f"{lig}_top.sdf"
    d       = PARAM_DIR / lig
    sdf_h   = d / f"{lig}_allH.sdf"
    
    mol = next(Chem.SDMolSupplier(str(sdf_in), removeHs=False, sanitize=True), None)
    mol_noH = Chem.RemoveHs(mol)
    mol_allH = Chem.AddHs(mol_noH)
    AllChem.EmbedMolecule(mol_allH, AllChem.ETKDGv3())   # regenerate 3D with H
    
    w = Chem.SDWriter(str(sdf_h))
    w.write(mol_allH)
    w.close()
    
    n_H = sum(1 for a in mol_allH.GetAtoms() if a.GetAtomicNum() == 1)
    n_total = mol_allH.GetNumAtoms()
    print(f"  {lig}: wrote {n_total} atoms ({n_H} H) → {sdf_h.name}")
    
    cmd = [
        "antechamber",
        "-i", str(sdf_h), "-fi", "sdf",
        "-o", str(d / f"{lig}.mol2"), "-fo", "mol2",
        "-c", "bcc", "-s", "2", "-nc", "0",
        "-rn", "LIG", "-at", "gaff2", "-dr", "no",
    ]
    log = open(d / "antechamber_retry.log", "w")
    p = subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT, cwd=str(d))
    retry_procs[lig] = p.pid
    print(f"    started pid {p.pid}")

print(f"\n{len(retry_procs)} retry jobs running")
