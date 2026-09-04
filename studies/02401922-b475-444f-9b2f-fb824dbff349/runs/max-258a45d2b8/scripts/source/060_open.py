
wd = '/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a'

# Map AMBER terminal residue names → standard PDB names
term_map = {
    'NSER': 'SER ', 'NGLY': 'GLY ', 'NALA': 'ALA ', 'NARG': 'ARG ',
    'NLEU': 'LEU ', 'NVAL': 'VAL ', 'NILE': 'ILE ', 'NTHR': 'THR ',
    'NPRO': 'PRO ', 'NASP': 'ASP ', 'NGLU': 'GLU ', 'NLYS': 'LYS ',
    'CSER': 'SER ', 'CGLY': 'GLY ', 'CALA': 'ALA ', 'CARG': 'ARG ',
    'CLEU': 'LEU ', 'CVAL': 'VAL ', 'CILE': 'ILE ', 'CTHR': 'THR ',
    'CPRO': 'PRO ', 'CASP': 'ASP ', 'CGLU': 'GLU ', 'CLYS': 'LYS ',
}

fixed, changed = [], 0
with open(f'{wd}/receptor_noh2.pdb') as f:
    for line in f:
        if line.startswith(('ATOM', 'HETATM')):
            resname = line[17:21]  # 4 chars
            key = resname.strip()
            if key in term_map:
                line = line[:17] + term_map[key] + line[21:]
                changed += 1
        fixed.append(line)

with open(f'{wd}/receptor_clean.pdb', 'w') as f:
    f.writelines(fixed)

print(f"Changed {changed} residue name occurrences")
# Verify no AMBER terminal names remain
remaining = [l[17:21].strip() for l in fixed if l.startswith(('ATOM','HETATM')) and l[17:21].strip() in term_map]
print(f"Remaining AMBER terminal names: {set(remaining)}")
