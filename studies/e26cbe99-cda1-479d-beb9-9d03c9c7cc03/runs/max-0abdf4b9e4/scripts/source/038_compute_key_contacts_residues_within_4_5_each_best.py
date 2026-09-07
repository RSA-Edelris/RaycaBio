
# Compute key contacts (residues within 4.5 Å) for each best pose
import numpy as np

def parse_pdb_atoms(path):
    atoms = []
    with open(path) as f:
        for line in f:
            rec = line[:6].strip()
            if rec not in ('ATOM','HETATM') or len(line) < 54:
                continue
            try:
                x, y, z = float(line[30:38]), float(line[38:46]), float(line[46:54])
                chain   = line[21].strip()
                resname = line[17:20].strip()
                resnum  = line[22:26].strip()
                aname   = line[12:16].strip()
                atoms.append(dict(rec=rec, chain=chain, resname=resname,
                                  resnum=resnum, aname=aname,
                                  x=x, y=y, z=z))
            except ValueError:
                continue
    return atoms

LIGANDS = ['EDS01357518_ent1','EDS01357518_ent2',
           'EDS01806218_ent1','EDS01806218_ent2','EDS01889984']

CONTACTS_CUTOFF = 4.5   # Å

contact_summary = {}
for lig in LIGANDS:
    atoms  = parse_pdb_atoms(f'complex_{lig}.pdb')
    lig_at = [a for a in atoms if a['resname']=='LIG']
    rec_at = [a for a in atoms if a['resname']!='LIG']

    contact_res = {}   # (resname, resnum) -> min_dist
    for la in lig_at:
        for ra in rec_at:
            d = np.sqrt((la['x']-ra['x'])**2 + (la['y']-ra['y'])**2 + (la['z']-ra['z'])**2)
            if d < CONTACTS_CUTOFF:
                key = (ra['resname'], ra['resnum'])
                contact_res[key] = min(contact_res.get(key, 99.), d)

    # Sort by distance
    sorted_contacts = sorted(contact_res.items(), key=lambda x: x[1])[:10]
    contact_summary[lig] = sorted_contacts

    trp_contacts = [(k, v) for k,v in sorted_contacts if k[0]=='TRP']
    other_key    = [(k, v) for k,v in sorted_contacts if k[0] not in ('TRP',)][:5]

    print(f"\n{lig}:")
    if trp_contacts:
        print(f"  TRP contacts: " + ", ".join(f"{k[0]}{k[1]} ({v:.1f}Å)" for k,v in trp_contacts))
    all_str = ", ".join(f"{k[0]}{k[1]} ({v:.1f}Å)" for k,v in sorted_contacts)
    print(f"  All top-10:   {all_str}")
