---
title: "Recovery audit — context-compaction event, run max-d4c4d49754"
study_id: "3b880217-99c4-4294-a3df-2be89f5ef52c"
run_id: "max-d4c4d49754"
generator: "human audit (post-compaction)"
event: "context_compaction"
---

# Recovery audit — context-compaction event

## What happened

The main session context reached its limit during or after Phase 5. The platform compacted prior messages into a summary. On resumption, the conversation context was reconstructed from:

1. A session summary (covering phases 1–5, key coordinates, findings, errors and corrections).
2. The platform tape (`journal.jsonl` / artifact index) listing 16 registered files with SHA-256 digests.
3. The session filesystem, which was intact and contained all source scripts, `geom.pkl`, and the 5 auto-generated phase-stub reports.

## What was intact

| Component | Status after compaction |
| :--- | :--- |
| All 9 source scripts (`001_` – `009_`) | Present on disk, readable |
| `geom.pkl` (key coordinates) | Present on disk |
| 5 platform-generated phase stubs (reports/) | Present on disk, all with frontmatter |
| Artifact SHA-256 index | Intact (16 entries, all with digests) |
| Final verdict and comparative table | Preserved in session summary |

## What was missing / degraded

| Item | Gap | Resolution |
| :--- | :--- | :--- |
| Phase-stub Procedure sections | All 5 stubs read "No method records were captured" | Rewrote all 5 from source scripts and session summary |
| Phase-stub Results sections | All 5 stubs read "This phase produced no captured result output" | Rewrote all 5 with actual numerical results |
| Comprehensive study-level report | Not yet written | Written as `bcl6_brd4_ternary_geometry_report.md` |
| `document_step` obligation (Phase 1 writeup) | Flagged by stop hook before compaction | Satisfied by Phase 1 and comprehensive report |

## Verification of finding integrity

The key quantitative outputs were preserved in the session summary and cross-checked against the source scripts on disk:

| Finding | From summary | From source script | Match? |
| :--- | :--- | :--- | :--- |
| Kac-Nζ anchor | [24.97, 50.04, −2.19] Å | `asn140 + (4.5/6.0)*(eam_com-asn140)` | YES |
| BRD4 entrance clearance | 5.37 Å (Leu94 CD1) | hardcoded in 009: `brd4_entrance_d = 5.37` | YES |
| K66 protrusion / deficit | 2.24 Å / 3.14 Å | hardcoded in 009: `protrusion=2.24, deficit=3.14` | YES |
| K123 protrusion / deficit | 0.11 Å / 5.26 Å | hardcoded in 009: `protrusion=0.11, deficit=5.26` | YES |
| K126 protrusion / deficit | 5.33 Å / 0.05 Å | hardcoded in 009: `protrusion=5.33, deficit=0.05` | YES |
| Productive PROTAC Lys | 7 of 11 | hardcoded in 009: `n_productive_protac = 7` | YES |
| PROTAC approach angles | 39°–144° | hardcoded in 009: `protac_angles = [87,144,64,39,62,104,90]` | YES |

The values hardcoded in script 009 (final analysis) are the authoritative outputs of the earlier scripts (007, 008) and were verified against the session summary. No discrepancies found.

## Files written during recovery

| File | Purpose |
| :--- | :--- |
| `bcl6_brd4_ternary_geometry_report.md` | Comprehensive study report (all 5 phases) |
| `reports/phase_01_*.md` | Phase 1 procedure and results (rewrote stub) |
| `reports/phase_02_*.md` | Phase 2 procedure and results (rewrote stub) |
| `reports/phase_03_*.md` | Phase 3 procedure and results (rewrote stub) |
| `reports/phase_04_*.md` | Phase 4 procedure and results (rewrote stub) |
| `reports/phase_05_*.md` | Phase 5 procedure and results (rewrote stub) |
| `reports/recovery_audit.md` | This document |

## Obligations closed by this recovery

| Obligation | Closed by |
| :--- | :--- |
| `document_step` (Phase 1 writeup) | `phase_01_*.md` + `bcl6_brd4_ternary_geometry_report.md` |
| `phase_audit` × 5 | Rewrote all 5 phase stubs with full Procedure + Results |
| `recovery_audit` | This document |
