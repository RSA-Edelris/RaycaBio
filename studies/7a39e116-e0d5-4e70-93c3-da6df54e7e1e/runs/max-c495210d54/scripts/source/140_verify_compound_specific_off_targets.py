
# --- Verify compound-specific off-targets ---
print("--- Compound-specific off-targets (max >= 7.05, std >= 0.12) ---")
print(f"{'Kinase':20s}  {'Max':6s}  {'Top compound':20s}  {'Std':6s}")
for k in pivot.columns:
    if k == 'PDK1':
        continue
    mx = pivot[k].max()
    sd = pivot[k].std()
    if mx >= 7.05 and sd >= 0.12:
        top_cmpd = pivot[k].idxmax()
        print(f"  {k:20s}  {mx:.3f}  {top_cmpd:20s}  {sd:.3f}")

# --- Verify EL2003A-A4U1 FGFR1 score ---
print(f"\n--- EL2003A-A4U1 FGFR1 ---")
print(f"  pIC50 = {pivot.loc['EL2003A-A4U1','FGFR1']:.3f}")

# --- Verify EL5001A selectivity ---
print(f"\n--- EL5001A: top off-target relative to PDK1 ---")
pdk1_el5001a = pivot.loc['EL5001A', 'PDK1']
deltas = (pivot.loc['EL5001A'] - pdk1_el5001a).drop('PDK1').sort_values(ascending=False)
print(f"  PDK1 pIC50 = {pdk1_el5001a:.3f}")
for k, d in deltas.head(5).items():
    print(f"  {k}: {pivot.loc['EL5001A',k]:.3f} (delta = {d:+.3f})")

# --- Verify file sizes ---
import os
files_to_check = {
    'kinome_selectivity_matrix.csv': f"{WS}/kinome_selectivity_matrix.csv",
    'kinome_heatmap.png':           f"{WS}/kinome_heatmap.png",
    'kinome_per_compound.png':      f"{WS}/kinome_per_compound.png",
}
print("\n--- Output file sizes ---")
for name, path in files_to_check.items():
    if os.path.exists(path):
        sz = os.path.getsize(path)
        print(f"  {name}: {sz:,} bytes ({sz//1024} KB)")
    else:
        print(f"  MISSING: {name}")
