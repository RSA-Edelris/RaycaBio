# Audit Report: Probe 2 — fix pytorch_lightning missing dep in boltzgen container

**Auditor:** Claude Sonnet 4.6 (independent)
**Date:** 2026-09-11
**Log audited:** `slurm-6460283.log`
**Phase report reviewed:** `reports/phase_01_probe_2_fix_pytorch_lightning_missing_dep_in_bol.md`
**Cross-referenced logs:** `slurm-6460149.log`, `slurm-6461898.log`, `slurm-6462018.log`, `slurm-6462059.log`, `slurm-6462118.log`, `slurm-6462167.log`

---

## Summary of What the Log Actually Shows

`slurm-6460283.log` (32 lines) records a job that:
1. Acquired a GPU node (NVIDIA GH200 120GB).
2. Created a fresh virtual environment at `/scratch/u6sp/hpcuser.u6sp/boltz_predict_venv/`.
3. Installed `boltz==2.2.1 --no-deps` (confirmed: `boltz 2.2.1 cuda True`).
4. Ran `boltz predict --help`.
5. Exited with code 1 on `ModuleNotFoundError: No module named 'pytorch_lightning'`.

The Rayca harness captured: `RAYCA: the job stopped at line 38 with exit 1`.

No fix was applied. The phase only confirmed that the dependency was missing.

---

## CRITICAL Findings

### C1. Phase report attributes the wrong job log as its output artifact

The phase report (`phase_01_probe_2_...md`) lists `slurm-6462167.log` (14.0 KB) as its sole output artifact. That file is the log from Probe 6 — the final bulk installation run that actually succeeded in making `boltz predict --help` work. The correct artifact for Probe 2 is `slurm-6460283.log` (3.1 KB), which is the log that actually belongs to this phase. The SHA-256 digest `315c97f0a382...` recorded in the report is for the wrong file.

**Impact:** The phase report cannot be reconciled with the work it purports to describe. Any downstream reference to the artifact is tracing the wrong provenance.

### C2. Phase report Methods section describes a completely unrelated procedure

The Methods section of the phase report documents a Boltz-2 PROTAC ternary complex structure prediction for ARV-471 / ERalpha / CRBN (258 + 469 amino acids, 3 diffusion samples, seed 42, no MSA). This procedure was not performed in Probe 2. `slurm-6460283.log` contains no structure prediction. The Methods block appears to be boilerplate copied from a different study phase (the main prediction goal) and was never replaced with an accurate description of the dependency-probe work.

**Impact:** The report's Methods section is factually false for the phase it is supposed to document.

### C3. Job exited with code 1 but the phase report claims success

The log contains the explicit harness message `RAYCA: the job stopped at line 38 with exit 1`. The phase report records `status: complete` and, in its Verification section, states `0 of which reported a failure`. A non-zero exit code is a job failure. Marking it complete with zero failures silently converts a documented error into a reported success.

**Impact:** Any system that consumes the phase report to decide whether the probe passed will draw the wrong conclusion.

---

## MAJOR Findings

### M1. No phase document existed at the time of execution (finding required by audit spec)

All five files in the `reports/` directory have a filesystem timestamp of `Sep 11 13:22`. The slurm logs for Probes 2 through 6 have earlier timestamps (`slurm-6460283.log` predates 13:22). The reports were generated retroactively in a single batch after Probe 6 completed. No document existed during the probe's execution or immediately after it failed.

**Impact:** There was no contemporaneous record of the phase's intent, method, or outcome. The retroactively generated report also contains the content errors described in C1 and C2.

### M2. Probe title names the wrong package environment

