
result = dispatch(
    'deeppurpose',
    {
        "drug_smiles":      train_s,
        "target_sequences": train_sq,
        "labels":           train_l,
        "drug_encoding":    "CNN",
        "target_encoding":  "CNN",
        "train_epoch":      15,
        "LR":               0.001,
        "batch_size":       32,
        "frac":             [0.7, 0.1, 0.2],
        "random_seed":      42,
        "predict_smiles":   pred_s,
        "predict_targets":  pred_sq
    },
    gpu=True
)
print("=== DeepPurpose ===")
print("Summary:", result.get('summary'))
print("Task:", result.get('task'))
print("Test metric:", result.get('test_metric'))
print("Device:", result.get('device'))
print("Num scored:", result.get('num_pairs_scored'))
preds = result.get('predictions', [])
print(f"Predictions ({len(preds)}):", [round(p,3) for p in preds[:10]])
