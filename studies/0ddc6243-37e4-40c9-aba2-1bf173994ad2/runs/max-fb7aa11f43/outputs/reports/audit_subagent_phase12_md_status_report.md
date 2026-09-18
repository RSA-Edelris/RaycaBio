---
title: "Independent Audit: Phase 12 — Write MD pipeline status report for job 22076601"
study_id: "0ddc6243-37e4-40c9-aba2-1bf173994ad2"
audit_date: "2026-09-15"
auditor: "claude-sonnet-4-6 (independent subagent, no prior knowledge of expected outcomes)"
sources_checked:
  - reports/phase_01_write_md_pipeline_status_report_for_job_22076601.md
  - reports/audit_phase_12_md_status_report_job22076601.md
  - jobB_log.txt
  - CPD1_progress.txt
  - CPD9_progress.txt
  - CPD12_progress.txt
---

# Independent Audit: Phase 12 — Write MD pipeline status report for job 22076601

All arithmetic was recomputed independently before any verdict was assigned.
No file listed in the audit brief was missing.

---

## 1. CRITICAL findings

### C-1 — s/ns value (20068) is inconsistent with the two co-stated performance metrics

**Claim (audit document, CPD4 NVT table):**
> Performance: 4.22 ns/day | Step time: 40.95 ms/step (20068 s/ns)

**Independent calculation:**

| Derivation | Formula | Result |
|---|---|---|
| s/ns from ns/day | 86 400 s ÷ 4.22 ns/day | **20 474 s/ns** |
| s/ns from ms/step (dt = 2 fs) | 40.95 ms/step × 500 000 steps/ns ÷ 1000 | **20 475 s/ns** |
| Stated s/ns | — | **20 068 s/ns** |
| Discrepancy | |20 474 − 20 068| | **406 s/ns (2.0 %)** |

Both independent derivations agree with each other (20 474–20 475 s/ns) and both
contradict the stated 20 068 s/ns. For the stated value to be correct, the ms/step
would have to be 40.14 (not 40.95) or ns/day would have to be 4.31 (not 4.22).
Neither alternative is consistent with the other stated values.

**Verdict: CRITICAL** — one of {ns/day, ms/step, s/ns} is wrong. The self-consistent
pair is (4.22 ns/day, 40.95 ms/step) → 20 474 s/ns. The value 20 068 s/ns should be
treated as a transcription or rounding error in the mdinfo readout.

---

## 2. MAJOR findings

### M-1 — Temperature SD (0.49 K) is not reproducible from the stated 2-decimal-place temperatures

**Claim (audit document and phase report):**
> Temperature mean ± SD: 299.66 ± 0.49 K (computed from 3 frames)

**Three frame values stated in audit document:** 300.02, 299.08, 299.89 K

**Independent calculation:**

| Method | Input precision | Mean (K) | SD (K) |
|---|---|---|---|
| Population SD (÷ n=3) | 2 d.p. (300.02, 299.08, 299.89) | 299.663 | 0.416 |
| Sample SD (÷ n−1=2) | 2 d.p. (300.02, 299.08, 299.89) | 299.663 | 0.509 |
| Sample SD (÷ n−1=2) | 1 d.p. (300.0, 299.1, 299.9) | 299.667 | **0.493 ≈ 0.49** |

The claimed 0.49 K is **only obtainable if the temperatures are rounded to 1 decimal
place before computing the SD**. The audit document states the values to 2 decimal
places, from which the sample SD is 0.51 K and the population SD is 0.42 K.
Neither matches 0.49 K.

The mean of 299.66 K is correct to 2 d.p. for either input precision set.

**Verdict: MAJOR** — the SD (0.49 K) is not reproducible from the values the document
provides. The discrepancy is caused by an undisclosed intermediate rounding step.
Consuming code or analysis that re-derives SD from the stated temperatures will obtain
0.51 K (sample) or 0.42 K (population), not 0.49 K.

---

### M-2 — Pipeline time rounds to 42.7 h, not 42.6 h

**Claim (audit document, Performance bottleneck section):**
> Full 7.5 ns/compound pipeline at 4.22 ns/day = 42.6 h/compound.

