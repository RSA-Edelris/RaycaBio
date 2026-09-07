
# Generate protein+ligand complex PDB files for the 5 best poses
# and compile the full results table.

import os, numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem

RT_KCAL = 0.5921;  LN10 = 2.30259

LIGANDS = ['EDS01357518_ent1','EDS01357518_ent2',
           'EDS01806218_ent1','EDS01806218_ent2','EDS01889984']

PARENT = {'EDS01357518_ent1':'EDS01357518 (R)', 'EDS01357518_ent2':'EDS01357518 (S)',
          'EDS01806218_ent1':'EDS01806218 (1R,2R)', 'EDS01806218_ent2':'EDS01806218 (1S,2S)',
          'EDS01889984':'EDS01889984'}

# Load the best pose for each ligand and the receptor header
with open('PB-20260903-4CI2_receptor_trimmed_capped.pdb') as f:
    rec_lines = [ln for ln in f if ln[:6].strip() in ('ATOM','HETATM','TER','REMARK','CRYST1')]

results = {}
complex_files = {}

for lig in LIGANDS:
    supp  = Chem.SDMolSupplier(f'poses_{lig}.sdf', removeHs=False)
    mols  = [m for m in supp if m is not None]
    pose  = mols[0]
    props = pose.GetPropsAsDict()

    vina       = props.get('minimizedAffinity', float('nan'))
    cnn_pose   = props.get('CNNscore',          float('nan'))
    cnn_aff    = props.get('CNNaffinity',        float('nan'))
    dG_cnn     = -RT_KCAL * LN10 * cnn_aff

    results[lig] = dict(vina=vina, cnn_pose=cnn_pose, cnn_aff=cnn_aff, dG_cnn=dG_cnn)

    # Write complex PDB: receptor ATOM lines + ligand HETATM lines from gnina
    conf  = pose.GetConformer()
    cpx_lines = list(rec_lines)
    # Strip terminal END/TER from receptor block
    cpx_lines = [ln for ln in cpx_lines if ln[:3] not in ('END',)]
    cpx_lines.append('TER\n')
    # Write ligand atoms as HETATM
    for i, atom in enumerate(pose.GetAtoms()):
        pos  = conf.GetAtomPosition(atom.GetIdx())
        elem = atom.GetSymbol()
        num  = str(i + 1)
        anm  = (f" {elem}{num:<3s}" if len(elem)==1 else f"{elem}{num:<3s}")[:4]
        cpx_lines.append(
            f"HETATM{i+1:5d} {anm:<4s} LIG Z   1    "
            f"{pos.x:8.3f}{pos.y:8.3f}{pos.z:8.3f}  1.00  0.00          {elem:>2s}\n")
    cpx_lines.append("END\n")

    cpx_path = f'complex_{lig}.pdb'
    with open(cpx_path, 'w') as fh:
        fh.writelines(cpx_lines)
    complex_files[lig] = cpx_path

print("Complex PDB files written:")
for lig, path in complex_files.items():
    sz = os.path.getsize(path)
    print(f"  {path}  ({sz:,} bytes)")

print("\n===== Final results table =====")
print(f"{'Ligand':<25}  {'Vina':>7}  {'CNN_pose':>9}  {'pKi':>6}  {'ΔG_CNN':>9}")
print("-"*65)
for lig in LIGANDS:
    r = results[lig]
    print(f"{lig:<25}  {r['vina']:>7.2f}  {r['cnn_pose']:>9.4f}  "
          f"{r['cnn_aff']:>6.3f}  {r['dG_cnn']:>9.2f}")

print("\nΔG_CNN (kcal/mol) = −RT·ln(10)·pKi = −1.364·pKi  (at 298 K)")
