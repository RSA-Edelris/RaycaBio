
import pandas as pd

# Merge docking scores with ADME
merged = best.merge(adme_df[['name','mw','logp','hbd','hba','tpsa','rotb','pains','ro5_viol','adme_pass','cpd_type','as_ratio']], 
                    on='name')

# Separate actives and designed
act_m = merged[merged.cpd_type == 'active'].copy()
des_m = merged[merged.cpd_type == 'designed'].copy()

# Rank designed by Vina affinity (most negative = best)
des_ranked = des_m.sort_values('vina').copy()
des_ranked['rank'] = range(1, len(des_ranked)+1)

# ADME-passing subset
des_pass = des_ranked[des_ranked.adme_pass].copy()
des_pass = des_pass.reset_index(drop=True)
des_pass['synth_rank'] = range(1, len(des_pass)+1)

cols = ['synth_rank','name','vina','cnn_aff','mw','logp','hbd','tpsa','rotb']
print("=== DESIGNED ANALOGUES: ADME-PASSING, RANKED BY VINA ===\n")
print(des_pass[cols].to_string(index=False))

print("\n\n=== ADME-FAILING DESIGNED (shown for completeness) ===")
des_fail = des_ranked[~des_ranked.adme_pass][['name','vina','cnn_aff','mw','logp','tpsa','pains','ro5_viol']]
print(des_fail.to_string(index=False))
