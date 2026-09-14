# Audit Report: Probe 5 — install chembl_structure_pipeline, verify boltz predict --help

**Auditor:** Independent automated review  
**Date:** 2026-09-11  
**Log audited:** `slurm-6462118.log` (28 lines, 2.2 KB)  
**Phase report audited:** `reports/phase_04_probe_5_install_chembl_structure_pipeline_verify.md`  
**Adjacent logs consulted:** `slurm-6462059.log` (Probe 4), `slurm-6462167.log` (Probe 6)

---

## CRITICAL Findings

### CRITICAL-1: boltz predict --help FAILED — claimed as success

The primary verification goal of this probe was to confirm that `boltz predict --help` runs successfully. The log shows it did not:

```
Traceback (most recent call last):
  File ".../boltz_predict_venv/bin/boltz", line 5, in <module>
    from boltz.main import cli
  ...
  File ".../transformers.py", line 3, in <module>
    from fairscale.nn.checkpoint.checkpoint_activations import checkpoint_wrapper
ModuleNotFoundError: No module named 'fairscale'
```

The phase report frontmatter records `status: "complete"` and the Verification section states "1 tool call(s) ran in this phase, 0 of which reported a failure." This is false. The only substantive test in the probe — `boltz predict --help` — raised an unhandled exception and exited with an error. The probe did not achieve its stated goal.

### CRITICAL-2: Wrong log file cited as output artifact

The phase report (phase_04) lists `slurm-6462167.log` as its sole log artifact with a recorded SHA-256 hash. However, `slurm-6462167.log` is the log for Probe 6 (the bulk-install step that runs after this probe). The correct log for Probe 5 is `slurm-6462118.log`. The artifact table therefore names, and hashes, a file from a different phase. Any reproduction or integrity check using the cited hash would be checking the wrong job.

### CRITICAL-3: Procedure section describes a completely unrelated experiment

The Methods / Procedure section of the phase report states:

> "Boltz-2 structure prediction was performed to model the bridging geometry of ARV-471 PROTAC bound to estrogen receptor alpha (ERalpha, chain A, 258 amino acids) and cereblon (CRBN, chain B, 469 amino acids)..."

This describes the downstream structure-prediction run, not a dependency installation probe. The identical text appears verbatim in the reports for Phase 3 (Probe 4) and Phase 5 (Probe 6) as well — none of which performed structure prediction. The procedure section for all three probe phases appears to have been copied from the actual Boltz-2 prediction phase and was never updated to reflect what the probe actually did. A reader cannot reconstruct the methods from this report.

### CRITICAL-4: Wrong version of chembl_structure_pipeline installed

Probe 5 installed `chembl_structure_pipeline-1.2.4`. However, the boltz package in the venv requires `chembl_structure_pipeline==1.2.2` (confirmed by the Probe 6 log, line 16: `from chembl_structure_pipeline==1.2.2->boltz==2.2.1`). The Probe 6 bulk-install step then explicitly uninstalled 1.2.4 and replaced it with 1.2.2 (log line 61: `Successfully uninstalled chembl_structure_pipeline-1.2.4`). The version installed by Probe 5 was incorrect for the boltz venv's dependency tree.

---

## MAJOR Findings

### MAJOR-1: Dependency conflicts suppressed without enumeration

The pip output in `slurm-6462118.log` line 8 reads:

```
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed.
This behaviour is the source of the following dependency conflicts.
```

The phrase "the following dependency conflicts" is never followed by the actual conflict list — the very next line is `Successfully installed chembl_structure_pipeline-1.2.4`. Pip normally prints each conflicting package on its own line between these two statements. The conflicts are either absent from the log (truncated or redirected) or were silently dropped by the job harness. The install completed anyway, which is the default pip behaviour when `--no-deps` is not used. Combined with CRITICAL-4 (wrong version), the suppressed conflicts likely included the version mismatch between what was being installed (1.2.4) and what boltz required (1.2.2).

### MAJOR-2: Systematic phase/probe numbering offset obscures a missing probe

Phases are numbered 1–5; the corresponding probes are numbered 2–6. Phase 1 = Probe 2, Phase 2 = Probe 3, ..., Phase 4 = Probe 5. This means Probe 1 has no phase report in this collection. No report documents what Probe 1 did, whether it succeeded or failed, or what state the environment was in before the probe sequence began. The offset is internally consistent across the five reports, but the gap at Probe 1 is an undocumented dependency for all subsequent probes.

