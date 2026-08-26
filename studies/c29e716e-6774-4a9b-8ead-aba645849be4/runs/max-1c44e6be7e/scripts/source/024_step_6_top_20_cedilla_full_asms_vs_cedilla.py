
# Step 6: Top 20 Cedilla + full ASMS vs Cedilla comparison table
from rdkit.Chem import rdFMCS

# Top 20 Cedilla structures
top20 = ced_df.nlargest(20,'pIC50_num')[['Molecule Name','pIC50_num','can_smiles','MW','LogP','HBD','HBA','RotB','pains','brenk',
    'Pharmaron Caliper Assay (CDK2/CCNE1): IC50 - Batch Mean (uM)',
    'Pharmaron Solubility (PBS, pH 7.4): Aqueous Solubility - Batch Mean (uM)',
    'HLM: t1/2 - Batch Mean (Min)','HLM: ER (Hepatic extraction ratio) - Batch Mean',
    'RLM: t1/2 - Batch Mean (Min)','RLM: ER (Hepatic extraction ratio) - Batch Mean']].copy()

print("Top 20 Cedilla compounds:")
print(f"{'Name':<15} {'pIC50':>6} {'IC50uM':>8} {'MW':>5} {'LogP':>5} {'Sol_uM':>8} {'HLM_t12':>8} {'HLM_ER':>7} {'PAINS':<25}")
for _, r in top20.iterrows():
    sol  = str(r['Pharmaron Solubility (PBS, pH 7.4): Aqueous Solubility - Batch Mean (uM)'])[:7]
    hlm  = str(r['HLM: t1/2 - Batch Mean (Min)'])[:6]
    hlmer= str(r['HLM: ER (Hepatic extraction ratio) - Batch Mean'])[:5]
    cal  = str(r['Pharmaron Caliper Assay (CDK2/CCNE1): IC50 - Batch Mean (uM)'])[:8]
    print(f"{r['Molecule Name']:<15} {r['pIC50_num']:>6.2f} {cal:>8} {r['MW']:>5.0f} {r['LogP']:>5.2f} {sol:>8} {hlm:>8} {hlmer:>7} {r['pains'][:25]}")

# MCS across top 20 Cedilla
top20_mols = [m for m in top20['std_mol'] if m is not None]
# std_mol not in top20 yet - need to fetch from ced_df
top20_names = set(top20['Molecule Name'])
top20_mols = [ced_df.loc[i,'std_mol'] for i in ced_df.index 
              if ced_df.loc[i,'Molecule Name'] in top20_names and ced_df.loc[i,'std_mol'] is not None]
mcs = rdFMCS.FindMCS(top20_mols, ringMatchesRingOnly=True, completeRingsOnly=True, timeout=20)
print(f"\nMCS across top-20 Cedilla: {mcs.numAtoms} atoms, {mcs.numBonds} bonds")
print(f"  SMARTS: {mcs.smartsString}")
