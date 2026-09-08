
print("\n" + "═"*90)
print("REJECTED COMPOUNDS — each row shows which filter failed (nothing disappears silently)")
print("═"*90)
rej_header = f"{'CR_ID':<12}  {'MW':>6}  {'cLogP':>6}  {'logS':>6}  {'PAMPA':>6}  {'hERG':>6}  {'CYP':>6}  {'MPO':>6}  Failed criterion"
print(rej_header)
print('-'*len(rej_header))

# Sort rejected by MPO desc
rejected_sorted = sorted(rejected, key=lambda r: -r['mpo_score'])
for row in rejected_sorted:
    print(f"{row['cr_id']:<12}  {row['mw']:>6.0f}  {row['clogp']:>6.2f}  "
          f"{row['sol_logS']:>6.2f}  {row['pampa_pampa_cat']:>6}  "
          f"{row['herg_herg_risk']:>6}  {row['cyp_cyp_risk']:>6}  "
          f"{row['mpo_score']:>6.4f}  {row['filter_fails']}")

print()
print("═"*90)
print("STRUCTURAL-OVERRIDE CANDIDATES")
print("  Definition: rejected by exactly 1 filter, MPO ≥ 0.55, and structural rationale noted.")
print("  These should be discussed before automatic discard.")
print("═"*90)
ov_header = f"{'CR_ID':<12}  {'MW':>6}  {'cLogP':>6}  {'logS':>6}  {'PAMPA':>6}  {'hERG':>6}  {'MPO':>6}  Failed  Structural note"
print(ov_header)
print('-'*len(ov_header))

for row in override_candidates:
    # Build structural note
    notes = []
    if row['sol_logS'] < -5.5:
        notes.append(f"logS={row['sol_logS']:.2f}: high-Ar scaffold; may dissolve better in DMSO stock + dilution protocol")
    if row['herg_herg_risk'] == 'High':
        notes.append("hERG-High: confirm with patch-clamp; basic-N could be profiled")
    if row['cyp_cyp_risk'] == 'High':
        notes.append("Multi-CYP: acceptable if used as tool compound only")
    if row['pampa_pampa_cat'] == 'Low':
        notes.append("Low PAMPA: consider formulation or prodrug; still usable for biochemical assay")
    note = '; '.join(notes) if notes else 'borderline'
    print(f"{row['cr_id']:<12}  {row['mw']:>6.0f}  {row['clogp']:>6.2f}  "
          f"{row['sol_logS']:>6.2f}  {row['pampa_pampa_cat']:>6}  "
          f"{row['herg_herg_risk']:>6}  {row['mpo_score']:>6.4f}  "
          f"{row['filter_fails'][:22]:<22}  {note}")

# Desirability function summary
print()
print("═"*90)
print("MPO DESIGN — desirability function per property")
print("═"*90)
rows_fmt = [
    ("Solubility (logS)",        "1.5", "Linear 0→1 from logS -5.5 to -3.0",           "Cell assays need ≥10 µM; -5.5 = 3 µM floor"),
    ("cLogP",                    "1.0", "Trapezoid: 0 at ≤0, 1 at 2-4, 0 at ≥5.5",   "PPI interfaces hydrophobic; 2-4 optimal"),
    ("PAMPA logPapp",            "1.5", "Linear 0→1 from logPapp -7.0 to -5.5",         "Cell permeability needed; intracellular target"),
    ("MetStab score",            "1.5", "Direct: 0-1 continuous scale",                  "HLM stability feeds in-vivo window"),
    ("CYP inhibition",           "1.5", "Low=1.0  Medium=0.5  High=0.0",                "Multi-isoform block → drug interaction risk"),
    ("PPB (fu)",                 "0.5", "fu≥0.05→1.0  0.01-0.05→0.7  <0.01→0.3",      "High PPB expected/accepted for PPI probes"),
    ("hERG risk",                "2.0", "Low=1.0  Medium=0.5  High=0.0",                "Cardiac safety; weight doubled as hard end"),
    ("MW",                       "0.5", "Trapezoid: 0 at ≤200, 1 at 400-650, 0 at ≥850","Informational; larger MW accepted for PPI"),
]
print(f"  {'Property':<25}  {'W':>4}  {'Desirability function':<42}  Rationale")
print(f"  {'-'*25}  {'----':>4}  {'-'*42}  {'-'*40}")
for prop, w, des, rat in rows_fmt:
    print(f"  {prop:<25}  {w:>4}  {des:<42}  {rat}")
print(f"\n  MPO = Σ(weight × desirability) / Σweights  [weighted arithmetic mean, max=1.0]")
print(f"  Total weight = 10.0")
