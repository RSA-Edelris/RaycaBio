# Independent Audit — ARV-471 GPU Prediction: add --no_kernels flag

**Auditor:** Independent reviewer (Claude Sonnet 4.6)
**Date:** 2026-09-11
**Files inspected:** boltz_run.py, slurm-6464953.log, slurm-6465991.log, slurm-6462167.log, audit_fix_no_kernels.md, phase_06_arv471_gpu_prediction_job_submission.md, phase_07_arv471_gpu_prediction_results.md, reports/phase_01_arv_471_gpu_prediction_add_no_kernels_flag.md, boltz_out confidence JSON (GPU model_0), boltz_cpu_out confidence JSON (CPU model_0)

---

## Summary

Two MAJOR findings. No CRITICAL findings. The core scientific outcome (3 GPU poses, confidence scores, ligand binding confidence) is correct. The errors are in a stated delta value (+0.110 vs the correct +0.109) and in the interpretation of what `protein_iptm` directionally represents.

---

## Findings

---

### **[MAJOR] — Δligand_iptm stated as +0.110; correct value from raw JSON is +0.109**

**File:** phase_07_arv471_gpu_prediction_results.md, line 29; also audit_fix_no_kernels.md (not repeated there but source data is the same)

**Claim:** "GPU vs CPU delta for model_0: Δconf +0.029, Δptm +0.033, Δiptm +0.040, Δligand_iptm +0.110"

**Check (computed directly from the JSON files):**

GPU model_0 `ligand_iptm` (boltz_out JSON, key `"ligand_iptm"`): `0.9064819812774658`
CPU model_0 `ligand_iptm` (boltz_cpu_out JSON, key `"ligand_iptm"`): `0.7970460057258606`

```
0.9064819812774658
- 0.7970460057258606
= 0.1094359755516052
```

At three decimal places, 0.1094... → **0.109** (4th decimal is 4; rounds down).

The other three deltas are correct:
- Δconf: 0.47777947783470154 − 0.4483930468559265 = 0.02938643... → **0.029** ✓
- Δptm: 0.4550328850746155 − 0.42173317074775696 = 0.03329971... → **0.033** ✓
- Δiptm: 0.3133130967617035 − 0.2734520137310028 = 0.03986108... → **0.040** ✓

**Root cause of the error:** The document's `phase_07_arv471_gpu_prediction_results.md` verification section claims scores were "read verbatim from each confidence_*.json" (verified: the 4dp table values are correct). However, the stated Δligand_iptm of +0.110 cannot be reproduced by any arithmetic path from the raw JSON:

- Raw subtraction: 0.10943597... → 0.109
- Floating-point subtraction of the 4dp-rounded table values (0.9065 − 0.7970): Python gives 0.10949999... → also 0.109

The only path to 0.110 is treating 0.1095 as an exact decimal and applying round-half-up: `f"{0.1095:.3f}"` in Python evaluates to `"0.110"` because the IEEE 754 representation of the literal `0.1095` is slightly above 0.10950000 (it is 0.10950000000000000011...). This appears to be how the figure was computed — by subtracting text-rounded values and mishandling the rounding of the intermediate 0.1095. Neither path from actual JSON data gives +0.110.

**Correct value: Δligand_iptm = +0.109 (0.1094)**

---

### **[MAJOR] — protein_iptm is equated to ERα→CRBN direction; this identity is not stable**

**File:** phase_07_arv471_gpu_prediction_results.md, lines 44 and 100; also Verification section line 149–151

**Claim:** "ERα → CRBN iptm = 0.160 (= protein_iptm)" and "ligand_iptm identity checked. JSON top-level `ligand_iptm: 0.9065` equals `pair_chains_iptm["2"]["0"]` = 0.9065 — confirming chain 2 = ARV-471 and chain 0 = ERα" (correct) — but by analogy, `protein_iptm` is implicitly tied to the ERα→CRBN direction.

**Check:**

GPU model_0 JSON:
```
"protein_iptm": 0.16041286289691925
"pair_chains_iptm": {
    "0": { "1": 0.16041286289691925 },   ← ERα→CRBN
    "1": { "0": 0.15849392116069794 }    ← CRBN→ERα
}
```
Here protein_iptm exactly equals pair_chains_iptm["0"]["1"] (ERα→CRBN). The document's claim holds numerically.

CPU baseline JSON:
```
"protein_iptm": 0.16132786870002747
"pair_chains_iptm": {
    "0": { "1": 0.1524539440870285  },   ← ERα→CRBN
    "1": { "0": 0.16132786870002747 }    ← CRBN→ERα
}
```
Here protein_iptm exactly equals pair_chains_iptm["1"]["0"] (CRBN→ERα direction), **not** pair_chains_iptm["0"]["1"].

In both cases, protein_iptm equals max(pair_chains_iptm["0"]["1"], pair_chains_iptm["1"]["0"]). For GPU model_0 the maximum happens to be in the ERα→CRBN direction; for CPU it is in the CRBN→ERα direction.

