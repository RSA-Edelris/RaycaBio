
# Identify interface residues by name/number, ligand pocket residues, check CIF for pLDDT
import gemmi, numpy as np, json

BASE = "/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b/job-6567207/ternary_out"

def parse_pdb_full(path):
    st = gemmi.read_structure(path)
    model = st[0]
    chains = {}
    for chain in model:
        records = []
        for res in chain:
            for atom in res:
                records.append({
                    'xyz': np.array([atom.pos.x, atom.pos.y, atom.pos.z]),
                    'bfactor': atom.b_iso,
                    'name': atom.name,
                    'resname': res.name,
                    'seqid': res.seqid.num,
                })
        chains[chain.name] = records
    return chains

def get_ca_records(records):
    return [r for r in records if r['name'] == 'CA']

# Model 0 detailed analysis
ch = parse_pdb_full(f"{BASE}/gspt1_crbn_glue_0.pdb")

ca_A = get_ca_records(ch['A'])
ca_B = get_ca_records(ch['B'])

xyz_A = np.array([r['xyz'] for r in ca_A])
xyz_B = np.array([r['xyz'] for r in ca_B])

# Interface residues at CA-CA ≤ 8 Å
dist_AB = np.sqrt(((xyz_A[:, None, :] - xyz_B[None, :, :])**2).sum(-1))
in_contact_A = np.where(dist_AB.min(axis=1) < 8.0)[0]
in_contact_B = np.where(dist_AB.min(axis=0) < 8.0)[0]

gspt1_interface = [(ca_A[i]['seqid'], ca_A[i]['resname']) for i in in_contact_A]
crbn_interface  = [(ca_B[i]['seqid'], ca_B[i]['resname']) for i in in_contact_B]

print("Model 0 GSPT1 interface residues (seq#, resname):")
print(gspt1_interface[:20], "..." if len(gspt1_interface) > 20 else "")
print(f"  range: {min(x[0] for x in gspt1_interface)} – {max(x[0] for x in gspt1_interface)}")

print("\nModel 0 CRBN interface residues (seq#, resname):")
print(crbn_interface[:20], "..." if len(crbn_interface) > 20 else "")
print(f"  range: {min(x[0] for x in crbn_interface)} – {max(x[0] for x in crbn_interface)}")

# Ligand contacts with CRBN — which CRBN residues?
lig_xyz = np.array([r['xyz'] for r in ch['C']])
hvy_B = []
for res in ch['B']:
    pass  # need to group by residue

# Group CRBN atoms by residue
from collections import defaultdict
crbn_by_res = defaultdict(list)
for r in ch['B']:
    crbn_by_res[r['seqid']].append(r)

lig_contacts = []
for seqid, atoms in sorted(crbn_by_res.items()):
    xyz_res = np.array([a['xyz'] for a in atoms])
    min_d = float(np.sqrt(((lig_xyz[:, None, :] - xyz_res[None, :, :])**2).sum(-1)).min())
    if min_d < 4.5:
        lig_contacts.append((seqid, atoms[0]['resname'], round(min_d, 2)))

print(f"\nModel 0 CRBN residues within 4.5 Å of ligand:")
print(lig_contacts)

# Check CIF for confidence/pLDDT records
cif_path = f"{BASE}/gspt1_crbn_glue_0.cif"
doc = gemmi.cif.read(cif_path)
block = doc.sole_block()
categories = [item.pair[0].split('.')[0] if item.pair else item.loop.tags[0].split('.')[0] 
              for item in block]
unique_cats = sorted(set(categories))
print("\nCIF categories:")
print(unique_cats)

# Try to find pLDDT / confidence in CIF
for tag_name in ['_atom_site.B_iso_or_equiv', '_ma_qa_metric_local.metric_value']:
    try:
        col = block.find_values(tag_name)
        vals = [float(v) for v in col]
        print(f"\n{tag_name}: n={len(vals)}, mean={np.mean(vals):.2f}, range=[{min(vals):.2f},{max(vals):.2f}]")
    except Exception as e:
        print(f"{tag_name}: {e}")
