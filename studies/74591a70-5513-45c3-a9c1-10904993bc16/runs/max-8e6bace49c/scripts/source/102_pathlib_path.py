
import pathlib, hashlib, re

sdf_path = pathlib.Path("/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e/CRBN_32_ligands_docking_GBSA.sdf")
text = sdf_path.read_text()

# Count compounds
n_compounds = text.count("$$$$")
# Get compound IDs
compound_ids = re.findall(r'<Compound_ID>\n(.+)', text)
# Get GBSA_rank values
gbsa_ranks = re.findall(r'<GBSA_rank>\n(.+)', text)
# Get GBSA_dG values
gbsa_dg = re.findall(r'<GBSA_dG_kcal_mol>\n(.+)', text)
# Get Vina_dG values
vina_dg = re.findall(r'<Vina_dG_kcal_mol>\n(.+)', text)
# Get CNN_pKd
cnn = re.findall(r'<CNN_pKd>\n(.+)', text)

# SHA256
sha = hashlib.sha256(sdf_path.read_bytes()).hexdigest()
print(f"File size: {sdf_path.stat().st_size/1024:.1f} KB")
print(f"SHA256: {sha}")
print(f"Compound count ($$$$): {n_compounds}")
print(f"\nFirst compound: {compound_ids[0] if compound_ids else 'N/A'}")
print(f"Last compound: {compound_ids[-1] if compound_ids else 'N/A'}")
print(f"\nGBSA_rank[0]: {gbsa_ranks[0] if gbsa_ranks else 'N/A'}")
print(f"GBSA_rank[-1]: {gbsa_ranks[-1] if gbsa_ranks else 'N/A'}")
print(f"\nGBSA_dG range: {min(float(x) for x in gbsa_dg):.2f} to {max(float(x) for x in gbsa_dg):.2f} kcal/mol")
print(f"Vina_dG range: {min(float(x) for x in vina_dg):.2f} to {max(float(x) for x in vina_dg):.2f} kcal/mol")
print(f"CNN_pKd range: {min(float(x) for x in cnn):.2f} to {max(float(x) for x in cnn):.2f}")

# Check property fields present
prop_tags = ['Compound_ID','Vina_dG_kcal_mol','CNN_pKd','GBSA_dG_kcal_mol','GBSA_dG_std',
             'GBSA_VDWAALS','GBSA_EEL','GBSA_EGB','GBSA_ESURF','GBSA_rank']
for tag in prop_tags:
    count = text.count(f'<{tag}>')
    print(f"  <{tag}>: {count} occurrences")
