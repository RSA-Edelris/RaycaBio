
import os, subprocess, json
from rdkit import Chem
from rdkit.Chem import AllChem

WD = '/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85'
AMBERHOME = '/home/ubuntu/rayca-runtime/.mamba/envs/rayca'
REC_PDB = f'{WD}/md_EDS01806218_ent2/receptor_tleap.pdb'
env = {**os.environ, 'AMBERHOME': AMBERHOME}

compounds = ['EDS01357518_ent1','EDS01357518_ent2',
             'EDS01806218_ent1','EDS01806218_ent2','EDS01889984']

mmgbsa_results = {}

for cid in compounds:
    d = f'{WD}/mmgbsa_{cid}'
    os.makedirs(d, exist_ok=True)

    # Extract best pose + add H
    with open(f'{WD}/poses_{cid}.sdf') as fh:
        blocks = [b.strip() for b in fh.read().split('$$$$') if b.strip()]
    mol = AllChem.AddHs(Chem.MolFromMolBlock(blocks[0], removeHs=True), addCoords=True)
    nc = sum(a.GetFormalCharge() for a in mol.GetAtoms())
    with Chem.SDWriter(f'{d}/lig_h.sdf') as w:
        w.write(mol)

    # antechamber (GAFF2 + AM1-BCC)
    r = subprocess.run([
        'antechamber', '-i', f'{d}/lig_h.sdf', '-fi', 'sdf',
        '-o', f'{d}/lig.mol2', '-fo', 'mol2',
        '-c', 'bcc', '-nc', str(nc), '-rn', 'LIG', '-at', 'gaff2', '-pf', 'y'],
        capture_output=True, text=True, cwd=d)
    # parmchk2
    r2 = subprocess.run([
        'parmchk2', '-i', f'{d}/lig.mol2', '-f', 'mol2',
        '-o', f'{d}/lig.frcmod', '-s', 'gaff2'],
        capture_output=True, text=True, cwd=d)

    # tleap — gas phase complex (no solvent)
    tleap_in = f"""\
source leaprc.protein.ff14SB
source leaprc.gaff2
LIG = loadmol2 {d}/lig.mol2
loadamberparams {d}/lig.frcmod
REC = loadpdb {REC_PDB}
complex = combine {{ REC LIG }}
saveamberparm complex {d}/complex.prmtop {d}/complex.inpcrd
quit
"""
    with open(f'{d}/tleap.in', 'w') as fh:
        fh.write(tleap_in)
    r3 = subprocess.run(['tleap', '-f', f'{d}/tleap.in'],
                        capture_output=True, text=True, cwd=d)

    ok = os.path.exists(f'{d}/complex.prmtop')
    print(f"{cid}: antechamber={'OK' if os.path.exists(f'{d}/lig.mol2') else 'FAIL'}  "
          f"parmchk2={'OK' if os.path.exists(f'{d}/lig.frcmod') else 'FAIL'}  "
          f"tleap={'OK' if ok else 'FAIL'}")
