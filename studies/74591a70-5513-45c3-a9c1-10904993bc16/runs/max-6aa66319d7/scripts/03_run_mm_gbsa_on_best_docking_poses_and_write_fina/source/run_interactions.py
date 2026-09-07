#!/usr/bin/env python3
"""ProLIF interaction fingerprinting for all 22 docked CRBN poses."""

import json, warnings
from pathlib import Path
import numpy as np

warnings.filterwarnings('ignore')

import MDAnalysis as mda
import prolif as plf
from rdkit import Chem

BASE      = Path("/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e")
BEST_DIR  = BASE / "best_poses2_top1"
REC_PDB   = BASE / "4CI2_receptor_for_docking.pdb"
OUT_FILE  = BASE / "interaction_fingerprints.json"

names = sorted([f.stem.replace('_pose1', '') for f in BEST_DIR.glob('*_pose1.sdf')])
print(f"Analysing {len(names)} compounds against CRBN/4CI2")

# Load receptor once as MDAnalysis Universe
rec_u = mda.Universe(str(REC_PDB))
protein_sel = rec_u.select_atoms("protein")
print(f"Receptor: {len(protein_sel.atoms)} protein atoms, {len(rec_u.residues)} residues")

all_fp = {}

for name in names:
    sdf = BEST_DIR / f"{name}_pose1.sdf"
    try:
        # Load ligand SDF as prolif Molecule
        lig_mol = Chem.SDMolSupplier(str(sdf), removeHs=False, sanitize=True)[0]
        if lig_mol is None:
            print(f"  {name}: failed to load SDF")
            continue

        # Create prolif fingerprint
        lig_plf  = plf.Molecule(lig_mol)
        prot_plf = plf.Molecule.from_mda(protein_sel)

        fp = plf.Fingerprint(
            interactions=[
                "HBDonor", "HBAcceptor",
                "Hydrophobic", "PiStacking",
                "PiCation", "CationPi",
                "Anionic", "Cationic",
                "MetalAcceptor",
            ]
        )
        fp.run_from_iterable([lig_plf], prot_plf)

        df = fp.to_dataframe(return_atoms=True)
        if df is None or len(df) == 0:
            print(f"  {name}: no interactions found")
            all_fp[name] = []
            continue

        interactions = []
        for col in df.columns:
            val = df.iloc[0][col]
            if val and val != (False,):
                # col is a tuple: (ligand_res, protein_res, interaction_type)
                lig_res, prot_res, itype = col
                # atom indices
                if isinstance(val, tuple) and len(val) >= 2:
                    lig_atom_idx  = val[0] if isinstance(val[0], (int, np.integer)) else val[0][0] if val[0] else None
                    prot_atom_idx = val[1] if isinstance(val[1], (int, np.integer)) else val[1][0] if val[1] else None
                else:
                    lig_atom_idx = prot_atom_idx = None

                # Get residue info from protein selection
                prot_res_str = str(prot_res)

                interactions.append({
                    'protein_residue': prot_res_str,
                    'interaction': itype,
                    'ligand_atom': int(lig_atom_idx) if lig_atom_idx is not None else None,
                    'protein_atom': int(prot_atom_idx) if prot_atom_idx is not None else None,
                })

        all_fp[name] = interactions
        n_inter = len(interactions)
        types_seen = sorted(set(i['interaction'] for i in interactions))
        print(f"  {name}: {n_inter} interactions — {', '.join(types_seen)}")

    except Exception as e:
        print(f"  {name}: ERROR — {e}")
        all_fp[name] = []

# --- Aggregate statistics ---
print("\n=== INTERACTION FREQUENCY STATISTICS ===")
from collections import Counter

# Count per residue × interaction type across all compounds
residue_type_counts = Counter()
interaction_type_counts = Counter()
residue_counts = Counter()

n_compounds = len([v for v in all_fp.values() if isinstance(v, list) and len(v) > 0])

for name, interactions in all_fp.items():
    if not isinstance(interactions, list):
        continue
    seen_this_compound = set()
    for inter in interactions:
        key = (inter['protein_residue'], inter['interaction'])
        if key not in seen_this_compound:
            seen_this_compound.add(key)
            residue_type_counts[key] += 1
            residue_counts[inter['protein_residue']] += 1
            interaction_type_counts[inter['interaction']] += 1

print(f"\nTop 20 protein residue × interaction type (out of {len(names)} compounds):")
print(f"{'Residue':<20} {'Interaction':<18} {'Count':>6} {'Freq%':>7}")
print("─" * 55)
for (res, itype), count in residue_type_counts.most_common(20):
    freq = 100.0 * count / len(names)
    print(f"{res:<20} {itype:<18} {count:>6} {freq:>6.0f}%")

print(f"\nInteraction type totals:")
for itype, count in interaction_type_counts.most_common():
    print(f"  {itype:<18}: {count}")

# Save results
out = {
    'fingerprints': all_fp,
    'residue_type_freq': {f"{k[0]}|{k[1]}": v for k, v in residue_type_counts.most_common()},
    'interaction_type_counts': dict(interaction_type_counts),
    'residue_counts': dict(residue_counts.most_common(20)),
    'n_compounds': len(names),
}
OUT_FILE.write_text(json.dumps(out, indent=2))
print(f"\nSaved to {OUT_FILE.name}")
