
# Prepare DeepPurpose inputs
train_smiles = df_dp['smiles'].tolist()
train_seqs   = df_dp['seq'].tolist()
train_labels = df_dp['pchembl'].tolist()

pred_smiles  = df_pred['smiles'].tolist()   # all CHEMBL3916849
pred_seqs    = df_pred['seq'].tolist()

print(f"Training: {len(train_smiles)} pairs")
print(f"Prediction: {len(pred_smiles)} pairs")
print(f"Label range: {min(train_labels):.2f} – {max(train_labels):.2f}")
print(f"Pred SMILES unique: {len(set(pred_smiles))} (should be 1)")

# Dispatch
result = dispatch(
    'deeppurpose',
    {
        "drug_smiles":      train_smiles,
        "target_sequences": train_seqs,
        "labels":           train_labels,
        "drug_encoding":    "CNN",
        "target_encoding":  "CNN",
        "train_epoch":      15,
        "LR":               0.001,
        "batch_size":       64,
        "frac":             [0.7, 0.1, 0.2],
        "random_seed":      42,
        "predict_smiles":   pred_smiles,
        "predict_targets":  pred_seqs
    },
    gpu=True
)
print("\n=== DeepPurpose result ===")
print("Summary:", result.get('summary'))
print("Task:", result.get('task'))
print("Test metric:", result.get('test_metric'))
print("Device:", result.get('device'))
print("Num pairs scored:", result.get('num_pairs_scored'))
