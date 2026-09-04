
from rdkit.Chem import SDWriter

out_path = '/home/ubuntu/rayca-sessions/c29e716e-6774-4a9b-8ead-aba645849be4-01def6985d02/library_200.sdf'

writer = SDWriter(out_path)

for _, row in sel_df.iterrows():
    mol = Chem.MolFromSmiles(row['smiles'])
    if mol is None:
        continue
    # Add 2D coords
    from rdkit.Chem import rdDepictor
    rdDepictor.Compute2DCoords(mol)
    
    # Set properties
    mol.SetProp('Compound_ID',   str(row['compound_id']))
    mol.SetProp('SMILES',        str(row['smiles']))
    mol.SetProp('R1_reagent',    str(row['r1_smi']))
    mol.SetProp('R1_ID',         str(row['r1_id']))
    mol.SetProp('N_reaction',    'Amidation' if row['rxn_type']=='amide' else 'Reductive_amination')
    mol.SetProp('R2_amine',      str(row['r2_smi']))
    mol.SetProp('R2_ID',         str(row['r2_id']))
    mol.SetProp('MW',            str(row['MW']))
    mol.SetProp('LogP',          str(row['LogP']))
    mol.SetProp('HBD',           str(row['HBD']))
    mol.SetProp('HBA',           str(row['HBA']))
    mol.SetProp('RotB',          str(row['RotB']))
    mol.SetProp('ASMS_similarity', str(row['asms_sim']))
    # Priority tier
    sim = row['asms_sim']
    if sim >= 0.75:
        tier = 'Tier1_high'
    elif sim >= 0.60:
        tier = 'Tier2_medium'
    else:
        tier = 'Tier3_explore'
    mol.SetProp('Priority_tier', tier)
    mol.SetProp('Scaffold', 'OC(=O)c1ccc2CCNCc2n1')
    
    writer.write(mol)

writer.close()
import os
size_kb = os.path.getsize(out_path) // 1024
print(f"Written: {out_path} ({size_kb} KB)")
print(f"\nPriority distribution:")
print(sel_df['asms_sim'].apply(lambda s: 'Tier1' if s>=0.75 else ('Tier2' if s>=0.60 else 'Tier3')).value_counts())
print(f"\nSample entries (first 5):")
print(sel_df[['compound_id','rxn_type','MW','LogP','asms_sim']].head(5).to_string())