### MAJOR-3: pip install destination ambiguous — system Python vs. venv

The Probe 5 pip output shows `setuptools` satisfied from `/usr/local/lib/python3.12/dist-packages` (the system-level Python) while `rdkit` is satisfied from the boltz venv at `/scratch/u6sp/hpcuser.u6sp/boltz_predict_venv/lib/python3.12/site-packages`. The install-target for `chembl_structure_pipeline` itself is not stated in the pip output. The mixed package provenance makes it impossible to confirm from this log alone that the package landed in the correct venv rather than the system Python. (Probe 6 later uninstalled 1.2.4 from the same environment it was installing boltz into, which implies it was in the venv, but this is indirect evidence and the Probe 5 log does not make it explicit.)

### MAJOR-4: CUDA read-only filesystem error is unexplained

Before the boltz invocation, the log records:

```
/usr/bin/rm: cannot remove '/usr/local/cuda/compat/lib': Read-only file system
rm: cannot remove '/usr/local/cuda/compat/lib': Read-only file system
```

This error appears in the `=== boltz predict --help ===` section. An `rm` command targeting the CUDA compatibility library directory was executed as part of the test setup. It failed silently (the script continued). The purpose of this rm command is not documented, it fails every time across probes 4, 5, and 6, and its interaction with the CUDA environment is unknown. A failing pre-step that is never reported as a failure is a form of silent error.

### MAJOR-5: boltz version not recorded

The phase report's Table R records `Version: not recorded` for boltz. The venv path (`boltz_predict_venv`) and the Probe 6 log (line 7: `boltz==2.2.1 in .../boltz_predict_venv/`) establish that boltz 2.2.1 was in use. The version was available but was not captured. A methods section that records "not recorded" for the primary tool under test is not reproducible.

---

## Verification

### VERIFIED: chembl_structure_pipeline installation completed successfully (for the package itself)

`slurm-6462118.log` line 9 shows `Successfully installed chembl_structure_pipeline-1.2.4`. Pip's exit path confirms the package was written to disk. The install of the package artifact itself succeeded, even though the version was wrong for the boltz venv (see CRITICAL-4).

### VERIFIED: GPU identity is consistent and plausible

`slurm-6462118.log` line 2 reports `NVIDIA GH200 120GB`. The same GPU is reported in Probe 4 and Probe 6 logs. All three probes ran on the same hardware class.

### VERIFIED: boltz predict --help test genuinely invoked the real boltz binary

The traceback shows the correct binary path (`/scratch/u6sp/hpcuser.u6sp/boltz_predict_venv/bin/boltz`) and a real Python import chain through boltz's source files. This was not a stub or mock. The test genuinely attempted to load boltz and correctly exposed a missing dependency.

### VERIFIED: The missing `fairscale` error is real and is the proximate cause of the test failure

The import chain in the traceback is coherent: `boltz.main` → `boltz1` → `confidence` → `encoders` → `transformers` → `fairscale`. This is a legitimate import failure. Probe 6 subsequently installed `fairscale-0.4.13`, and `boltz predict --help` then produced the full help text. The causal relationship between the missing fairscale and the probe failure is confirmed by the recovery in the next probe.

### VERIFIED: Phase/probe number relationship is internally consistent

Across all five reports, Phase N corresponds to Probe N+1. The offset is consistent; there is no 0-based/1-based flip within the five-report sequence. (The gap at Probe 1 is noted under MAJOR-2 but is a coverage gap, not a numbering error within the captured set.)

### VERIFIED: The document for this phase does exist

A phase report at `reports/phase_04_probe_5_install_chembl_structure_pipeline_verify.md` exists on disk and was generated by the Rayca Modulon phase report generator. The finding is not absence of the document but rather that its content (procedure, artifact reference, and success status) is materially incorrect.

---

## Summary

The probe log itself honestly records two outcomes: a pip install that completed (with suppressed conflict details) and a boltz import that failed with `ModuleNotFoundError`. The phase report generated from this probe misrepresents both: it claims zero failures, cites the wrong log file, records an unrelated procedure, and omits the boltz version. The wrong version of chembl_structure_pipeline (1.2.4 instead of the required 1.2.2) was also installed, and the version conflict was masked by pip's default behaviour. The probe's stated goal — verify boltz predict --help — was not met.
