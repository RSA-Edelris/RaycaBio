
dg_vals = {k: v['DELTA_TOTAL'] for k, v in data.items() if isinstance(v, dict) and 'DELTA_TOTAL' in v}
print(f"dG range: {min(dg_vals.values()):.1f} to {max(dg_vals.values()):.1f} kcal/mol")
best = min(dg_vals, key=lambda k: dg_vals[k])
worst = max(dg_vals, key=lambda k: dg_vals[k])
print(f"Best: {best} = {dg_vals[best]:.1f}")
print(f"Worst: {worst} = {dg_vals[worst]:.1f}")
print(f"N = {len(dg_vals)}")
