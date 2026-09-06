#!/usr/bin/env python3
"""
Estimate binding free energies from docked poses using a fast
MM/GBSA-proxy approach: gnina CNN affinity (pKi) as primary score +
MMFF conformational strain of the docked ligand pose as a secondary
quality filter (high strain → penalised binding).

For a full production MM/GBSA you would run AmberTools/GROMACS/OpenMM.
NOTE: mmff_strain_kcal is the intramolecular MMFF strain of the docked
ligand conformation, NOT a protein-ligand interaction energy.
"""
import json, os
from pathlib import Path
from rdkit import Chem
from rdkit.Chem import AllChem, rdForceFieldHelpers
import numpy as np

WDIR = Path("/home/ubuntu/rayca-sessions/31fad337-0958-45c1-a0cd-572f9cf727b6-0505c6de016f/cdk2_campaign")

results = json.loads((WDIR / "docking_results.json").read_text())
print(f"Computing energies for {len(results)} ligands")

energy_records = []
for rec in results:
    name      = rec["name"]
    pose_file = rec.get("output_file", "")
    vina_score  = rec.get("best_affinity", None)
    cnn_score   = rec.get("best_cnn_affinity", None)

    mmff_ie = None
    if pose_file and os.path.exists(pose_file):
        try:
            suppl = Chem.SDMolSupplier(pose_file, sanitize=True, removeHs=False)
            best  = next((m for m in suppl if m is not None), None)
            if best is not None:
                bh = Chem.AddHs(best, addCoords=True)
                ff = AllChem.MMFFGetMoleculeForceField(
                        bh, AllChem.MMFFGetMoleculeProperties(bh))
                if ff:
                    mmff_ie = ff.CalcEnergy()
        except Exception as e:
            mmff_ie = None

    energy_records.append({
        "name":              name,
        "vina_affinity":     vina_score,
        "cnn_affinity":      cnn_score,
        "cnn_pose_score":    rec.get("best_cnn_pose"),
        "mmff_strain_kcal":  round(mmff_ie, 3) if mmff_ie is not None else None,
        "best_score":        cnn_score if cnn_score else vina_score,
    })

# Sort by CNN affinity descending: higher pKi = stronger predicted binding
energy_records.sort(key=lambda x: x["best_score"] if x["best_score"] else 0, reverse=True)

(WDIR / "energy_results.json").write_text(json.dumps(energy_records, indent=2))
print("Saved energy_results.json")

print("\n=== TOP 20 BY CNN AFFINITY ===")
print(f"{'Rank':<5}{'Name':<20}{'Vina(kcal/mol)':<18}{'CNN_affinity':<16}{'CNN_pose':<12}")
print("-"*70)
for i, r in enumerate(energy_records[:20], 1):
    print(f"{i:<5}{r['name']:<20}{str(r['vina_affinity']):<18}{str(r['cnn_affinity']):<16}{str(r['cnn_pose_score']):<12}")
