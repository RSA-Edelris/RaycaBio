
# Redefine parse_condition (function lost across calls)
def parse_condition(cond):
    parts = cond.split('_')
    for i, p in enumerate(parts):
        if p in ('K3PO4', 'K2CO3'):
            base_idx = i
            break
    return ('_'.join(parts[:base_idx]), parts[base_idx], parts[base_idx+1], parts[base_idx+2])

# df is still in scope; re-apply parse to restore Ligand/Base/Cu/Solvent columns
df[['Ligand','Base','Cu','Solvent']] = df['Condition'].apply(lambda x: pd.Series(parse_condition(x)))

# ── Plate matrix (8 rows × 12 cols) ──────────────────────────────────────────
plate = np.zeros((8, 12))
plate_cond = [['' for _ in range(12)] for _ in range(8)]
for _, r in df.iterrows():
    ri, ci = r['row_idx'], int(r['col_idx']) - 1
    plate[ri, ci] = r['norm_yield']
    plate_cond[ri][ci] = r['Condition']

# ── Condition pivot tables ────────────────────────────────────────────────────
lig_order = (df.groupby('Ligand')['norm_yield'].mean()
               .sort_values(ascending=False).index.tolist())

def pivot_mean(row_var):
    pv = df.pivot_table(index=row_var, columns='Ligand',
                        values='norm_yield', aggfunc='mean')
    return pv[lig_order]

pv_solv = pivot_mean('Solvent')
pv_base = pivot_mean('Base')
pv_cu   = pivot_mean('Cu')

print("Condition pivot shapes ready")
print("Ligand order:", lig_order)
print("Plate matrix max:", plate.max().round(3))
