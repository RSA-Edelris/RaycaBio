
import subprocess

# CTX crystal interactions (redefine helper)
def parse_atoms_pdb(path):
    atoms = []
    with open(path) as f:
        for line in f:
            if not line.startswith(('ATOM','HETATM')): continue
            try:
                name   = line[12:16].strip()
                resname= line[17:20].strip()
                chain  = line[21]
                resnum = line[22:26].strip()
                x,y,z  = float(line[30:38]),float(line[38:46]),float(line[46:54])
                elem   = line[76:78].strip() if len(line)>=78 else name[0]
                atoms.append({'name':name,'resname':resname,'chain':chain,
                              'resnum':resnum,'x':x,'y':y,'z':z,'elem':elem})
            except: pass
    return atoms

ctx_atoms_crys = parse_atoms_pdb('ctx_ref.pdb')
rec_atoms = parse_atoms_pdb('receptor_prepared.pdb')

ctx_hbonds = []
for la in ctx_atoms_crys:
    if la['elem'] == 'H': continue
    for ra in rec_atoms:
        if ra['elem'] == 'H': continue
        d = ((la['x']-ra['x'])**2+(la['y']-ra['y'])**2+(la['z']-ra['z'])**2)**0.5
        if d < 3.5 and la['elem'] in ('N','O') and ra['elem'] in ('N','O'):
            ctx_hbonds.append((la['name'], f"{ra['chain']}:{ra['resname']}{ra['resnum']}", ra['name'], round(d,2)))

print("=== CTX CRYSTAL H-BONDS ===")
seen = set()
for h in sorted(ctx_hbonds, key=lambda x: x[3]):
    key = (h[0],h[1],h[2])
    if key not in seen:
        seen.add(key)
        print(f"  {h[0]:6s} -- {h[1]:15s} {h[2]:6s}  {h[3]:.2f} Å")

# Check MMPBSA tools
for tool in ['MMPBSA.py', 'ante-MMPBSA.py', 'tleap', 'cpptraj']:
    r = subprocess.run(['which', tool], capture_output=True, text=True)
    print(tool, ':', r.stdout.strip() or 'not found')
