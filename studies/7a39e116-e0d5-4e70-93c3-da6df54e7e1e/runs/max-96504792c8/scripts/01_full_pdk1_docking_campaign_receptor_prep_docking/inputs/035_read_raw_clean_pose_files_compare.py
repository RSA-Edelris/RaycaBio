
import re

# Read the raw clean pose files to compare
for i in range(1, 6):
    path = f"{WS}/clean_pose_{i}.sdf"
    with open(path) as f:
        content = f.read()
    mol_block = content.split("$$$$")[0].strip()
    # Count atoms and bonds
    lines = mol_block.split('\n')
    # Find counts line in V2000
    counts_line = None
    for line in lines[:10]:
        if 'V2000' in line or len(line.strip()) > 0:
            parts = line.split()
            if len(parts) >= 2:
                try:
                    na, nb = int(parts[0]), int(parts[1])
                    if 10 < na < 100:
                        counts_line = (na, nb)
                        break
                except:
                    pass
    # Check for 3D (non-zero z coords)
    has_3d = any(
        len(l.split()) >= 4 and l.split()[2] != '0.0000' and l.split()[2] != '0'
        for l in lines
        if len(l.split()) >= 4 and not l.startswith('M')
    )
    print(f"Pose {i}: {len(content)} bytes, counts={counts_line}, has_3d={has_3d}")
    # Show first few atom lines
    atom_lines = [l for l in lines if len(l.split()) >= 4 and not l.startswith('M')][:3]
    print(f"  Sample: {atom_lines[:2]}")
