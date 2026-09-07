---
title: "Recovery Audit — Parallel Docking Workflow Failure"
study_id: "74591a70-5513-45c3-a9c1-10904993bc16"
audit_type: "recovery"
phase_id: "3"
---

# Recovery Audit — Parallel Docking Workflow Failure

This document records the failure of the initial parallel docking workflow attempt,
the detection of the failure, and the confirmed recovery steps. It supplements the
phase 3 audit document.

---

## Failure event

**Workflow ID:** wf_51656335-806

**What was attempted:** 32 gnina agents launched in parallel, one per ligand, each
writing docked poses to `gnina_docked.sdf.gz` in the shared session workspace.

**Failure mode 1 — file collision:** All 32 agents wrote to the same shared workspace
path (`gnina_docked.sdf.gz`). Each agent's output overwrote the previous agent's.
The final pose file in the workspace belonged to whichever agent completed last;
all others were silently lost. This affected all 32 ligands — none had a reliable
pose file at the expected path after the parallel run.

**Failure mode 2 — concurrency exhaustion:** Three agents (for EDEL-CRBN-0002,
EDEL-CRBN-0003, and EDEL-CRBN-0003_ent) produced empty `.jsonl` files, indicating
they were queued but never executed. Cause: the platform concurrency cap
(~10 simultaneous agents) combined with the 32-agent burst; when slower agents held
slots, the queued agents timed out before a slot opened.

---

## Detection

The failure was detected by inspecting the workflow journal files after the run
completed. Three methods used:

1. **File listing:** `ls poses/` showed only a single `gnina_docked.sdf.gz` rather
   than 32 named files — confirmed the collision problem.

2. **Journal inspection:** `.jsonl` transcript files for the 3 missing agents were
   0 bytes (no content = never started).

3. **Score collection:** Attempted to read `docking_scores_all32.json` and found
   only 29 entries instead of 32, confirming the 3 missing agents.

---

## Recovery steps

**Step 1 — Sequential re-docking (all 32):**
All 32 ligands were re-docked sequentially in 4 batches of 8 using `run_aidd_tool`
directly in `run_python`. After each gnina call the output file was immediately
moved:

```python
copy(f"{WORK}/gnina_docked.sdf.gz", f"{WORK}/poses/{name}_poses.sdf.gz")
```

This eliminated the collision — each pose file was saved to its own named path
before the next docking call began.

**Step 2 — Verify 3 missing ligands:**
The 3 previously unstarted ligands (EDEL-CRBN-0002, EDEL-CRBN-0003, EDEL-CRBN-0003_ent)
were included in the sequential re-run and completed successfully.

---

## Confirmation that recovery is complete

| Check | Status |
|-------|--------|
| `poses/` directory contains 32 `.sdf.gz` files | CONFIRMED |
| All 32 files non-zero size | CONFIRMED |
| `docking_scores_all32.json` contains 32 entries | CONFIRMED |
| All 32 entries have non-null Vina affinity | CONFIRMED |
| `gpu_used=True` for all 32 | CONFIRMED |
| num_poses=5 for all 32 | CONFIRMED |
| EDEL-CRBN-0002 docked (was one of the 3 missing) | CONFIRMED, –8.46 kcal/mol |
| EDEL-CRBN-0003 docked (was one of the 3 missing) | CONFIRMED, –7.35 kcal/mol |
| EDEL-CRBN-0003_ent docked (was one of the 3 missing) | CONFIRMED, –8.31 kcal/mol |

All 32 ligands have verified docking results. No data loss from the initial
parallel failure persists in the final analysis.

---

## Root cause and prevention

**Root cause:** gnina always writes to `gnina_docked.sdf.gz` in the shared workspace.
Parallel agents do not have separate workspaces unless explicitly isolated.

**Prevention for future runs:** Either:
1. Use sequential dispatch (as implemented here), or
2. Use `isolation: "worktree"` in the agent call to give each agent its own
   filesystem sandbox (confirmed available in this platform's Agent tool), or
3. Pass a per-ligand `output_file` parameter to gnina (if schema supports it —
   check with `aidd_tool_schema("gnina")` before assuming).

The sequential approach used here adds approximately 20 minutes of wall-clock
time compared to ideal parallel execution, but is reliable and fully verifiable.
