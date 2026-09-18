
import gemmi, numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem

receptor_path = "/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b/docking/receptor_CRBN_GSPT1.pdb"
pose_dir      = "/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b/docking/poses"

# Load receptor and extract coords for key residues
st = gemmi.read_structure(receptor_path)
model = st[0]

def residue_atoms(chain_name, seqid_str):
    """Return list of (x,y,z) for all non-H atoms in a residue."""
    coords = []
    for ch in model:
        if ch.name != chain_name:
            continue
        for res in ch:
            if str(res.seqid) == seqid_str:
                for atom in res:
                    if atom.element.name != 'H':
                        coords.append(np.array([atom.pos.x, atom.pos.y, atom.pos.z]))
    return coords

# CRBN (chain Z) Trp-cage and glutarimide pocket residues
crbn_pocket = {}
for (ch, sid) in [('Z','353'),('Z','357'),('Z','378'),('Z','380'),
                  ('Z','351'),('Z','391'),('Z','400'),('Z','402')]:
    crbn_pocket[f"{ch}{sid}"] = residue_atoms(ch, sid)

# GSPT1 (chain X) neo-interface residues  
gspt1_neo = {}
for (ch, sid) in [('X','572'),('X','573'),('X','574'),('X','575'),('X','628')]:
    gspt1_neo[f"{ch}{sid}"] = residue_atoms(ch, sid)

crbn_pts  = np.array([a for v in crbn_pocket.values() for a in v])
gspt1_pts = np.array([a for v in gspt1_neo.values() for a in v])

print(f"CRBN pocket atoms: {len(crbn_pts)}")
print(f"GSPT1 neo atoms:   {len(gspt1_pts)}")

# Check residue counts
for k,v in crbn_pocket.items():
    print(f"  CRBN {k}: {len(v)} atoms")
for k,v in gspt1_neo.items():
    print(f"  GSPT1 {k}: {len(v)} atoms")
