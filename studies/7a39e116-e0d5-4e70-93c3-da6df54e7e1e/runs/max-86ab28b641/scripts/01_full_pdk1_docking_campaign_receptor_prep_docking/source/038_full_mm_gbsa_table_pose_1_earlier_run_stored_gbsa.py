
import os

# ── Full MM/GBSA table ──────────────────────────────────────────────────────
# Pose 1 from earlier run (stored in gbsa_results dict above)
# Poses 2-5 from last dispatch — but results_list was already parsed
# Let me retrieve all complete data from the last run's output

# The `gbsa_results` dict from the previous cell should still be in scope
print("gbsa_results keys:", list(gbsa_results.keys()))
for p, r in sorted(gbsa_results.items()):
    print(f"Pose {p}: {r}")
