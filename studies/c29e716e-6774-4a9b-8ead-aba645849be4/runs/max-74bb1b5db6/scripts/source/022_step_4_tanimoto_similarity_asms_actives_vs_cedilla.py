
# Step 4: Tanimoto similarity of ASMS actives vs Cedilla
from rdkit.Chem import AllChem, DataStructs

def get_fp(mol, radius=2, nbits=2048):
    if mol is None: return None
    return AllChem.GetMorganFingerprintAsBitVect(mol, radius, nbits)

asms_fps = [(row['EDS_Number'], get_fp(row['std_mol'])) for _, row in asms_df.iterrows()]
ced_fps  = [(row['Molecule Name'], get_fp(row['std_mol'])) for _, row in ced_df.iterrows()]

# For each ASMS active: best Tanimoto match in Cedilla
print("ASMS active → best Cedilla match (Tanimoto):")
print(f"{'ASMS_ID':<15} {'AS_ratio':<10} {'BestCedilla':<15} {'Sim':>5} {'pIC50':>7} {'CaliperuM':>10}")
print("-"*70)
for eds, afp in asms_fps:
    if afp is None: continue
    sims = [(cname, DataStructs.TanimotoSimilarity(afp, cfp))
            for cname, cfp in ced_fps if cfp is not None]
    best_name, best_sim = max(sims, key=lambda x: x[1])
    c_row = ced_df[ced_df['Molecule Name']==best_name].iloc[0]
    a_row = asms_df[asms_df['EDS_Number']==eds].iloc[0]
    cal = c_row.get('Pharmaron Caliper Assay (CDK2/CCNE1): IC50 - Batch Mean (uM)','')
    print(f"{eds:<15} {str(a_row['AS ratio']):<10} {best_name:<15} {best_sim:>5.3f} {str(c_row['pIC50']):>7} {str(cal):>10}")

# How many ASMS actives are "novel" vs Cedilla (max Tanimoto < 0.4)?
novel_thresh = 0.4
novel_count = 0
for eds, afp in asms_fps:
    if afp is None: continue
    sims = [DataStructs.TanimotoSimilarity(afp, cfp) for _, cfp in ced_fps if cfp is not None]
    if max(sims) < novel_thresh:
        novel_count += 1
print(f"\nASMS actives with max Tanimoto < {novel_thresh} vs Cedilla: {novel_count}/15 (novel chemotypes)")