The probe is titled "fix pytorch_lightning missing dep in **boltzgen container**." The work in `slurm-6460283.log` was performed by installing `boltz` (the structure-prediction tool) into a fresh venv at `/scratch/u6sp/hpcuser.u6sp/boltz_predict_venv/`. The boltzgen container (`/opt/boltzgen/venv/`) is a separate software stack used for binder design and was functional, as confirmed in `slurm-6460149.log` (boltzgen's own top-level help and `run` subcommand printed successfully). The `pytorch_lightning` issue was in the `boltz` predict venv, not in the boltzgen container.

**Impact:** `boltz` and `boltzgen` are distinct packages with distinct environments. The mislabeling obscures which environment was being diagnosed and may mislead any engineer revisiting the probe.

### M3. Probe title claims "fix" but only diagnosis was performed

The name states "fix pytorch_lightning missing dep." `slurm-6460283.log` shows that `boltz==2.2.1` was installed `--no-deps` and then `boltz predict --help` was run to expose the missing module. No installation of `pytorch_lightning` or any other missing dependency was attempted in this job. The actual installation did not occur until `slurm-6461898.log` (Probe 3). Naming the probe "fix" when only a diagnosis was performed misrepresents the scope of the work.

**Impact:** A reader relying on the phase name to understand the probe's completion state will believe the dependency was resolved when it was not.

### M4. Probe 3 installed wrong package versions — corrected only in Probe 6

`slurm-6461898.log` (Probe 3) manually installed: `mashumaro-3.22`, `gemmi-0.7.5`, `biopython-1.88`, `modelcif-1.8`, `hydra-core-1.3.6`. The pip output in `slurm-6462167.log` (Probe 6) records the boltz==2.2.1 pinned requirements as: `mashumaro==3.14`, `gemmi==0.6.5` (implied by the installed gemmi-0.6.5 after uninstall of 0.7.5), `biopython==1.84`, `modelcif==1.2`, `hydra-core==1.3.2`. Probe 6 explicitly uninstalled and replaced those four packages before the final successful `boltz predict --help`. The mismatches in Probe 3 caused downstream failures not attributable to additional missing modules.

This is a rule-from-single-data-point risk: after each probe added one dependency and re-ran the test, the conclusion was always "add only this one dep." The actual requirement was a full pinned dependency set from boltz==2.2.1's metadata, which was only resolved in Probe 6 by running pip with deps allowed.

**Impact:** Probes 3–5 were partly invalidated by incorrect version choices made in Probe 3. The cascade of failures was in part version-mismatch-driven, not only sequential-import-driven.

### M5. Platform / architecture mismatch between report and actual compute node

The phase report records `Platform: Linux-6.17.0-1022-gcp-x86_64-with-glibc2.39`. The DEPRECATION warnings in every slurm log from the boltzgen container reference `nvfuser-0.2.26a0+c5e1555-py3.12-linux-aarch64.egg`, confirming the compute nodes are aarch64 (Arm64 Grace Hopper). The phase report's platform string is from the Rayca management host (a GCP x86_64 instance), not the machine where the probe ran.

**Impact:** The environment table is misleading. A reproducibility attempt using the reported platform would target the wrong architecture.

### M6. Phase numbering offset creates a gap — Probe 1 has no phase report

Phase reports are numbered phase_01 through phase_05 and correspond to Probes 2 through 6. Probe 1 (`slurm-6460149.log`, the initial boltzgen capability check) has no corresponding phase report. If the intent is 1-based phase numbering aligned to probe numbers, phase_01 should correspond to Probe 1. If the intent is that Probe 1 was an unnumbered setup step, the offset should be documented. As written, the numbering implies Phase 1 = Probe 1, but the file name reads `phase_01_probe_2_...`, making clear a mismatch exists and is unexplained.

**Impact:** A reviewer counting phase reports and probes will see six probes and five phase reports with unexplained offset.

---

## Verification

### N1. No bare except / silent-success pattern in the probe script itself

The probe script used explicit exit codes captured by the Rayca harness (`exit 1` was recorded and surfaced). No `|| true` or equivalent suppression was present in the failing step. The harness correctly attributed and reported the failure at the script level.

### N2. No reversed positional arguments in the probe

`boltz predict --help` is an introspection command with no positional data arguments. No argument order issue is present in the probe log.

---

## Verified Correct

### V1. The specific error was correctly identified

`slurm-6460283.log` line 27: `ModuleNotFoundError: No module named 'pytorch_lightning'` at `boltz/main.py` line 16 (`from pytorch_lightning import Trainer, seed_everything`). This is a genuine missing dependency in the boltz==2.2.1 package when installed without deps. The traceback is complete and accurate.

### V2. CUDA availability confirmed before the test

Line 18 of `slurm-6460283.log`: `boltz 2.2.1 cuda True`. CUDA was verified present before the import test ran, ruling out a GPU/driver issue as the cause of the failure.

### V3. boltz version matches the stated probe target

The probe title targets boltz (the structure predictor). `boltz 2.2.1` is what was installed and tested, consistent with the stated version in the broader study context.

### V4. pytorch_lightning import failure is the first import failure in the chain

From `slurm-6461898.log` (Probe 3), after installing pytorch_lightning, the next failure was `ModuleNotFoundError: No module named 'torchmetrics'` — a dependency of pytorch_lightning. This confirms that pytorch_lightning itself was reached only after being installed, and the cascade of import errors observed in Probe 3 onwards traces back correctly to the --no-deps installation strategy. Probe 2's single error was genuinely the first import blocker.

### V5. boltz predict --help eventually succeeded after full dependency resolution

`slurm-6462167.log` ends with a complete `boltz predict --help` output (Options table fully printed), confirming that the dependency chain was eventually fully resolved through Probes 3–6. The direction of work was correct, even if the strategy (one-at-a-time manual installs) was inefficient and introduced version mismatches corrected only in the final probe.

---

## Summary Table

| ID | Severity | Finding |
|---|---|---|
| C1 | CRITICAL | Phase report cites `slurm-6462167.log` (Probe 6) as Probe 2's output artifact; correct file is `slurm-6460283.log` |
| C2 | CRITICAL | Methods section describes PROTAC Boltz-2 structure prediction — entirely wrong procedure for this phase |
| C3 | CRITICAL | Job exited with code 1; report records `status: complete` and `0 failures` |
| M1 | MAJOR | No phase document existed during or immediately after probe execution; all reports retroactively generated at Sep 11 13:22 |
| M2 | MAJOR | "boltzgen container" is the wrong environment; issue was in the `boltz` predict venv |
| M3 | MAJOR | Probe named "fix" but only performed diagnosis; no fix was applied until Probe 3 |
| M4 | MAJOR | Probe 3 installed wrong pinned versions (mashumaro 3.22 vs 3.14, hydra-core 1.3.6 vs 1.3.2, gemmi 0.7.5 vs 0.6.5, modelcif 1.8 vs 1.2), requiring re-correction in Probe 6 |
| M5 | MAJOR | Phase report records x86_64 platform; compute nodes are aarch64 (GH200 Grace Hopper) |
| M6 | MAJOR | Phase numbering 1–5 covers Probes 2–6; Probe 1 has no phase report and the offset is undocumented |
| V1 | VERIFIED CORRECT | pytorch_lightning identified as the first import blocker in boltz==2.2.1 installed --no-deps |
| V2 | VERIFIED CORRECT | CUDA verified present before test; GPU driver not the issue |
| V3 | VERIFIED CORRECT | boltz 2.2.1 was the version installed and tested |
| V4 | VERIFIED CORRECT | pytorch_lightning is genuinely the first import in the chain that fails |
| V5 | VERIFIED CORRECT | Full dependency resolution eventually succeeded in Probe 6 |
