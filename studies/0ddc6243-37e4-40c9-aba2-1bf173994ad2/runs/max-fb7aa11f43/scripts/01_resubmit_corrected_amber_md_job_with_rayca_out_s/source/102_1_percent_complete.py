
import math

# ── 1. Percent complete ────────────────────────────────────────────────────────
steps_done   = 120000
steps_total  = 250000
pct_complete = steps_done / steps_total * 100
print(f"Percent complete: {steps_done}/{steps_total} = {pct_complete:.1f}%")

# ── 2. Temperature mean ± SD (3 frames) ────────────────────────────────────────
temps_2dp = [300.02, 299.08, 299.89]   # as stated in audit document (2 d.p.)
temps_1dp = [300.0,  299.1,  299.9]    # rounded to 1 d.p.

def stats(values, label):
    n    = len(values)
    mean = sum(values) / n
    pop_var  = sum((t - mean)**2 for t in values) / n
    samp_var = sum((t - mean)**2 for t in values) / (n - 1)
    print(f"\n  {label}")
    print(f"    mean            = {mean:.4f} K")
    print(f"    population SD   = {math.sqrt(pop_var):.4f} K")
    print(f"    sample SD (n-1) = {math.sqrt(samp_var):.4f} K")

print("\n--- Temperature SD ---")
stats(temps_2dp, "Input: 300.02, 299.08, 299.89 K (2 d.p.)")
stats(temps_1dp, "Input: 300.0,  299.1,  299.9  K (1 d.p.)")
print("\n  Claimed: mean = 299.66 K, SD = 0.49 K")

# ── 3. Pipeline time: 7.5 ns/compound at 4.22 ns/day ──────────────────────────
ns_total  = 7.5
ns_per_day = 4.22
days = ns_total / ns_per_day
hours = days * 24
print(f"\n--- Pipeline time ---")
print(f"  {ns_total} ns / {ns_per_day} ns/day = {days:.5f} days = {hours:.4f} h")
print(f"  Claimed: 42.6 h   Correct: {hours:.1f} h (rounds to {round(hours,1)} h)")

# ── 4. Consistency: ns/day, ms/step, s/ns ──────────────────────────────────────
ns_day       = 4.22
ms_step      = 40.95
dt_fs        = 2.0          # assumed timestep (fs)
steps_per_ns = 1e6 / dt_fs  # = 500,000

s_per_ns_from_ns_day  = 86400 / ns_day
s_per_ns_from_ms_step = (ms_step / 1000) * steps_per_ns

print(f"\n--- s/ns consistency ---")
print(f"  From ns/day  ({ns_day} ns/day):         s/ns = {s_per_ns_from_ns_day:.1f}")
print(f"  From ms/step ({ms_step} ms/step, dt=2fs): s/ns = {s_per_ns_from_ms_step:.1f}")
print(f"  Claimed s/ns = 20068")
print(f"  Discrepancy: {abs(s_per_ns_from_ns_day - 20068):.1f} s/ns ({abs(s_per_ns_from_ns_day - 20068)/20068*100:.2f}%)")

# What ms/step is implied by 20068 s/ns at dt=2fs?
ms_step_from_s_per_ns = (20068 / steps_per_ns) * 1000
print(f"  ms/step implied by 20068 s/ns (dt=2fs): {ms_step_from_s_per_ns:.3f} ms/step")

# ── 5. Remaining NVT walltime ──────────────────────────────────────────────────
steps_remaining = steps_total - steps_done
walltime_s  = steps_remaining * ms_step / 1000
walltime_min = walltime_s / 60
walltime_h   = walltime_min / 60
print(f"\n--- Remaining NVT walltime ---")
print(f"  {steps_remaining} steps × {ms_step} ms/step = {walltime_s:.0f} s = {walltime_min:.1f} min = {walltime_h:.2f} h")
print(f"  Claimed: ~1.5 h   Computed: {walltime_h:.2f} h  (match: {abs(walltime_h-1.5)<0.1})")

# ── 6. 1 compound per 48 h check ──────────────────────────────────────────────
walltime_limit = 48
print(f"\n--- 1 compound per 48 h ---")
print(f"  Pipeline time: {hours:.3f} h  vs  LUMI limit: {walltime_limit} h")
print(f"  Fits in one job: {hours < walltime_limit}  (margin: {walltime_limit - hours:.2f} h)")

# ── 7. Phase document artifact count ──────────────────────────────────────────
artifacts = [
    "analyze.py",
    "analysis_B.tar.gz",
    "jobB_log.txt",
    "mdlogs_B.tar.gz",
    "CPD1_progress.txt",   # duplicate row 5
    "CPD1_progress.txt",   # duplicate row 6
    "slurm-22076621.log",
    "CPD9_progress.txt",   # duplicate row 8
    "CPD9_progress.txt",   # duplicate row 9
    "slurm-22076698.log",
]
print(f"\n--- Artifact table ---")
print(f"  Total rows in table: {len(artifacts)}")
print(f"  Unique filenames:    {len(set(artifacts))}")
print(f"  Claimed count: 10   Unique: {len(set(artifacts))}")
print(f"  CPD12_progress.txt present in table: {'CPD12_progress.txt' in artifacts}")
