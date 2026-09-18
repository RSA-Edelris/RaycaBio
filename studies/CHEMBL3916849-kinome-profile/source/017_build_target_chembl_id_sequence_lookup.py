
import pandas as pd, json

# Build target_chembl_id -> sequence lookup
target_seq_lookup = {}
for cid, info in training_targets.items():
    acc = info['uniprot']
    if acc in seq_map:
        target_seq_lookup[cid] = seq_map[acc]

# Assemble training pairs
rows = []
for _, row in df_train.iterrows():
    mid = row['molecule_chembl_id']
    tid = row['target_chembl_id']
    pval = row['pchembl_value']
    smiles = smiles_map2.get(mid)
    seq = target_seq_lookup.get(tid)
    if smiles and seq and pval:
        rows.append({'smiles': smiles, 'seq': seq, 'pchembl': float(pval)})

df_dp = pd.DataFrame(rows).drop_duplicates(subset=['smiles','seq'])
print(f"Training pairs: {len(df_dp)}")
print(f"pchembl range: {df_dp['pchembl'].min():.1f} – {df_dp['pchembl'].max():.1f}, mean={df_dp['pchembl'].mean():.2f}")

# Build prediction pairs: CHEMBL3916849 vs each kinase in panel
QUERY_SMILES = "O=C(Nc1cccc(Nc2ncc(Br)c(NCCc3cnc[nH]3)n2)c1)N1CCCC1"

pred_pairs = []
for acc, name in KINOME_PANEL.items():
    if acc in seq_map:
        pred_pairs.append({'smiles': QUERY_SMILES, 'seq': seq_map[acc], 
                           'acc': acc, 'name': name})

df_pred = pd.DataFrame(pred_pairs)
print(f"Prediction pairs: {len(df_pred)}")

# Check sizes are valid
print(f"\nTraining: {len(df_dp)} pairs, Prediction: {len(df_pred)} kinases")
print("First training pair:", df_dp.iloc[0]['smiles'][:40], "...", df_dp.iloc[0]['seq'][:20], "...", df_dp.iloc[0]['pchembl'])