**The document's claim "ERα → CRBN iptm (= protein_iptm)" is only coincidentally true for GPU model_0.** The underlying definition of `protein_iptm` in boltz appears to be the maximum of the two inter-protein directional iptm values, not a fixed ERα→CRBN direction. The verification note in phase_07 correctly identifies the ligand_iptm identity but then implicitly applies the same single-element-equality reasoning to protein_iptm without testing whether it holds across multiple JSON files. It does not hold in the CPU JSON.

**Impact on results:** The numerical confidence values in the table are all correct. The error is in the directional interpretation offered as commentary ("ERα → CRBN iptm = protein_iptm"). This matters for reproducibility: a reader trying to reconstruct protein_iptm from pair_chains_iptm for a different run using the ERα→CRBN index would get the wrong value whenever CRBN→ERα is higher.

---

### **[MAJOR] — Phase document in reports/ contains wrong recycling_steps parameter**

**File:** reports/phase_01_arv_471_gpu_prediction_add_no_kernels_flag.md, line 64

**Content of auto-generated phase report (Parameters block):**
```yaml
recycling_steps: 1
```

**Actual value used in every GPU job** (confirmed from slurm-6464953.log line 126, phase_06 job scripts, and audit_fix_no_kernels.md):
```
--recycling_steps 3
```

The auto-generated phase report also lists the method step status as `"running"` (not `"complete"`) and states "This phase produced no captured result output" — meaning the platform's phase document was generated from an incomplete state snapshot and was never updated to reflect the actual job outcome. The only artifact registered is slurm-6465991.log; the three PDB files and three confidence JSONs are not registered in this document.

**Note on phase document existence (item 1 of the audit brief):** A dedicated phase document for the --no_kernels fix does exist at `reports/phase_01_arv_471_gpu_prediction_add_no_kernels_flag.md`. It is titled "Phase 1: ARV-471 GPU prediction — add --no_kernels flag" and is distinct from phase_06 and phase_07 in the session root. However, it is a thin auto-generated stub (94 lines) with the parameter error above and no results section. The substantive write-up of the fix lives in `audit_fix_no_kernels.md` and Job 6 of `phase_06_arv471_gpu_prediction_job_submission.md`. The audit brief's premise that no dedicated phase document exists is therefore partly wrong — the file exists but is incomplete.

---

## Verified Correct

**[VERIFIED CORRECT] — `--no_kernels` flag description matches installed boltz==2.2.1**

`slurm-6462167.log` lines 153–154 show the actual `boltz predict --help` output from the installed venv:
```
  --no_kernels                    Whether to disable the kernels. Default
                                  False
```
`audit_fix_no_kernels.md` quotes this as `"--no_kernels  Whether to disable the kernels. Default False"`. The description is accurate. The flag is a Click boolean option (no argument required; presence sets it to True), consistent with how it appears in job 6465991's command (`--no_kernels` appended without a value).

---

**[VERIFIED CORRECT] — pLDDT token count arithmetic and slice assignments**

phase_07 claims: 258 (ERα) + 469 (CRBN) + 54 (ARV-471) = 781 total.
Slices: ERα = [0:258], CRBN = [258:727], ligand = [727:781].

Arithmetic:
- 258 + 469 = 727 ✓
- 727 + 54 = 781 ✓
- [0:258] = 258 tokens ✓
- [258:727] = 469 tokens ✓
- [727:781] = 54 tokens ✓

All slice boundary arithmetic is correct.

---

**[VERIFIED CORRECT] — All nine pair_chains_iptm table values match GPU model_0 JSON**

phase_07 table (rows = "from" chain, cols = "to" chain):

| | ERα (0) | CRBN (1) | ARV-471 (2) |
|---|---|---|---|
| ERα (0) | 0.908 | 0.160 | 0.637 |
| CRBN (1) | 0.159 | 0.302 | 0.136 |
| ARV-471 (2) | 0.906 | 0.231 | 0.826 |

Verified against GPU JSON pair_chains_iptm (all comparisons to 3dp):
- [0][0] = 0.9083959... → 0.908 ✓
- [0][1] = 0.1604128... → 0.160 ✓
- [0][2] = 0.6372441... → 0.637 ✓
- [1][0] = 0.1584939... → 0.159 ✓
- [1][1] = 0.3015887... → 0.302 ✓
- [1][2] = 0.1362124... → 0.136 ✓
- [2][0] = 0.9064819... → 0.906 ✓
- [2][1] = 0.2305624... → 0.231 ✓
- [2][2] = 0.8261362... → 0.826 ✓

---

**[VERIFIED CORRECT] — ligand_iptm = pair_chains_iptm["2"]["0"] identity**

GPU JSON top-level `"ligand_iptm": 0.9064819812774658`.
GPU JSON `pair_chains_iptm["2"]["0"]`: 0.9064819812774658.
Values are identical to full float precision. The document's claim "ARV-471 → ERα iptm = 0.906 (= ligand_iptm)" is correct.

---

**[VERIFIED CORRECT] — All four confidence score table values (GPU model_0) match JSON**

