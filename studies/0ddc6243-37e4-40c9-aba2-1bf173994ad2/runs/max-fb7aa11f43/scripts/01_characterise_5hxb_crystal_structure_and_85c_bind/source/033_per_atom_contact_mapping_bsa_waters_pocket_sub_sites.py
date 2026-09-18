
# Per-atom contact mapping, BSA, waters, pocket sub-sites
import gemmi, numpy as np
from collections import defaultdict

# --- Per-ligand-atom contact assignment ---
def get_res_contacts_peratom(chain, lig_atoms, cutoff=4.5):
    """Return {res_id: [(lig_atom_name, dist), ...]}"""
    contacts = defaultdict(list)
    for res in chain:
        if res.entity_type != gemmi.EntityType.Polymer:
            continue
        heavy_res = [(atom.name, np.array([atom.pos.x, atom.pos.y, atom.pos.z]))
                     for atom in res if atom.element.atomic_number > 1]
        if not heavy_res:
            continue
        for la in lig_atoms:
            for ra_name, ra_xyz in heavy_res:
                d = float(np.linalg.norm(la['xyz'] - ra_xyz))
                if d < cutoff:
                    key = f"{res.name}{res.seqid.num}"
                    contacts[key].append((la['name'], ra_name, round(d, 2)))
    return contacts

crbn_atom = get_res_contacts_peratom(model['Z'], lig_Z)
gspt1_atom = get_res_contacts_peratom(model['X'], lig_Z)

# Which ligand atoms contact CRBN vs GSPT1?
crbn_lig_atoms = set()
gspt1_lig_atoms = set()
for v in crbn_atom.values():
    for la, ra, d in v:
        crbn_lig_atoms.add(la)
for v in gspt1_atom.values():
    for la, ra, d in v:
        gspt1_lig_atoms.add(la)
bridge_atoms = crbn_lig_atoms & gspt1_lig_atoms
crbn_only_atoms = crbn_lig_atoms - gspt1_lig_atoms
gspt1_only_atoms = gspt1_lig_atoms - crbn_lig_atoms

print("Ligand atoms by contact type:")
print(f"  CRBN-only:    {sorted(crbn_only_atoms)}")
print(f"  GSPT1-only:   {sorted(gspt1_only_atoms)}")
print(f"  Bridge(both): {sorted(bridge_atoms)}")

# Closest contacts per CRBN residue with ligand atom name
print("\nCRBN anchor contacts (with closest ligand atom):")
for res_key, pairs in sorted(crbn_atom.items(), key=lambda x: min(p[2] for p in x[1])):
    best = min(pairs, key=lambda p: p[2])
    bfac = next((a['bfac'] for a in lig_Z if a['name'] == best[0]), 0)
    print(f"  {res_key:8s}  {best[0]:4s}–{best[1]:4s}  {best[2]:.2f} Å  (lig B={bfac:.0f})")

print("\nGSPT1 bridging contacts (with closest ligand atom):")
for res_key, pairs in sorted(gspt1_atom.items(), key=lambda x: min(p[2] for p in x[1])):
    best = min(pairs, key=lambda p: p[2])
    bfac = next((a['bfac'] for a in lig_Z if a['name'] == best[0]), 0)
    print(f"  {res_key:8s}  {best[0]:4s}–{best[1]:4s}  {best[2]:.2f} Å  (lig B={bfac:.0f})")
