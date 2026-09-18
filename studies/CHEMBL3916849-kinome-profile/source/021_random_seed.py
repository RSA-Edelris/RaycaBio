
import random, json
random.seed(42)

# Truncate sequences to 300 AA (covers kinase domain for most)
MAX_SEQ = 300

# Stratified downsample: 80 training pairs, keep pchembl distribution
df_dp['pchembl_bin'] = pd.cut(df_dp['pchembl'], bins=[5,6,7,8,9,11], labels=['5-6','6-7','7-8','8-9','9+'])
sampled = df_dp.groupby('pchembl_bin', group_keys=False).apply(
    lambda g: g.sample(min(len(g), 16), random_state=42)
).reset_index(drop=True)
print(f"Sampled training pairs: {len(sampled)}")
print(sampled['pchembl_bin'].value_counts().sort_index())

train_s  = sampled['smiles'].tolist()
train_sq = [s[:MAX_SEQ] for s in sampled['seq'].tolist()]
train_l  = sampled['pchembl'].tolist()

pred_s   = pred_smiles  # already short (1 unique SMILES)
pred_sq  = [s[:MAX_SEQ] for s in pred_seqs]

# Estimate payload size
payload = json.dumps({
    "drug_smiles": train_s, "target_sequences": train_sq, "labels": train_l,
    "drug_encoding": "CNN", "target_encoding": "CNN", "train_epoch": 15,
    "frac": [0.7, 0.1, 0.2], "random_seed": 42,
    "predict_smiles": pred_s, "predict_targets": pred_sq
})
print(f"\nPayload size: {len(payload)/1024:.1f} KB")
