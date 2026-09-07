
import os

# ---- Phase 1 audit: Protein preparation -----------------------------------
audit({
    "phase": "Phase 1 — Protein preparation (4CI2)",
    "goal": "Download 4CI2, repair with PDBFixer at pH 7.4, identify pocket, trim receptor.",
    "checks": [
        {"check": "Raw PDB downloaded",
         "result": "pass",
         "evidence": f"PB-20260903-4CI2_raw.pdb exists ({os.path.getsize('PB-20260903-4CI2_raw.pdb'):,} bytes)"},
        {"check": "PDBFixer receptor produced",
         "result": "pass",
         "evidence": f"PB-20260903-4CI2_receptor.pdb exists ({os.path.getsize('PB-20260903-4CI2_receptor.pdb'):,} bytes)"},
        {"check": "Trimmed pocket receptor produced (noH, for docking)",
         "result": "pass",
         "evidence": f"PB-20260903-4CI2_receptor_trimmed_noH.pdb exists ({os.path.getsize('PB-20260903-4CI2_receptor_trimmed_noH.pdb'):,} bytes)"},
        {"check": "Trimmed receptor capped for MM-GBSA",
         "result": "pass",
         "evidence": f"PB-20260903-4CI2_receptor_trimmed_capped.pdb exists ({os.path.getsize('PB-20260903-4CI2_receptor_trimmed_capped.pdb'):,} bytes)"},
        {"check": "Pocket centroid identified from crystal LVY",
         "result": "pass",
         "evidence": "x=84.80, y=154.94, z=13.24 Å; tri-Trp pocket confirmed"},
        {"check": "No missing internal loops",
         "result": "pass",
         "evidence": "REMARK 465 analysis confirmed missing residues are terminal His-tag only"},
    ],
    "issues": [
        "fpocket unavailable; pocket defined from crystal ligand position instead",
        "Histidine protonation states not verified with explicit PROPKA calculation",
    ],
    "verdict": "pass"
})
print("Phase 1 audit submitted")
