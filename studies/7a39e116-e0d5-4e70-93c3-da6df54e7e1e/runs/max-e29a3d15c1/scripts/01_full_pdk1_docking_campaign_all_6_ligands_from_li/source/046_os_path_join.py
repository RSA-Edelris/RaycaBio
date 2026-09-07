
import os, glob

ws = '/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777'

# Check existing receptor
rec = os.path.join(ws, '1Z5M_receptor_pH7.4.pdb')
lig_sdf = os.path.join(ws, 'ligand_clean_PDK1.sdf')
print(f"Receptor exists: {os.path.exists(rec)} ({os.path.getsize(rec)//1024} kB)")
print(f"Ligands SDF:     {os.path.exists(lig_sdf)} ({os.path.getsize(lig_sdf)} bytes)")

# Recover box center from prior dispatch scripts — look for centerX/Y/Z or boxX
src_dir = os.path.join(ws)
scripts = sorted(glob.glob(os.path.join(src_dir, '0[01][0-9]_*.py')))
box_params = {}
for s in scripts:
    txt = open(s).read()
    if 'centerX' in txt or 'boxX' in txt or 'center_x' in txt:
        print(f"\nBox params found in: {os.path.basename(s)}")
        for line in txt.splitlines():
            if any(k in line for k in ('centerX','centerY','centerZ','sizeX','sizeY','sizeZ',
                                        'boxX','boxY','boxZ','center_x','center_y','center_z',
                                        'size_x','size_y','size_z')):
                print(f"  {line.strip()}")