**Independent calculation:**
7.5 ns ÷ 4.22 ns/day = 1.7773 days × 24 h/day = **42.654 h**

42.654 rounded to one decimal place = **42.7 h**, not 42.6 h.

The error is 0.054 h (≈3 min) and has no practical consequence for the
"1 compound per 48 h" conclusion, but the stated value is arithmetically wrong.

**Verdict: MAJOR** — incorrect rounding. Should be 42.7 h.

---

### M-3 — Audit pipeline table misrepresents CPD10 and CPD11 mini status

**Claim (audit document pipeline completeness table):**

| System | Mini |
|---|---|
| CPD10 | Done (tleap only, no MD) |
| CPD11 | — |

**Raw evidence (jobB_log.txt, header + body):**

```
RESULTS=[…/out/job-22076607]
…
>>> CPD10 start 20:07:32
  CPD10 mini FAILED (exit 1)
>>> CPD11 start 20:07:32
  CPD11 mini FAILED (exit 1)
```

Both CPD10 and CPD11 had the minimisation stage **attempted and failed** in job 22076607.
The table description "Done (tleap only, no MD)" for CPD10 describes what happened in the
earlier job 22075127, not the mini status. Placing it in the "Mini" column misrepresents
the pipeline state: mini was not skipped, it was attempted and failed.

For CPD11, the "—" entry implies no attempt was made; the raw log contradicts this.

**Verdict: MAJOR** — both entries are misleading. The Mini column for CPD10 and CPD11
should read "FAILED (job 22076607, srun)" to match the raw log.

---

### M-4 — jobB_log.txt verification section cites wrong job number (22076611 vs 22076607)

**Raw evidence:**

Line 3 of jobB_log.txt (RESULTS header):
```
RESULTS=[/scratch/project_462001483/rayca/max-f288f18e91/out/job-22076607]
```

Verification section of the same file:
```
Failure mode is identical to that seen in jobs 22076611, 22076621, 22076698, 22076809
```

The verification text says **22076611** but the job that produced jobB_log.txt is **22076607**
(per the RESULTS path, which is the authoritative identifier). The phase report and audit
document correctly list 22076607 in their job lists, so this error was not propagated into
the final report — but the verification text embedded in the source log is internally
inconsistent.

**Verdict: MAJOR** — the verification section of jobB_log.txt contains a wrong job number.
Any future reader relying on that section alone would record the wrong ID.

---

### M-5 — Performance figure is a single-point measurement generalised to all 9 systems

**Claim (audit document):**
> Performance: 4.22 ns/day … Full 7.5 ns/compound pipeline at 4.22 ns/day = 42.6 h/compound.
> With a 48 h LUMI `small` partition walltime, only 1 compound completes per job submission.

**Basis:** One mdinfo snapshot taken mid-NVT (step 120 000 of 250 000) for CPD4 on
~127 k-atom system at 128 MPI ranks.

The throughput will vary by:
- MD stage (NVT vs NPT vs production have different force-field contexts)
- Compound identity (different ligand / system sizes)
- Node load at sampling time

The "42.6 h/compound" conclusion and the implied minimum job-submission strategy (one
compound per 48 h slot) both rest entirely on this single observation. The audit document
acknowledges the SD caveat for temperature but does not flag the single-point nature of
the performance extrapolation.

**Verdict: MAJOR** — single-point generalisation. The 48 h estimate should be treated
as an order-of-magnitude bound, not a precise pipeline plan.

---

### M-6 — Artifact table inflates file count with duplicate rows; CPD12_progress.txt absent

**Phase document, Table A:**
CPD1_progress.txt appears in rows 5 and 6 (identical hash: 8aba8cc9e8f0).
CPD9_progress.txt appears in rows 8 and 9 (identical hash: 3cf2bdf8f26f).

Table claims 10 files produced; unique filenames = 8.

CPD12_progress.txt is a real source file (verified above) but is not listed in the
artifact table at all, despite being the evidence for CPD12's failure in job 22076809.

