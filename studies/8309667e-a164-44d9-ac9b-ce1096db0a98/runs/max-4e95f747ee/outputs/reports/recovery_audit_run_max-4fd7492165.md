## Context

This audit covers run `max-4fd7492165`, which resumed from a compacted context. The session carried an in-progress task to revise the synthetic programme cost for MCUF651, A317, and 7977 to incorporate a two-run protocol: one small 0.1 mmol scouting run before each preparative step.

## What was open at session start

Open obligations reported by the stop hook: `document_step`, `recovery_audit`.

The prior session (from the compaction summary) had:
- Created Task #1: "Revise programme cost for 2 runs per step (assay + preparative)" — status `in_progress`
- Not yet run the actual Python calculations

## What this session did

1. **Ran cost calculations** (files 020–021): computed per-step assay reagent costs at 0.1 mmol scale and assay labour (0.35 cd/step × €866/cd = €303/step) for all 12 reaction events (2 for MCUF651, 5 for A317, 5 for 7977).

2. **Updated the main deliverable** `synthetic_programme_100mg_MCUF651_A317_7977.md` with revised totals, per-compound schedules (extended by ~1 day each), and an explanation of the two-run protocol.

3. **Updated the phase report** `reports/phase_01_deliver_synthetic_programme_cost_and_timeline_fo.md` with the revised summary table and elapsed-time table.

## Revised totals

| Compound | Single-run total | Two-run total | Addition | New cd |
| :--- | ---: | ---: | ---: | ---: |
| MCUF651 | €1,143 | **€1,754** | €611 | 1.95 |
| A317 | €2,352 | **€3,875** | €1,523 | 4.25 |
| 7977 | €2,315 | **€3,835** | €1,520 | 4.25 |
| All three | €5,810 | **€9,464** | €3,654 | 10.45 |

Range: **€7,570 – €12,780**

The €3,654 addition is entirely labour (assay reagents = €18 total). Labour fraction rises from 93% to 95%.

## Numerical integrity

- `ac()` function redefined in each `run_python` cell (platform drops user functions between calls; data persists).
- Results consistent with the approximate estimates carried in the compaction summary (€9,466 estimated vs €9,464 calculated — within rounding).
- No purification formula error introduced (flat EST €20–25/column, unchanged from prior session's correction).

## Files produced this session

| File | Kind | Purpose |
| :--- | :--- | :--- |
| `020_two_run_adjustment_*.py` | source | First attempt (KeyError on DIPEA — aborted) |
| `021_sum.py` | source | Final calculation; clean output |
| `synthetic_programme_100mg_MCUF651_A317_7977.md` | deliverable | Updated with two-run costs and schedules |
| `reports/phase_01_deliver_synthetic_programme_cost_and_timeline_fo.md` | phase report | Summary table and elapsed-time table revised |
