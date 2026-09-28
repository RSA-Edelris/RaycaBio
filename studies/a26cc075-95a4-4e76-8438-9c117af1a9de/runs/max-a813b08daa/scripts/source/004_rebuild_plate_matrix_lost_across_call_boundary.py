
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.gridspec as gridspec
import matplotlib.colors as mcolors
import matplotlib.cm as cm

# Rebuild plate matrix (lost across call boundary)
plate   = np.zeros((8, 12))
for _, r in df.iterrows():
    ri2, ci2 = int(r['row_idx']), int(r['col_idx']) - 1
    plate[ri2, ci2] = r['norm_yield']

# Rebuild condition pivots (functions dropped; inline here)
def pivot_mean_fn(row_var):
    pv = df.pivot_table(index=row_var, columns='Ligand',
                        values='norm_yield', aggfunc='mean')
    return pv[lig_order]

pv_solv = pivot_mean_fn('Solvent')
pv_base = pivot_mean_fn('Base')
pv_cu   = pivot_mean_fn('Cu')

print("plate max:", plate.max().round(4))
print("pivots shapes:", pv_solv.shape, pv_base.shape, pv_cu.shape)
