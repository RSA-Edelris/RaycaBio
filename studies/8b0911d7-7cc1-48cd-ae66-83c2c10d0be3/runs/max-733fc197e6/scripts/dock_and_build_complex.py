#!/usr/bin/env python3
"""
Dock all 4 ligands against PTPN2 using vina Python bindings.
Saves pose PDBQT files, then builds a combined multi-ligand PDB:
  - Protein (ATOM records from 9C56_receptor.pdb)
  - Co-crystal ligand FRJ (HETATM from 9C56.pdb) as reference
  - Best docked pose for each of the 4 compounds (HETATM)
"""
import os, sys, subprocess, json
from pathlib import Path

WORKDIR = Path('/home/ubuntu/rayca-sessions/8b0911d7-7cc1-48cd-ae66-83c2c10d0be3-c43f8bb507fc')
LIG_DIR  = WORKDIR / 'ligands'
FIG_DIR  = WORKDIR / 'figures'
ORIG_PDB = Path('/home/ubuntu/rayca-artifacts/db61873ef1ff7fa5e8bf27d4/files/9C56.pdb')
RECEPTOR_PDB  = WORKDIR / '9C56_receptor.pdb'
RECEPTOR_PDBQT = WORKDIR / '9C56_receptor.pdbqt'

# Docking box (FRJ centroid, confirmed from prior runs)
BOX_CENTER = (28.48, 12.33, 4.22)
BOX_SIZE   = (22.0, 28.0, 24.0)

LIGANDS = [
    {'id': 'EDS00760714-1', 'name': 'Compound32_R', 'chain': 'B', 'resnum': 501},
    {'id': 'EDS00760714-2', 'name': 'Compound32_S', 'chain': 'C', 'resnum': 502},
    {'id': 'EDS00760778-1', 'name': 'Compound16_R', 'chain': 'D', 'resnum': 503},
    {'id': 'EDS00760778-2', 'name': 'Compound16_S', 'chain': 'E', 'resnum': 504},
]

# ── Step 1: Receptor PDB → PDBQT ──
print("Preparing receptor PDBQT...")
if not RECEPTOR_PDBQT.exists():
    r = subprocess.run(
        ['obabel', str(RECEPTOR_PDB), '-O', str(RECEPTOR_PDBQT), '-xr'],
        capture_output=True, text=True
    )
    if r.returncode != 0:
        print(f"  obabel error: {r.stderr[:200]}")
        sys.exit(1)
    print(f"  Written: {RECEPTOR_PDBQT}")
else:
    print(f"  Exists: {RECEPTOR_PDBQT}")

# ── Step 2: Ligand SDF → PDBQT via meeko ──
from rdkit import Chem
from meeko import MoleculePreparation, PDBQTMolecule, PDBQTWriterLegacy

def sdf_to_pdbqt(sdf_path, out_pdbqt):
    mol = next(Chem.SDMolSupplier(str(sdf_path), removeHs=False))
    if mol is None:
        raise ValueError(f"Could not parse {sdf_path}")
    preparator = MoleculePreparation()
    mol_setups = preparator.prepare(mol)
    pdbqt_string, is_ok, error_msg = PDBQTWriterLegacy.write_string(mol_setups[0])
    if not is_ok:
        raise ValueError(f"meeko error: {error_msg}")
    with open(out_pdbqt, 'w') as f:
        f.write(pdbqt_string)
    return out_pdbqt

print("\nPreparing ligand PDBQTs...")
lig_pdbqts = {}
for lig in LIGANDS:
    sdf = LIG_DIR / f"{lig['id']}.sdf"
    pdbqt = LIG_DIR / f"{lig['id']}.pdbqt"
    try:
        sdf_to_pdbqt(sdf, pdbqt)
        lig_pdbqts[lig['id']] = pdbqt
        print(f"  {lig['id']}: OK")
    except Exception as e:
        print(f"  {lig['id']}: FAILED — {e}")

# ── Step 3: Dock each ligand ──
import vina

print("\nDocking...")
all_results = {}
for lig in LIGANDS:
    lid = lig['id']
    if lid not in lig_pdbqts:
        print(f"  {lid}: SKIP (no PDBQT)")
        continue
    poses_pdbqt = LIG_DIR / f"{lid}_poses.pdbqt"

    v = vina.Vina(sf_name='vina', verbosity=0)
    v.set_receptor(str(RECEPTOR_PDBQT))
    v.set_ligand_from_file(str(lig_pdbqts[lid]))
    v.compute_vina_maps(
        center=list(BOX_CENTER),
        box_size=list(BOX_SIZE)
    )
    v.dock(exhaustiveness=16, n_poses=5)
    v.write_poses(str(poses_pdbqt), n_poses=5, overwrite=True)

    energies = v.energies(n_poses=5)
    scores = [float(e[0]) for e in energies]
    all_results[lid] = {'best': scores[0], 'poses': scores}
    print(f"  {lid}: best={scores[0]:.1f} kcal/mol  all={[f'{s:.1f}' for s in scores]}")

    # Save JSON
    rj = LIG_DIR / f"{lid}_results.json"
    with open(rj, 'w') as f:
        json.dump({
            'ligand_id': lid,
            'best_affinity_kcal_mol': scores[0],
            'affinities_kcal_mol': scores,
            'num_poses': len(scores)
        }, f, indent=2)