**Verdict: MAJOR** — artifact count overstated (10 vs 8 unique); one evidentiary file
(CPD12_progress.txt) is unregistered in the artifact table.

---

## 3. VERIFIED CORRECT

| # | Claim | Evidence | Verdict |
|---|---|---|---|
| V-1 | 120 000/250 000 = 48.0% complete | 120000 ÷ 250000 = 0.4800 exactly | VERIFIED CORRECT |
| V-2 | Temperature mean = 299.66 K | (300.02 + 299.08 + 299.89)/3 = 299.663 K → rounds to 299.66 K | VERIFIED CORRECT |
| V-3 | Remaining NVT ~1.5 h | 130 000 steps × 40.95 ms/step = 5324 s = 88.7 min = 1.48 h | VERIFIED CORRECT |
| V-4 | "1 compound per 48 h" conclusion | 42.654 h < 48 h LUMI limit (margin 5.3 h) | VERIFIED CORRECT |
| V-5 | CPD1 FAILED in job 22076621 | CPD1_progress.txt: mini started 20:09:38, failed 20:09:39 | VERIFIED CORRECT |
| V-6 | CPD9 FAILED in job 22076698 | CPD9_progress.txt: mini started and failed at 20:14:11 | VERIFIED CORRECT |
| V-7 | CPD12 FAILED in job 22076809 | CPD12_progress.txt: mini started and failed at 20:17:21 | VERIFIED CORRECT |
| V-8 | CPD9, CPD10, CPD11, CPD12 all FAILED in job 22076607 | jobB_log.txt body: all four FAILED exit 1 at 20:07:32; RESULTS header confirms job-22076607 | VERIFIED CORRECT |
| V-9 | Phase report job list (22076607, 22076621, 22076698, 22076809) | Matches RESULTS headers and progress files | VERIFIED CORRECT |
| V-10 | 40.95 ms/step is consistent with 4.22 ns/day at dt=2 fs | 40.95 × 500 000/1000 = 20 475 s/ns vs 86400/4.22 = 20 474 s/ns | VERIFIED CORRECT |
| V-11 | Job 22076601 produced no output; workdir cleaned | Both phase report and audit document state this; no contradicting evidence in available files | VERIFIED CORRECT (uncontradicted) |
| V-12 | Root cause: missing systems tarball, not a job failure | Consistent with exit 0, 15 s runtime, and contrast with successful job 22076604 | VERIFIED CORRECT (reasoning is consistent) |
| V-13 | All 4 parallel-job root causes: srun "More processors requested than permitted" | CPD1/CPD9/CPD12 progress files show ≤1 s failures; jobB_log shows all 4 compounds failed simultaneously at 20:07:32 | VERIFIED CORRECT |
| V-14 | Simulation time 240.000 ps at step 120 000 | 120 000 steps × 2 fs/step = 240 000 fs = 240.000 ps | VERIFIED CORRECT |

---

## 4. Summary table

| ID | Severity | Claim | Finding |
|---|---|---|---|
| C-1 | CRITICAL | s/ns = 20068 | Should be ~20 474; inconsistent with both ns/day (4.22) and ms/step (40.95) |
| M-1 | MAJOR | SD = 0.49 K | Only reproducible from 1-d.p. temperatures; from stated 2-d.p. values: sample SD = 0.51 K, population SD = 0.42 K |
| M-2 | MAJOR | Pipeline time = 42.6 h | 7.5/4.22×24 = 42.654 h rounds to 42.7 h |
| M-3 | MAJOR | CPD10 Mini "Done (tleap only)"; CPD11 Mini "—" | Both failed mini in job 22076607 per jobB_log.txt |
| M-4 | MAJOR | jobB_log verification text cites job 22076611 | RESULTS header is authoritative: job is 22076607 |
| M-5 | MAJOR | 4.22 ns/day extrapolated to all 9 systems | Single-point mid-NVT measurement for one compound |
| M-6 | MAJOR | "10 files produced"; CPD12_progress.txt not in table | 8 unique files; CPD12_progress.txt missing from artifact registry |
| V-1…V-14 | VERIFIED | (see table above) | 14 claims checked against raw data and held up |