- confidence_score: 0.47777947783470154 → 0.4778 ✓
- ptm: 0.4550328850746155 → 0.4550 ✓
- iptm: 0.3133130967617035 → 0.3133 ✓
- ligand_iptm: 0.9064819812774658 → 0.9065 ✓
- protein_iptm: 0.16041286289691925 → 0.1604 ✓

---

**[VERIFIED CORRECT] — All four CPU baseline table values match JSON**

- confidence_score: 0.4483930468559265 → 0.4484 ✓
- ptm: 0.42173317074775696 → 0.4217 ✓
- iptm: 0.2734520137310028 → 0.2735 ✓
- ligand_iptm: 0.7970460057258606 → 0.7970 ✓

---

**[VERIFIED CORRECT] — Three deltas (Δconf, Δptm, Δiptm) are correct**

From raw JSON values:
- Δconf: 0.47777947... − 0.44839304... = 0.02938643... → **+0.029** (stated: +0.029) ✓
- Δptm: 0.45503288... − 0.42173317... = 0.03329971... → **+0.033** (stated: +0.033) ✓
- Δiptm: 0.31331309... − 0.27345201... = 0.03986108... → **+0.040** (stated: +0.040) ✓

---

**[VERIFIED CORRECT] — boltz_run.py has no bare except or silent failure in prediction path**

Searched boltz_run.py (64 lines) exhaustively. No `except` clause appears anywhere in the file. The `_NoOp` class absorbs tensorboard calls silently, but all of these occur in the logging/instrumentation layer, not in the boltz prediction forward pass. The `hparams` lambda `(lambda hparams_dict, metrics_dict: ({}, {}, {}))` returns an empty 3-tuple as a stub; this does not silence any prediction error. The actual `cli()` call on line 63 runs unguarded, so any boltz prediction failure propagates as an unhandled exception and surfaces in the Slurm log with a non-zero exit code.

---

**[VERIFIED CORRECT] — Job 6465991 completed and job 6464953 failed with the stated error**

slurm-6464953.log line 122: `ModuleNotFoundError: No module named 'cuequivariance_torch'` — confirmed.
slurm-6464953.log line 125: `RAYCA: the job stopped at line 33 with exit 1` — confirmed.
slurm-6465991.log line 21: `Predicting DataLoader 0: 100%|██████████| 1/1 [00:35<00:00, 0.03it/s]Number of failed examples: 0` — confirmed. No cuequivariance error in the succeeding log.

---

**[VERIFIED CORRECT] — No stale indexing errors in chain mapping or model numbering**

Chain 0/1/2 (JSON) → A/B/C (PDB) → ERα/CRBN/ARV-471 is applied consistently throughout both phase_06 and phase_07. "model_0" is consistently called "model_0" or "first model"; no off-by-one slips found. The pair_chains_iptm row/column orientation (rows = "from", cols = "to") is applied consistently: pair_chains_iptm["2"]["0"] = ARV-471→ERα direction, which matches the ligand_iptm value, as verified above.

---

**[VERIFIED CORRECT] — 35 s runtime claim is appropriately hedged**

audit_fix_no_kernels.md states: "The 35-second wall time ... *suggests* the fallback is fast enough for practical use at this complex size." The word "suggests" is present; the hedging condition "at this complex size" is present. The phase_07 document reports it as a measured fact ("Runtime: 35 seconds on NVIDIA GH200 120 GB") without generalising to a universal claim. No rule is stated from a single data point.

---

## Findings Summary

| # | Severity | Finding |
|---|---|---|
| 1 | MAJOR | Δligand_iptm stated as +0.110; raw JSON gives +0.109 (off by 0.001 in the final decimal) |
| 2 | MAJOR | protein_iptm equated to ERα→CRBN direction; the identity flips to CRBN→ERα in the CPU JSON; the correct definition is max(protein-protein pair iptm values) |
| 3 | MAJOR | Auto-generated phase report (reports/phase_01_...) records recycling_steps: 1; actual jobs used recycling_steps: 3; status frozen as "running"; no output results registered |
| — | VERIFIED | --no_kernels flag description matches installed boltz 2.2.1 help output |
| — | VERIFIED | pLDDT token arithmetic and slice boundaries are correct |
| — | VERIFIED | All nine pair_chains_iptm table values match GPU JSON to 3dp |
| — | VERIFIED | ligand_iptm = pair_chains_iptm["2"]["0"] identity holds to full float precision |
| — | VERIFIED | GPU model_0 and CPU baseline table values match raw JSON |
| — | VERIFIED | Δconf, Δptm, Δiptm are all correct at 3dp |
| — | VERIFIED | boltz_run.py has no bare except or silent failure in prediction path |
| — | VERIFIED | Slurm logs confirm job 6464953 failed with stated error and job 6465991 succeeded |
| — | VERIFIED | Chain mapping, model numbering, and pair_chains_iptm orientation are consistent |
| — | VERIFIED | 35 s runtime claim is not stated as a generalised rule |
