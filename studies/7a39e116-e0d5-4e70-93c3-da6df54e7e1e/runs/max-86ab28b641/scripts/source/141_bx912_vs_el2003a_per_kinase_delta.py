
# BX912 vs EL2003A: per-kinase delta
delta = (pivot.loc['BX912'] - pivot.loc['EL2003A']).sort_values(ascending=False)

print("BX912 vs EL2003A — pIC50 difference (BX912 − EL2003A)")
print(f"{'Kinase':20s}  {'BX912':7s}  {'EL2003A':8s}  {'Delta':7s}")
print("-" * 50)
for k, d in delta.items():
    marker = " ***" if d >= 0.3 else (" *" if d >= 0.15 else "")
    print(f"  {k:20s}  {pivot.loc['BX912',k]:.3f}    {pivot.loc['EL2003A',k]:.3f}    {d:+.3f}{marker}")
