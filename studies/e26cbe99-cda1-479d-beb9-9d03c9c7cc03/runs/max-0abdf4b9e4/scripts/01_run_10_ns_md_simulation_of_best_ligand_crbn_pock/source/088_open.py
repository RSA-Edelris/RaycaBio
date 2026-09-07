
import json, os, subprocess
from rdkit import Chem
from rdkit.Chem import AllChem, rdMolDescriptors

WD = '/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85'
AMBERHOME = '/home/ubuntu/rayca-runtime/.mamba/envs/rayca'

# Load existing scores
with open(f'{WD}/final_results.json') as fh:
    scores = json.load(fh)

compounds = [
    ('EDS01357518_ent1', 'S', '#60a5fa'),
    ('EDS01357518_ent2', 'R', '#93c5fd'),
    ('EDS01806218_ent1', '1R,2R', '#f472b6'),
    ('EDS01806218_ent2', '1S,2S', '#f9a8d4'),
    ('EDS01889984',      '—',    '#86efac'),
]

# Function to extract best pose + get net charge
def prep_ligand(cid, work_dir):
    sdf_path = f'{WD}/poses_{cid}.sdf'
    with open(sdf_path) as fh:
        blocks = [b.strip() for b in fh.read().split('$$$$') if b.strip()]
    mol = Chem.MolFromMolBlock(blocks[0], removeHs=True)
    mol_h = AllChem.AddHs(mol, addCoords=True)
    net_charge = sum(a.GetFormalCharge() for a in mol_h.GetAtoms())
    sdf_out = f'{work_dir}/lig_h.sdf'
    with Chem.SDWriter(sdf_out) as w:
        w.write(mol_h)
    return sdf_out, net_charge

for cid, stereo, _ in compounds:
    sc = scores[cid]
    print(f"{cid} ({stereo}): Vina={sc['vina']:.2f}  ΔG_CNN={sc['dG_cnn']:.2f}")
