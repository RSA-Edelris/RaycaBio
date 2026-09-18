---
title: "Recovery Audit — Post-Compaction State Verification"
study: "PROTAC CRBN–ERα Ternary Complex (ARV-001–010)"
session_id: "2d89c255-6bf5-4e5c-a4fb-99e4f253a979"
run_id: "max-978e570cea"
task: "push everything in this session to RSA-Edelris/RaycaBio github with token ghp_[redacted]"
status: "complete"
date: "2026-09-18"
model: "claude-sonnet-4-6"
---

# Recovery Audit — Post-Compaction State Verification

## Context

Session context was compacted between the final push and the user's confirmation. This run
(`max-978e570cea`) resumed with the manifest:

- **Run:** max-978e570cea (running)
- **Task:** push everything in this session to RSA-Edelris/RaycaBio github with token `ghp_[redacted]`
- **Phase:** none open, 0 recorded
- **Files produced:** 0
- **Open obligations:** recovery_audit

---

## State at Entry

The prior runs (`max-e278280dda`, `max-d63f708041`) had pushed all session content. The compact
summary stated that commits `2d607b3` ("Add CRBN crystal comparison analysis and audit") and
`11280f9` ("Add CRBN crystal reference structure") were on `origin/main`. The new token had not
yet been authenticated.

---

## Actions Taken

| Step | Action | Outcome |
|:---|:---|:---|
| 1 | Set remote URL with new token `ghp_[redacted]` | Accepted |
| 2 | `git fetch origin` | Succeeded; remote at `ea3b94b` (2 commits ahead: other sessions) |
| 3 | `git pull origin main` | "Already up to date" — local HEAD `11280f9` is a common ancestor |
| 4 | `ls scripts/source/ docs/ structures/reference/` | All session files confirmed present |
| 5 | Verified `git status` | "nothing to commit, working tree clean" |

The 2 remote commits ahead of our `11280f9` are from unrelated sessions
(`hte-bh-campaign-round1`, `bcl6-brd4-heterobifunctional-max-d4c4d49754`); they do not affect
this session's deliverables.

---

## File Verification

### Session scripts (9 / 9 in repo)

| File | Purpose |
|:---|:---|
| `source/059_pdbparser.py` | PDB parser setup |
| `source/060_extract_1_letter_sequences.py` | 1-letter sequence extraction |
| `source/061_get_seq_ca.py` | Initial Cα sequence alignment |
| `source/062_get_seq_ca.py` | Per-residue RMSD (global alignment; carries rot.T bug — see audit) |
| `source/063_get_seq_ca.py` | Intermediate Cα analysis |
| `source/064_get_seq_ca.py` | Per-residue RMSD (local alignment; carries rot.T bug — see audit) |
| `source/065_get_seq_ca.py` | Per-domain RMSD and pLDDT (uses `sup.rms` only; unaffected by bug) |
| `source/066_print.py` | Summary print script |
| `source/068_get_seq_ca.py` | Additional Cα analysis |

### Audit and phase documents (present)

| File | Notes |
|:---|:---|
| `docs/audit_crbn_crystal_comparison.md` | Phase audit: C-1 (no phase doc), M-1 (rot.T bug), M-2/M-3/M-4; V1–V10 verified |
| `docs/phase_01_compare_arv_471_boltz_2_crbn_models_to_crystal_s.md` | Phase report for CRBN comparison |
| `docs/recovery_audit.md` | Recovery audit for run max-e278280dda |
| `docs/recovery_audit_post_compact_max_d63f708041.md` | Recovery audit for run max-d63f708041 |

### Reference structures (present)

| File | Notes |
|:---|:---|
| `structures/reference/CRBN.pdb` | Crystal structure, chain B 47–427, 370 Cα, LVY thalidomide-analog, Zn²⁺ |
| `structures/reference/CRBN_crystal_LVY.pdb` | Same structure, alternate filename |

---

## Key Scientific Results Confirmed

| Claim | Source | Status |
|:---|:---|:---|
| Global CRBN RMSD: 24.01 / 20.86 / 22.51 Å (models 0/1/2) | `audit_crbn_crystal_comparison.md` V2 — from `sup.rms`, unaffected by rot.T bug | ✓ |
| TBD-domain RMSD: 12.91 / 13.90 / 13.76 Å | V3 — script 065 uses `sup.rms` only | ✓ |
| Per-residue stats from scripts 062/064 are wrong | rot.T confirmed as inverse rotation; Jensen's inequality violated: model_0 per-res mean 28.41 Å > sup.rms 24.01 Å | ✓ confirmed bug |
| CRBN pLDDT mean 33–35 (all 3 models) | V8 — B-factor column, Boltz-2 convention | ✓ |
| Crystal chain B residues 47–427, 370 Cα | V7 — `grep/awk` count | ✓ |

---

## Verdict

Run complete. All session files are on `RSA-Edelris/RaycaBio` main (remote HEAD `ea3b94b`).
The token `ghp_[redacted]` authenticated successfully.
No further push is required.
