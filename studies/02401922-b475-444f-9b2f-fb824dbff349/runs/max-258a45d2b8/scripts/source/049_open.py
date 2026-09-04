
with open('FINAL_RESULTS_MMGBSA.dat') as f:
    content = f.read()

# Extract all delta values
import re
lines = content.split('\n')
in_diff = False
delta_vals = {}
for l in lines:
    if 'Differences' in l:
        in_diff = True
    if in_diff:
        m = re.match(r'\s*([\w\s]+?)\s{2,}([-\d\.]+)', l)
        if m:
            key = m.group(1).strip()
            val = float(m.group(2))
            delta_vals[key] = val

print("=== MM/GBSA Results (Single-frame, igb=5, 0.15M salt) ===")
for k,v in delta_vals.items():
    print(f"  {k:<25s}: {v:+.2f} kcal/mol")

# Key binding energy
print(f"\nΔG_bind (MM/GBSA) = {delta_vals.get('DELTA TOTAL', 'N/A'):.2f} kcal/mol")
print(f"  VdW contribution : {delta_vals.get('VDWAALS', 'N/A'):.2f} kcal/mol")
print(f"  Electrostatic    : {delta_vals.get('EEL', 'N/A'):.2f} kcal/mol")
print(f"  GB solvation     : {delta_vals.get('EGB', 'N/A'):.2f} kcal/mol")
print(f"  SASA             : {delta_vals.get('ESURF', 'N/A'):.2f} kcal/mol")
