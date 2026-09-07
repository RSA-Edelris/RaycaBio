
# ── BUILD DOCKING RECEPTOR + SELECT SITE WATERS ───────────────────────────────
from openmm.app import PDBFile as PDBFileOM
import openmm.unit as unit
import numpy as np, os

positions = fixer2.positions
topology  = fixer2.topology

# centroid in nm (OpenMM units)
centroid_nm = centroid / 10.0   # Å → nm

# Water selection radius: 5 Å = 0.5 nm
WATER_RADIUS_NM = 0.5

protein_atoms, water_atoms, lvy_atoms, zn_atoms = [], [], [], []
water_res, kept_water_res = set(), set()

for atom in topology.atoms():
    res = atom.residue
    pos = positions[atom.index].value_in_unit(unit.nanometers)
    rname = res.name.upper()
    if rname == "LVY":
        lvy_atoms.append(atom.index)
    elif rname in ("HOH", "WAT"):
        water_res.add(res.index)
        d = np.linalg.norm(np.array(pos) - centroid_nm)
        if d <= WATER_RADIUS_NM:
            kept_water_res.add(res.index)
            water_atoms.append(atom.index)
    elif rname == "ZN":
        zn_atoms.append(atom.index)
    else:
        protein_atoms.append(atom.index)

print(f"Protein atoms : {len(protein_atoms)}")
print(f"ZN atoms      : {len(zn_atoms)}")
print(f"Total waters  : {len(water_res)} residues")
print(f"Site waters (≤5 Å from LVY centroid): {len(kept_water_res)} residues")
print(f"LVY atoms (excluded from receptor)   : {len(lvy_atoms)}")

# keep_atoms = protein + ZN + site waters
keep_set = set(protein_atoms + zn_atoms + water_atoms)

# Write docking receptor PDB via raw lines from full file, filtering by residue
from openmm.app import Modeller
rec_path   = f"{WORK}/4CI2_receptor_for_docking.pdb"
lvy_ref_path = f"{WORK}/4CI2_LVY_ref.pdb"

# Write receptor
with open(full_path) as fin, open(rec_path, 'w') as fout:
    for line in fin:
        rec = line[:6].strip()
        if rec in ("ATOM","HETATM"):
            rname = line[17:20].strip().upper()
            if rname == "LVY":
                continue   # remove LVY from receptor
            # filter HOH not in kept_water_res: use residue seq number
            if rname in ("HOH","WAT"):
                resseq = int(line[22:26].strip())
                # check if this residue is in kept set by matching
                # (position check already done via kept_water_res set)
                # Since we don't have a direct line→res.index map, use distance
                x, y, z = float(line[30:38]), float(line[38:46]), float(line[46:54])
                d = np.linalg.norm(np.array([x, y, z]) - centroid) 
                if d > 5.0:   # 5 Å cutoff in Å
                    continue
            fout.write(line)
        elif rec in ("TER","END","REMARK","CRYST1","HEADER"):
            fout.write(line)

# Write LVY reference  
with open(full_path) as fin, open(lvy_ref_path, 'w') as fout:
    for line in fin:
        if line[:6].strip() == "HETATM" and line[17:20].strip() == "LVY":
            fout.write(line)

print(f"\nDocking receptor → {rec_path}  ({os.path.getsize(rec_path):,} bytes)")
print(f"LVY reference   → {lvy_ref_path}  ({os.path.getsize(lvy_ref_path):,} bytes)")
print(f"\nBox centre: X={centroid[0]:.3f} Y={centroid[1]:.3f} Z={centroid[2]:.3f}")
print(f"Box size: 24 × 24 × 24 Å  (CRBN ThBD pocket ~18 Å wide; 24 gives ample sampling)")