print(f"\nDocking complete. Results: {all_results}")

# ── Step 4: Parse best pose from each PDBQT ──
def parse_best_pose_pdbqt(pdbqt_path):
    """Return list of (name, x, y, z) for the first MODEL in a multi-model PDBQT."""
    atoms = []
    in_model = False
    with open(pdbqt_path) as f:
        for line in f:
            if line.startswith('MODEL'):
                in_model = True
            elif line.startswith('ENDMDL'):
                break
            elif in_model and (line.startswith('ATOM') or line.startswith('HETATM')):
                aname = line[12:16].strip()
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])
                atoms.append((aname, x, y, z))
    return atoms

# ── Step 5: Extract FRJ from original PDB ──
print("\nExtracting FRJ co-crystal ligand...")
frj_atoms = []
with open(ORIG_PDB) as f:
    for line in f:
        if (line.startswith('HETATM') and 'FRJ' in line
                and line[16] in (' ', 'A')   # alt loc filter (keep A or blank)
                and float(line[54:60]) > 0.5):  # occupancy > 0.5
            aname = line[12:16].strip()
            x = float(line[30:38])
            y = float(line[38:46])
            z = float(line[46:54])
            frj_atoms.append((aname, x, y, z))
print(f"  FRJ atoms: {len(frj_atoms)}")

# ── Step 6: Build combined PDB ──
LABEL_MAP = {
    'EDS00760714-1': ('C32R', 'B', 501),
    'EDS00760714-2': ('C32S', 'C', 502),
    'EDS00760778-1': ('C16R', 'D', 503),
    'EDS00760778-2': ('C16S', 'E', 504),
}

SCORE_MAP = {
    'EDS00760714-1': -7.0,  # fallback if not re-docked
    'EDS00760714-2': -6.7,
    'EDS00760778-1': -7.3,
    'EDS00760778-2': None,
}
for lid, res in all_results.items():
    SCORE_MAP[lid] = res['best']

out_pdb = WORKDIR / 'PTPN2_9C56_docked_poses.pdb'
print(f"\nBuilding combined PDB: {out_pdb}")

with open(out_pdb, 'w') as f:
    f.write("REMARK PTPN2/TCPTP (9C56) — docked poses + FRJ co-crystal reference\n")
    f.write("REMARK Chain A: Protein receptor\n")
    f.write("REMARK Chain F: Co-crystal ligand FRJ (reference, occupancy 0.71)\n")
    f.write("REMARK Chain B: Compound 32 (R) — EDS00760714-1\n")
    f.write("REMARK Chain C: Compound 32 (S) — EDS00760714-2\n")
    f.write("REMARK Chain D: Compound 16 (R) — EDS00760778-1\n")
    f.write("REMARK Chain E: Compound 16 (S) — EDS00760778-2\n")
    for lid, res in sorted(all_results.items()):
        score = res['best']
        f.write(f"REMARK {LABEL_MAP[lid][0]} best Vina dG = {score:.1f} kcal/mol\n")
    f.write("REMARK\n")

    # Protein ATOM records (chain A)
    with open(RECEPTOR_PDB) as rec:
        for line in rec:
            if line.startswith('ATOM'):
                f.write(line)
    f.write("TER\n")

    # FRJ reference (chain F)
    for i, (aname, x, y, z) in enumerate(frj_atoms, 1):
        el = aname[0] if aname[0].isalpha() else aname[1]
        f.write(f"HETATM{i:5d}  {aname:<4s}FRJ F 400    {x:8.3f}{y:8.3f}{z:8.3f}  0.71  0.00          {el:>2s}\n")
    f.write("TER\n")

    # Best docked pose per ligand
    for lid in ['EDS00760714-1', 'EDS00760714-2', 'EDS00760778-1', 'EDS00760778-2']:
        poses_pdbqt = LIG_DIR / f"{lid}_poses.pdbqt"
        if not poses_pdbqt.exists():
            print(f"  {lid}: no poses file, skipping")
            continue
        label, chain, resnum = LABEL_MAP[lid]
        score = SCORE_MAP.get(lid)
        atoms = parse_best_pose_pdbqt(poses_pdbqt)
        if not atoms:
            print(f"  {lid}: empty pose, skipping")
            continue
        score_str = f"{score:.1f}" if score else "?"
        f.write(f"REMARK Ligand {label} dG={score_str} kcal/mol\n")
        for i, (aname, x, y, z) in enumerate(atoms, 1):
            el = aname[0] if aname[0].isalpha() else aname[1]
            f.write(f"HETATM{i:5d}  {aname:<4s}{label:<4s}{chain} {resnum:3d}    {x:8.3f}{y:8.3f}{z:8.3f}  1.00  0.00          {el:>2s}\n")
        f.write("TER\n")
        print(f"  {lid} ({label}): {len(atoms)} atoms written, chain {chain}")

    f.write("END\n")

sz = out_pdb.stat().st_size
print(f"\nOutput: {out_pdb}  ({sz//1024} KB)")
print("DONE")
