#!/usr/bin/env python3
"""
Prepare 4 PTPN2 ligands from V3000 SDF:
- Parse V2000 converted SDF
- Extract stereochemistry from 3D coords
- Apply Dimorphite-DL protonation at pH 7.4
- Generate 3D conformers with ETKDG + MMFF
- Write individual SDF files for docking
"""
import re, os, json, sys
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors, rdMolDescriptors

WORKDIR = '/home/ubuntu/rayca-sessions/8b0911d7-7cc1-48cd-ae66-83c2c10d0be3-c43f8bb507fc'
SDF_V2K = os.path.join(WORKDIR, 'ligands_v2000.sdf')
SDF_IN  = "/home/ubuntu/rayca-artifacts/11507a0e2f5e69d5dfa40a62/files/P965_EDELRIS_2 Hits w enantiomers.sdf"
LIG_DIR = os.path.join(WORKDIR, 'ligands')
os.makedirs(LIG_DIR, exist_ok=True)

# Parse properties from original V3000
with open(SDF_IN) as f:
    raw = f.read()
blocks = raw.split('$$$$')
props_list = []
for blk in blocks:
    if not blk.strip():
        continue
    p = {}
    for m in re.finditer(r'>  <([^>]+)>\s*\n([^\n]+)', blk):
        p[m.group(1).strip()] = m.group(2).strip()
    if p:
        props_list.append(p)

# Load 3D mols from V2000
suppl = Chem.SDMolSupplier(SDF_V2K, removeHs=True, sanitize=True)
mols_raw = [m for m in suppl if m is not None]

print(f"Mols: {len(mols_raw)}  Props: {len(props_list)}")

# Pair names for enantiomers
# -1 and -2 share same root ID (EDS00760714, EDS00760778)
all_meta = []

for i, (mol, props) in enumerate(zip(mols_raw, props_list)):
    mol_id   = props.get('ID', f'lig{i}')
    mol_name = props.get('Molecule Name', f'Compound_{i}')
    kd       = props.get('Kd', '?')
    cls_val  = props.get('Class', '?')

    # Canonical isomeric SMILES (preserves stereo from 3D)
    smi = Chem.MolToSmiles(mol, isomericSmiles=True)
    mw  = round(Descriptors.MolWt(mol), 1)
    logp = round(Descriptors.MolLogP(mol), 2)
    hba = rdMolDescriptors.CalcNumHBA(mol)
    hbd = rdMolDescriptors.CalcNumHBD(mol)
    rot = rdMolDescriptors.CalcNumRotatableBonds(mol)
    tpsa = round(rdMolDescriptors.CalcTPSA(mol), 1)
    stereo = Chem.FindMolChiralCenters(mol, includeUnassigned=True)

    # Determine enantiomer label
    root_id = mol_id.rsplit('-', 1)[0]
    suffix  = mol_id.rsplit('-', 1)[1] if '-' in mol_id else '1'
    enant_label = 'ent1' if suffix == '1' else 'ent2'

    # --- Protonation via Dimorphite-DL ---
    try:
        from dimorphite_dl import DimorphiteDL
        dl = DimorphiteDL(min_ph=7.2, max_ph=7.6, pka_precision=1.0, quiet=True)
        protonated_smiles = dl.protonate(smi)
        if protonated_smiles:
            smi_ph74 = protonated_smiles[0]
        else:
            smi_ph74 = smi
    except Exception as e:
        print(f"  Dimorphite-DL failed: {e}; using original SMILES")
        smi_ph74 = smi

    print(f"\n{mol_id} ({mol_name})")
    print(f"  SMILES_orig: {smi}")
    print(f"  SMILES_pH74: {smi_ph74}")
    print(f"  MW={mw}  cLogP={logp}  HBA={hba}  HBD={hbd}  Rot={rot}  TPSA={tpsa}")
    print(f"  Kd={kd}  Stereocenters={stereo}")

    # --- Build 3D conformer from pH 7.4 SMILES ---
    mol_ph = Chem.MolFromSmiles(smi_ph74)
    if mol_ph is None:
        print(f"  WARNING: pH SMILES failed, using original")
        mol_ph = Chem.MolFromSmiles(smi)
    if mol_ph is None:
        print(f"  ERROR: molecule {mol_id} failed entirely, skipping")
        continue

    mol_ph_h = Chem.AddHs(mol_ph)

    # Try to use original 3D coords as template for embedding
    ps = AllChem.ETKDGv3()
    ps.randomSeed = 42
    ps.useSmallRingTorsions = True
    ps.useMacrocycleTorsions = True
    ret = AllChem.EmbedMolecule(mol_ph_h, ps)
    if ret == -1:
        # fallback: random coords
        AllChem.EmbedMolecule(mol_ph_h, AllChem.ETKDG())
    AllChem.MMFFOptimizeMolecule(mol_ph_h, maxIters=2000)

    # Write SDF
    sdf_path = os.path.join(LIG_DIR, f'{mol_id}.sdf')
    writer = Chem.SDWriter(sdf_path)
    mol_ph_h.SetProp('_Name', mol_id)
    mol_ph_h.SetProp('Molecule_Name', mol_name)
    mol_ph_h.SetProp('Kd', kd)
    mol_ph_h.SetProp('SMILES_pH74', smi_ph74)
    writer.write(mol_ph_h)
    writer.close()
    print(f"  Written: {sdf_path}")

    all_meta.append({
        'id': mol_id, 'name': mol_name, 'root_id': root_id,
        'enant_label': enant_label, 'kd': kd, 'cls': cls_val,
        'smiles_3d': smi, 'smiles_ph74': smi_ph74,
        'mw': mw, 'logp': logp, 'hba': hba, 'hbd': hbd,
        'rot': rot, 'tpsa': tpsa,
        'stereocenters': [(a, c) for a, c in stereo],
        'sdf_file': sdf_path
    })

# Save metadata
meta_path = os.path.join(WORKDIR, 'ligand_meta.json')
with open(meta_path, 'w') as f:
    json.dump(all_meta, f, indent=2)
print(f"\nMetadata written: {meta_path}")
print("DONE")
