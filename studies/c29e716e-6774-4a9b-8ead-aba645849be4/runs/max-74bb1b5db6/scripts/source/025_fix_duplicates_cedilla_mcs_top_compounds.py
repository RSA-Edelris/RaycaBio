
# Fix duplicates in Cedilla + MCS on top compounds
from rdkit.Chem import rdFMCS

# Check duplicates
print(f"Cedilla total rows: {len(ced_df)}")
print(f"Unique Molecule Names: {ced_df['Molecule Name'].nunique()}")
print(f"Unique InChIKeys: {ced_df['inchi_key'].nunique()}")
dup_names = ced_df[ced_df.duplicated('Molecule Name', keep=False)]['Molecule Name'].value_counts().head(10)
print(f"\nDuplicated molecule names (top 10):\n{dup_names}")

# Deduplicate: keep first per InChIKey
ced_dedup = ced_df.drop_duplicates('inchi_key', keep='first').copy()
ced_dedup['pIC50_num'] = pd.to_numeric(ced_dedup['pIC50'], errors='coerce')
print(f"\nAfter dedup: {len(ced_dedup)} unique compounds")

# Top 15 unique by pIC50
top15 = ced_dedup.nlargest(15,'pIC50_num')
print("\nTop 15 unique Cedilla by pIC50:")
print(f"{'Name':<15} {'pIC50':>6} {'IC50uM':>7} {'MW':>5} {'LogP':>5} {'Sol_uM':>8} {'HLM_t12':>8} {'HLM_ER':>7}")
for _, r in top15.iterrows():
    sol   = str(r.get('Pharmaron Solubility (PBS, pH 7.4): Aqueous Solubility - Batch Mean (uM)', ''))[:7]
    hlm   = str(r.get('HLM: t1/2 - Batch Mean (Min)', ''))[:6]
    hlmer = str(r.get('HLM: ER (Hepatic extraction ratio) - Batch Mean', ''))[:5]
    cal   = str(r.get('Pharmaron Caliper Assay (CDK2/CCNE1): IC50 - Batch Mean (uM)', ''))[:7]
    print(f"{r['Molecule Name']:<15} {r['pIC50_num']:>6.2f} {cal:>7} {r['MW']:>5.0f} {r['LogP']:>5.2f} {sol:>8} {hlm:>8} {hlmer:>7}")

# MCS of top 10 unique compounds
top10_mols = [ced_dedup.loc[i,'std_mol'] for i in ced_dedup.nlargest(10,'pIC50_num').index
              if ced_dedup.loc[i,'std_mol'] is not None]
if top10_mols:
    mcs = rdFMCS.FindMCS(top10_mols, ringMatchesRingOnly=True, completeRingsOnly=True, timeout=20)
    print(f"\nMCS top-10 Cedilla: {mcs.numAtoms} atoms, {mcs.numBonds} bonds")
    print(f"  SMARTS: {mcs.smartsString}")
