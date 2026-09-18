
import statistics, math

data = [
    ("EDS00495858", "active",   1, 2.64317, 15.34862),
    ("EDS00495858", "active",   2, 1.37524, 14.72651),
    ("EDS00495858", "active",   3, 1.23586, 16.74997),
    ("EDS00480994", "active",   1, 1.07282, 15.54088),
    ("EDS00480994", "active",   2, 0.89522, 16.65142),
    ("EDS00480994", "active",   3, 0.14823, 15.46230),
    ("EDS00444974", "active",   1, 2.25385, 13.82830),
    ("EDS00444974", "active",   2, 4.99459, 14.68400),
    ("EDS00444974", "active",   3, 0.54345, 14.33369),
    ("EDS00481054", "inactive", 1, 5.52406, 14.48849),
    ("EDS00481054", "inactive", 2, 4.74020, 15.57081),
    ("EDS00481054", "inactive", 3, 2.37615, 14.45048),
    ("EDS00441134", "inactive", 1, 3.59312, 17.32208),
    ("EDS00441134", "inactive", 2, 0.36212, 15.69135),
    ("EDS00441134", "inactive", 3, 0.22375, 15.63212),
    ("EDS00445742", "inactive", 1, 4.69542, 14.55601),
    ("EDS00445742", "inactive", 2, 1.41630, 14.45069),
    ("EDS00445742", "inactive", 3, 4.76893, 15.85062),
]

compounds = {}
for cid, cls, rep, rmsd, bsa in data:
    if cid not in compounds:
        compounds[cid] = {"class": cls, "rmsd": [], "bsa": []}
    compounds[cid]["rmsd"].append(rmsd)
    compounds[cid]["bsa"].append(bsa)

print("Per-compound summary:")
print(f"{'Compound':<14} {'Class':<8} {'RMSD mean':>10} {'RMSD range':>11} {'BSA mean':>10} {'BSA range':>10}")
for cid, d in compounds.items():
    rm = statistics.mean(d["rmsd"])
    rr = max(d["rmsd"]) - min(d["rmsd"])
    bm = statistics.mean(d["bsa"])
    br = max(d["bsa"]) - min(d["bsa"])
    print(f"{cid:<14} {d['class']:<8} {rm:>10.3f} {rr:>11.3f} {bm:>10.3f} {br:>10.3f}")

active_rmsd_cpd  = [statistics.mean(d["rmsd"]) for d in compounds.values() if d["class"]=="active"]
inactive_rmsd_cpd = [statistics.mean(d["rmsd"]) for d in compounds.values() if d["class"]=="inactive"]
active_bsa_cpd   = [statistics.mean(d["bsa"])  for d in compounds.values() if d["class"]=="active"]
inactive_bsa_cpd  = [statistics.mean(d["bsa"])  for d in compounds.values() if d["class"]=="inactive"]

active_rmsd_all  = [r for (c,cl,rep,r,b) in data if cl=="active"]
inactive_rmsd_all = [r for (c,cl,rep,r,b) in data if cl=="inactive"]

gap = statistics.mean(inactive_rmsd_cpd) - statistics.mean(active_rmsd_cpd)
max_active_range   = max(max(d["rmsd"])-min(d["rmsd"]) for d in compounds.values() if d["class"]=="active")
max_inactive_range = max(max(d["rmsd"])-min(d["rmsd"]) for d in compounds.values() if d["class"]=="inactive")

print()
print("=== RMSD class comparison ===")
print(f"Active   grand mean: {statistics.mean(active_rmsd_cpd):.3f} nm  (SD across 3 compounds: {statistics.stdev(active_rmsd_cpd):.3f})")
print(f"Inactive grand mean: {statistics.mean(inactive_rmsd_cpd):.3f} nm  (SD across 3 compounds: {statistics.stdev(inactive_rmsd_cpd):.3f})")
print(f"Between-class gap: {gap:.3f} nm")
print(f"Max active within-compound range:   {max_active_range:.3f} nm")
print(f"Max inactive within-compound range: {max_inactive_range:.3f} nm")
print(f"Separation criterion met (gap > max range): {gap > max(max_active_range, max_inactive_range)}")

print()
print("=== BSA class comparison ===")
bsa_gap = abs(statistics.mean(inactive_bsa_cpd) - statistics.mean(active_bsa_cpd))
max_active_bsa_range   = max(max(d["bsa"])-min(d["bsa"]) for d in compounds.values() if d["class"]=="active")
max_inactive_bsa_range = max(max(d["bsa"])-min(d["bsa"]) for d in compounds.values() if d["class"]=="inactive")
print(f"Active   BSA grand mean: {statistics.mean(active_bsa_cpd):.3f} nm²")
print(f"Inactive BSA grand mean: {statistics.mean(inactive_bsa_cpd):.3f} nm²")
print(f"Between-class gap: {bsa_gap:.3f} nm²")
print(f"Max active within-compound range:   {max_active_bsa_range:.3f}")
print(f"Max inactive within-compound range: {max_inactive_bsa_range:.3f}")

print()
print("=== Drift rate ===")
n_active_drifted   = sum(1 for r in active_rmsd_all if r > 2.0)
n_inactive_drifted = sum(1 for r in inactive_rmsd_all if r > 2.0)
print(f"Replicas with RMSD>2 nm (pose substantially displaced):")
print(f"  Actives:   {n_active_drifted}/9 = {n_active_drifted/9*100:.0f}%")
print(f"  Inactives: {n_inactive_drifted}/9 = {n_inactive_drifted/9*100:.0f}%")

print()
print("=== MinDist stability ===")
mindists = [0.16793,0.16793,0.16766,0.16708,0.16704,0.16773,
            0.16823,0.16799,0.16941,0.16872,0.16990,0.17059,
            0.16554,0.16743,0.16931,0.16717,0.16732,0.16598]
print(f"All 18 replicas: mean={statistics.mean(mindists)*10:.2f} Å  SD={statistics.stdev(mindists)*10:.2f} Å  range={1000*(max(mindists)-min(mindists)):.0f} pm")
print("Inter-chain complex remains intact throughout for all systems.")
