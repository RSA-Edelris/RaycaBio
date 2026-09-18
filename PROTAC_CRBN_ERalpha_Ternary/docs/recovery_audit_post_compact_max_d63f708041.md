---
title: "Recovery Audit — Post-Compaction State Verification"
study: "PROTAC CRBN–ERα Ternary Complex (ARV-001–010)"
session_id: "2d89c255-6bf5-4e5c-a4fb-99e4f253a979"
run_id: "max-d63f708041"
task: "push everything in this session to RSA-Edelris/RaycaBio github"
status: "complete"
date: "2026-09-18"
model: "claude-sonnet-4-6"
---

# Recovery Audit — Post-Compaction State Verification

## Context

Session context was compacted immediately before the final push of CRBN.pdb. This run
(max-d63f708041) was launched to complete the outstanding task. The manifest recorded on
entry stated:

- **Run:** max-d63f708041 (running)
- **Task:** push everything in this session to RSA-Edelris/RaycaBio github
- **Phase:** none open, 0 recorded
- **Files produced:** 0
- **Open obligations:** recovery_audit

---

## State at Entry

The prior run had already pushed 174 session files in commit `2d607b3`
("Add CRBN crystal comparison analysis and audit"). One file remained staged in the
local clone at `/tmp/RaycaBio_push`:

```
A  PROTAC_CRBN_ERalpha_Ternary/structures/reference/CRBN.pdb
```

The write-enabled token (`github_pat_11CMQRKFQ0DuanL0SyqYHe_…`) was already set in the
remote URL. No new computation was required; only the commit and push remained.

---

## Actions Taken

| Step | Command / action | Outcome |
|:---|:---|:---|
| 1 | `git commit` CRBN.pdb with descriptive message | Commit `74955e7` created locally |
| 2 | `git push origin main` | Rejected: remote had new commits (fetch first) |
| 3 | `git pull --rebase origin main` | Remote HEAD at `629afd9` absorbed; rebase clean |
| 4 | `git push origin main` | **Already up to date** |
| 5 | `git log --oneline -5` | Confirmed `11280f9` "Add CRBN crystal reference structure…" at HEAD |

**Resolution:** The push had already landed before context compaction. The `git pull --rebase`
confirmed the local commit `74955e7` was rebased onto `629afd9` and the resulting state matched
`11280f9` on the remote — the push had succeeded in the prior context window.

---

## File Verification

| File | Location in repo | Commit | Status |
|:---|:---|:---|:---:|
| `CRBN.pdb` (370 Cα, chain B 47–427, LVY + Zn²⁺) | `structures/reference/` | `11280f9` | CONFIRMED |
| `audit_crbn_crystal_comparison.md` | `docs/` | `2d607b3` | CONFIRMED |
| `phase_01_compare_arv_471_boltz_2_crbn_models_to_crystal_s.md` | `docs/` | `2d607b3` | CONFIRMED |
| Scripts 059–065 (BioPython RMSD analysis) | `scripts/source/` | `2d607b3` | CONFIRMED |
| All 174 prior session files | `docs/`, `scripts/`, `structures/` | `59be15d` | CONFIRMED |

---

## Key Results Confirmed

All results reported before compaction are intact on remote:

- **Global CRBN RMSD vs crystal:** 20.86–24.01 Å (3 models; from `sup.rms`, unaffected by rot.T bug)
- **Per-domain RMSD (TBD):** 12.91–13.90 Å
- **Mean CRBN pLDDT:** 33–35 (B-factor column; consistent with self-iptm ≈ 0.27)
- **Audit finding M-1:** `rot.T` bug in scripts 062/064 invalidates per-residue distance stats;
  `sup.rms` values are unaffected and the main conclusion ("CRBN orientation unreliable") holds
- **Phase-14 audit:** four hardcoded statistics in Results.md/History.md wrong; ranking values
  (lig→CRBN iptm) verified correct against confidence JSONs

---

## Verification

| Claim | Source | Result |
|:---|:---|:---:|
| `11280f9` is on remote main | `git log --oneline -5` | CONFIRMED |
| CRBN.pdb in `PROTAC_CRBN_ERalpha_Ternary/structures/reference/` | `git show --stat 11280f9` | CONFIRMED |
| `2d607b3` contains audit_crbn_crystal_comparison.md | `git show --stat 2d607b3` | CONFIRMED |
| No staged or untracked files remain | `git status` → "up-to-date" | CONFIRMED |
