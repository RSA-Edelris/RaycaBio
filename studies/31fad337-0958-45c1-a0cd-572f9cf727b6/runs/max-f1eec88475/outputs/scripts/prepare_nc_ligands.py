#!/usr/bin/env python3
"""Prepare 3D SDF files for NC-001 to NC-010 from SMILES."""
import sys
from pathlib import Path
from rdkit import Chem
from rdkit.Chem import AllChem, SDWriter

WDIR    = Path(__file__).parent
OUT_DIR = WDIR / "ligands_prepared"
OUT_DIR.mkdir(exist_ok=True)

COMPOUNDS = {
    "NC-001": "Cc1c(C(=O)N2CCc3c(nc(C(=O)NCc4ccc(N5CCN(C)CC5)cc4)n3C)C2)oc2ccc(F)cc12",
    "NC-002": "Cc1c(C(=O)N2CCc3c(nc(C(=O)NCc4ccc(N5CCN(C)CC5)cc4)n3C)C2)oc2cc(Cl)ccc12",
    "NC-003": "Cc1c(C(=O)N2CCc3c(nc(C(=O)NCc4ccc(N5CCOCC5)cc4)n3C)C2)oc2ccccc12",
    "NC-004": "Cc1c(C(=O)N2CCc3c(nc(C(=O)N[C@@H](C)c4ccc(N5CCN(C)CC5)cc4)n3C)C2)oc2ccccc12",
    "NC-005": "Cc1c(C(=O)N2CCc3c(nc(C(=O)NCc4ccc(N5CCN(C)CC5)cc4)[nH]3)C2)oc2ccccc12",
    "NC-006": "Cc1c(C(=O)N2CCc3sc(C(=O)NCc4ccc(N5CCN(C)CC5)cc4)nc3C2)oc2ccc(F)cc12",
    "NC-007": "Cc1c(C(=O)N2CCc3c(nc(C(=O)NCc4ccc(N5CC6(COC6)C5)cc4)n3C)C2)oc2ccccc12",
    "NC-008": "Cc1c(C(=O)N2CCc3c(nc(C(=O)NCc4ncc(N5CCN(C)CC5)cc4)n3C)C2)oc2ccccc12",
    "NC-009": "Cc1c(C(=O)N2CCc3c(nc(C(=O)NCc4c(OC)ccc(N5CCN(C)CC5)c4)n3C)C2)oc2ccccc12",
    "NC-010": "Cc1c(C(=O)N2CCc3c(nc(C(=O)NCc4ccc(N5CCN(C)CC5)cc4)n3C)C2)sc2ccccc12",
}

results = {}
for name, smi in COMPOUNDS.items():
    out_path = OUT_DIR / f"{name}.sdf"
    mol = Chem.MolFromSmiles(smi)
    if mol is None:
        print(f"FAIL parse: {name}", flush=True)
        results[name] = "parse_error"
        continue
    mol_h = Chem.AddHs(mol)
    params = AllChem.ETKDGv3()
    params.randomSeed = 42
    ret = AllChem.EmbedMolecule(mol_h, params)
    if ret != 0:
        ret = AllChem.EmbedMolecule(mol_h, AllChem.ETKDG())
    if ret != 0:
        print(f"FAIL embed: {name}", flush=True)
        results[name] = "embed_error"
        continue
    AllChem.MMFFOptimizeMolecule(mol_h, maxIters=2000)
    mol_noH = Chem.RemoveHs(mol_h)
    mol_noH.SetProp("_Name", name)
    mol_noH.SetProp("SMILES", smi)
    w = SDWriter(str(out_path))
    w.write(mol_noH)
    w.close()
    natoms = mol_noH.GetNumAtoms()
    print(f"OK  {name}: {natoms} heavy atoms -> {out_path.name}", flush=True)
    results[name] = natoms

ok  = sum(1 for v in results.values() if isinstance(v, int))
bad = [k for k, v in results.items() if not isinstance(v, int)]
print(f"\nDone: {ok}/{len(COMPOUNDS)} written to {OUT_DIR}")
if bad:
    print(f"Failed: {bad}")
    sys.exit(1)
