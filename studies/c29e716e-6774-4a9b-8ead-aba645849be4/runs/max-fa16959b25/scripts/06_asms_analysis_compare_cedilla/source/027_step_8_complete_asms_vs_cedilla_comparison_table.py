
# Step 8: Complete ASMS vs Cedilla comparison table
print("=== FULL ASMS_active vs Cedilla comparison ===\n")

from rdkit.Chem import AllChem, DataStructs

def get_fp(mol):
    return AllChem.GetMorganFingerprintAsBitVect(mol, 2, 2048) if mol else None

ced_dedup_fps = [(row['Molecule Name'], get_fp(row['std_mol']), row['pIC50_num'])
                  for _, row in ced_dedup.iterrows() if row['std_mol'] is not None]

print(f"{'EDS_Number':<15} {'Rank':>5} {'AS':>8} {'MW':>5} {'LogP':>5} "
      f"{'PAINS':<25} {'Brenk':<22} "
      f"{'NearestCTX':<15} {'Sim':>5} {'CTX_pIC50':>10} {'Novel?':<7}")
print("-"*130)

for _, arow in asms_df.sort_values('Hit_rank').iterrows():
    afp = get_fp(arow['std_mol'])
    if afp is None: continue
    sims = [(cname, DataStructs.TanimotoSimilarity(afp, cfp), pic50)
            for cname, cfp, pic50 in ced_dedup_fps]
    best = max(sims, key=lambda x: x[1])
    novel = 'YES' if best[1] < 0.4 else ('~' if best[1] < 0.5 else 'no')
    pains_flag = arow['pains'] if arow['pains'] else '-'
    brenk_flag = arow['brenk'] if arow['brenk'] else '-'
    print(f"{arow['EDS_Number']:<15} {str(arow['Hit_rank']):>5} {float(arow['AS ratio']):>8.4f} "
          f"{arow['MW']:>5.0f} {arow['LogP']:>5.2f} "
          f"{pains_flag[:25]:<25} {brenk_flag[:22]:<22} "
          f"{best[0]:<15} {best[1]:>5.3f} {str(best[2]):>10} {novel:<7}")
