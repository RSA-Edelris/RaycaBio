#!/usr/bin/env python3
"""
ProLIF interaction fingerprinting on best docking poses.
Run after docking_results.json is available.
"""
import json, os, sys
from pathlib import Path
from rdkit import Chem
import MDAnalysis as mda
import prolif as plf
import numpy as np

WDIR    = Path("/home/ubuntu/rayca-sessions/31fad337-0958-45c1-a0cd-572f9cf727b6-0505c6de016f/cdk2_campaign")
REC_PDB = WDIR / "receptor_prepared.pdb"  # needs explicit H for HBDonor/HBAcceptor

results = json.loads((WDIR / "docking_results.json").read_text())
print(f"Processing {len(results)} docked ligands")

# Load receptor once
u_prot = mda.Universe(str(REC_PDB))
prot_sel = u_prot.select_atoms("protein")
prot_mol = plf.Molecule.from_mda(prot_sel)

ifp_records = []

for rec in results:
    name = rec["name"]
    pose_file = rec.get("output_file", "")
    if not pose_file or not os.path.exists(pose_file):
        print(f"  SKIP {name}: no pose file")
        continue
    try:
        suppl = Chem.SDMolSupplier(pose_file, sanitize=True, removeHs=False)
        best_pose = next((m for m in suppl if m is not None), None)
        if best_pose is None:
            print(f"  SKIP {name}: unreadable SDF")
            continue
        lig_mol = plf.Molecule.from_rdkit(best_pose)
        fp = plf.Fingerprint(
            interactions=["Hydrophobic","HBDonor","HBAcceptor",
                          "PiStacking","CationPi","Anionic","Cationic",
                          "VdWContact","EdgeToFace","FaceToFace"]
        )
        fp.run_from_iterable([lig_mol], prot_mol)
        df = fp.to_dataframe()
        if df.empty:
            ifp_records.append({"name": name, "interactions": {}})
            continue
        row = df.iloc[0]
        ixns = {}
        for col in df.columns:
            if row[col]:
                # ProLIF 2.x columns: (ligand_name, residue_name, interaction_type)
                if isinstance(col, tuple) and len(col) >= 3:
                    res_name = col[1]
                    ix_type  = col[2]
                elif isinstance(col, tuple) and len(col) == 2:
                    res_name = col[0]
                    ix_type  = col[1]
                else:
                    res_name = str(col)
                    ix_type  = "contact"
                key = f"{res_name}:{ix_type}"
                ixns[key] = True
        ifp_records.append({"name": name, "interactions": ixns})
    except Exception as e:
        print(f"  ERROR {name}: {e}")
        ifp_records.append({"name": name, "interactions": {}, "error": str(e)})

(WDIR / "interaction_fingerprints.json").write_text(json.dumps(ifp_records, indent=2))
print(f"Saved interaction_fingerprints.json  ({len(ifp_records)} entries)")

# ── Statistics table ─────────────────────────────────────────────────────────
from collections import Counter
all_ixns = Counter()
# Only count records that completed without error in the denominator
valid_records = [r for r in ifp_records if "error" not in r]
n_failed = len(ifp_records) - len(valid_records)
if n_failed:
    print(f"  NOTE: {n_failed} records excluded from stats due to ProLIF errors")
for r in valid_records:
    for k in r["interactions"]:
        all_ixns[k] += 1

print("\n=== TOP 30 INTERACTIONS ACROSS SERIES ===")
print(f"{'Residue:Type':<35} {'Count':>6} {'%':>6}")
print("-"*50)
n = len(valid_records)
for ixn, cnt in all_ixns.most_common(30):
    print(f"{ixn:<35} {cnt:>6} {100*cnt/n:>5.1f}%")

(WDIR / "interaction_stats.json").write_text(
    json.dumps({
        "n_analysed": n,
        "n_failed": n_failed,
        "interactions": [{"interaction": k, "count": v, "pct": round(100*v/n, 1)}
                         for k, v in all_ixns.most_common()]
    }, indent=2))
print("\nSaved interaction_stats.json")
