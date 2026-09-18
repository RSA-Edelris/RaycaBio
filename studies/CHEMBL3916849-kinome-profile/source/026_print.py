
import pandas as pd, numpy as np

out = result['output']
preds = out['predictions']
print(f"Model: CNN/CNN | Train epochs: 15 | Test MSE: {out['summary'].split('MSE=')[1]}")
print(f"Training pairs used: 56 (of 80, after 70% split)")
print(f"Predictions: {len(preds)}")

# Map predictions to kinase names
pred_df = df_pred.copy()
pred_df['pred_pchembl'] = preds
pred_df['pred_nM'] = 10**(-pred_df['pred_pchembl'] + 9)  # convert pChEMBL (pM->pKd nM)

# Known experimental values for context
known = {
    'AURKA': ('O14965', 13.79),   # Kd nM
    'MARK4': ('Q96L34', 338.0),   # IC50 nM
    'MARK3': ('P27448', 3333.0),  # IC50 nM
    'TBK1':  ('Q9UHD2', 2327.0),  # IC50 nM
}

pred_df['known_nM'] = pred_df['acc'].map({a: v for n,(a,v) in known.items()})
pred_df_sorted = pred_df.sort_values('pred_pchembl', ascending=False)

print("\n=== KINOME-WIDE PREDICTIONS (ranked) ===")
print(f"{'Rank':>4} {'Name':>12} {'UniProt':>8} {'pred_pChEMBL':>12} {'pred_nM':>10} {'known_nM':>10}")
print("-"*62)
for i, (_, row) in enumerate(pred_df_sorted.iterrows(), 1):
    known_str = f"{row['known_nM']:.0f}" if pd.notna(row['known_nM']) else "—"
    print(f"{i:>4} {row['name']:>12} {row['acc']:>8} {row['pred_pchembl']:>12.3f} {row['pred_nM']:>10.1f} {known_str:>10}")
