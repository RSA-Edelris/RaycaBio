
# Verify atom order mismatch — compare element sequences from both mol2 files
def get_mol2_elements(path):
    elems = []
    in_atoms = False
    with open(path) as f:
        for line in f:
            if '@<TRIPOS>ATOM' in line:
                in_atoms = True; continue
            if '@<TRIPOS>' in line and in_atoms:
                break
            if in_atoms and line.strip():
                parts = line.split()
                if len(parts) >= 6:
                    # atom type is like C.ar, N.3, O.2 → element is before dot
                    elem = parts[5].split('.')[0]
                    elems.append(elem)
    return elems

e_template = get_mol2_elements('ligand.mol2')
e_docked   = get_mol2_elements('ligand_docked.mol2')

print("Template elements:", e_template)
print("Docked elements:  ", e_docked)
print("Match:", e_template == e_docked)
mismatches = [(i,a,b) for i,(a,b) in enumerate(zip(e_template,e_docked)) if a!=b]
print(f"Mismatches: {len(mismatches)}")
if mismatches:
    for i,a,b in mismatches[:10]:
        print(f"  atom {i}: template={a} docked={b}")
