#!/usr/bin/env python3
"""ProLIF interaction fingerprinting for 22 CRBN docked poses.
   Selects binding-site residues within 8 Å of each ligand to avoid
   converting the whole 6 k-atom receptor to RDKit.
"""

import json, warnings, sys
from pathlib import Path
from collections import Counter

warnings.filterwarnings('ignore')

import numpy as np
import MDAnalysis as mda
import prolif as plf
from rdkit import Chem

BASE      = Path("/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e")
BEST_DIR  = BASE / "best_poses2_top1"
REC_PDB   = BASE / "4CI2_receptor_for_docking.pdb"
OUT_FILE  = BASE / "interaction_fingerprints.json"

names = sorted([f.stem.replace('_pose1', '') for f in BEST_DIR.glob('*_pose1.sdf')])
print(f"ProLIF: analysing {len(names)} poses", flush=True)

# Load receptor universe once
rec_u = mda.Universe(str(REC_PDB))
print(f"Receptor: {len(rec_u.atoms)} atoms", flush=True)

all_fp   = {}
res_type = Counter()
int_type = Counter()
res_cnt  = Counter()

for name in names:
    sdf = BEST_DIR / f"{name}_pose1.sdf"
    try:
        rdmol = Chem.SDMolSupplier(str(sdf), removeHs=False, sanitize=True)[0]
        if rdmol is None:
            print(f"  {name}: RDKit load failed", flush=True)
            all_fp[name] = []
            continue

        # Get ligand centroid for binding-site selection
        conf  = rdmol.GetConformer()
        pos   = conf.GetPositions()
        cx, cy, cz = pos.mean(axis=0)

        # Select protein residues within 8 Å of ligand centroid
        bs_sel = rec_u.select_atoms(
            f"protein and (resid 1-9999) and point {cx:.2f} {cy:.2f} {cz:.2f} 8.0"
        )
        if len(bs_sel) == 0:
            # Fallback: 12 Å
            bs_sel = rec_u.select_atoms(
                f"protein and point {cx:.2f} {cy:.2f} {cz:.2f} 12.0"
            )
        if len(bs_sel) == 0:
            print(f"  {name}: no pocket residues found", flush=True)
            all_fp[name] = []
            continue

        prot_plf = plf.Molecule.from_mda(bs_sel)
        lig_plf  = plf.Molecule(rdmol)

        fp = plf.Fingerprint(
            interactions=["HBDonor","HBAcceptor","Hydrophobic",
                          "PiStacking","PiCation","CationPi"]
        )
        fp.run_from_iterable([lig_plf], prot_plf)

        df  = fp.to_dataframe(return_atoms=True)
        ints = []
        if df is not None and len(df) > 0:
            for col in df.columns:
                val = df.iloc[0][col]
                if val and val is not False and val != (False,):
                    try:
                        lig_res, prot_res, itype = col
                        ints.append({
                            'protein_residue': str(prot_res),
                            'interaction': str(itype),
                        })
                    except Exception:
                        pass

        all_fp[name] = ints
        types_seen = sorted(set(i['interaction'] for i in ints))
        print(f"  {name}: {len(ints)} interactions [{', '.join(types_seen)}]", flush=True)

        seen = set()
        for inter in ints:
            key = (inter['protein_residue'], inter['interaction'])
            if key not in seen:
                seen.add(key)
                res_type[key] += 1
                res_cnt[inter['protein_residue']] += 1
                int_type[inter['interaction']] += 1

    except Exception as e:
        print(f"  {name}: ERROR {e}", flush=True)
        all_fp[name] = []

n = len(names)
print(f"\n=== TOP RESIDUE × INTERACTION (n={n}) ===", flush=True)
print(f"{'Residue':<22} {'Interaction':<18} {'#':>4} {'Freq':>6}")
print("─" * 54)
for (res, itype), cnt in res_type.most_common(25):
    print(f"{res:<22} {itype:<18} {cnt:>4} {100*cnt/n:>5.0f}%")

print(f"\nInteraction totals:")
for itype, cnt in int_type.most_common():
    print(f"  {itype:<18} {cnt}")

out = {
    'fingerprints': all_fp,
    'residue_type_freq': {f"{k[0]}|{k[1]}": v for k, v in res_type.most_common()},
    'interaction_type_counts': dict(int_type),
    'residue_counts': dict(res_cnt.most_common(20)),
    'n_compounds': n,
}
OUT_FILE.write_text(json.dumps(out, indent=2))
print(f"\nSaved → {OUT_FILE}", flush=True)
