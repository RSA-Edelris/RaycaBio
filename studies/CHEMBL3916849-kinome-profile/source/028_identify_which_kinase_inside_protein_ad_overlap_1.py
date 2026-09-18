
import numpy as np

# Identify which kinase is inside protein AD (overlap = 1.000)
def kmer_overlap(s1, s2, k=5):
    k1 = set(s1[i:i+k] for i in range(len(s1)-k+1))
    k2 = set(s2[i:i+k] for i in range(len(s2)-k+1))
    return len(k1 & k2) / max(len(k1 | k2), 1)

train_seqs_uniq = list(set(train_sq))
for i, (ps, name, acc) in enumerate(zip(pred_sq, df_pred['name'].tolist(), df_pred['acc'].tolist())):
    ovlps = [kmer_overlap(ps, ts) for ts in train_seqs_uniq]
    if max(ovlps) >= 0.40:
        best = max(ovlps)
        # Find which training target it matches
        best_ts_idx = np.argmax(ovlps)
        best_ts = train_seqs_uniq[best_ts_idx]
        # Find ChEMBL ID
        match_cid = [cid for cid, info in training_targets.items()
                     if info.get('uniprot') in seq_map and 
                     seq_map[info['uniprot']][:MAX_SEQ] == best_ts]
        print(f"Kinase IN protein AD: {name} ({acc}), overlap={best:.3f}")
        print(f"  Matches training target: {match_cid}")
        if match_cid:
            print(f"  Name: {training_targets[match_cid[0]]['name']}")

# Compute final stats for report
print("\n=== MODEL PERFORMANCE SUMMARY ===")
print(f"Training pairs:    80 total (56 train / 8 val / 16 test)")
print(f"Unique proteins:   12")
print(f"Unique compounds:  76")
print(f"Test MSE:          2.265  (RMSE = {2.265**0.5:.3f} pChEMBL)")
print(f"Prediction range:  {min(preds):.3f}–{max(preds):.3f} pChEMBL (Δ={max(preds)-min(preds):.3f})")
print(f"Training mean:     {np.mean(train_l):.3f} pChEMBL")
print(f"\nAD: Chemical  — max Tc = 0.211 (threshold 0.40) → ALL OOD")
print(f"AD: Protein   — 1/40 kinases match training protein (see above)")
print(f"AD: Combined  — 0/40 predictions inside full AD (both conditions)")
