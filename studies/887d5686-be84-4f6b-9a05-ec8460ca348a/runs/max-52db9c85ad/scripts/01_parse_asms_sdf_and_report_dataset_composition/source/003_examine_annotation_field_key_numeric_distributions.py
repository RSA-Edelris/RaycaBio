
# Examine the annotation field and key numeric distributions
import statistics

hit_values = Counter(r.get('HIT P841', '') for r in records)
print("HIT P841 unique values:", dict(hit_values))

rt_check = Counter(r.get('RT check manual', '') for r in records)
print("\nRT check manual:", dict(rt_check))

stereo = Counter(r.get('Stereo  Configuration', '') for r in records)
print("\nStereo Configuration:", dict(stereo))

# Numeric fields
as_ratios, as_ratios2, avg_brs, hit_ranks = [], [], [], []
for r in records:
    try: as_ratios.append(float(r['AS ratio']))
    except: pass
    try: as_ratios2.append(float(r['AS ratio 2']))
    except: pass
    try: avg_brs.append(float(r['Avg BR']))
    except: pass
    try: hit_ranks.append(int(r['Hit_rank']))
    except: pass

def stats(name, vals):
    vals_s = sorted(vals)
    n = len(vals_s)
    print(f"\n{name} (n={n}):")
    print(f"  min={vals_s[0]:.4f}  max={vals_s[-1]:.4f}")
    print(f"  median={vals_s[n//2]:.4f}  mean={sum(vals_s)/n:.4f}")
    for pct in [25, 75, 90, 95, 99]:
        idx = int(pct/100 * n)
        print(f"  p{pct}={vals_s[idx]:.4f}")

stats("AS ratio", as_ratios)
stats("AS ratio 2", as_ratios2)
stats("Avg BR (Binding Ratio)", avg_brs)
stats("Hit_rank", hit_ranks)
