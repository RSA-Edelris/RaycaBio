
import os, shutil

# --- Step 1: Strip ALL H atoms from receptor (fixes HIE HD1 fatal tleap error) ---
receptor_in  = "1Z5M_receptor_pH7.4.pdb"
receptor_out = "receptor_pH74_noH.pdb"

heavy_lines = []
with open(receptor_in) as f:
    for line in f:
        if not line.startswith("ATOM"):
            continue
        # Element column (1-indexed cols 77-78, 0-indexed 76:78)
        elem = line[76:78].strip() if len(line) >= 78 else ""
        if elem == "H":
            continue
        atom_name = line[12:16].strip()
        if atom_name.startswith("H"):
            continue
        if len(atom_name) >= 2 and atom_name[0].isdigit() and atom_name[1] == "H":
            continue
        heavy_lines.append(line)

with open(receptor_out, "w") as g:
    g.writelines(heavy_lines)

n_atoms = sum(1 for l in heavy_lines if l.startswith("ATOM"))
print(f"Receptor heavy atoms: {n_atoms}")

# Check HIS residue names (should be HIE/HID/HIP, not HIS)
his_variants = {}
for l in heavy_lines:
    resname = l[17:20].strip()
    if resname in ("HIS","HIE","HID","HIP"):
        resnum = l[22:26].strip()
        key = f"{resname}_{resnum}"
        if key not in his_variants:
            his_variants[key] = resname

print("Histidine residues:", his_variants)

# Confirm no HD1 atoms remain on HIE
hie_hd1 = [l.strip() for l in heavy_lines if "HD1" in l and "HIE" in l]
print(f"HIE HD1 atoms remaining: {len(hie_hd1)} (should be 0)")

# Check ligand file
lig_path = "all_poses/EL2003A_pose2.sdf"
print(f"\nLigand file: {lig_path}, exists={os.path.exists(lig_path)}, "
      f"size={os.path.getsize(lig_path)} bytes")
