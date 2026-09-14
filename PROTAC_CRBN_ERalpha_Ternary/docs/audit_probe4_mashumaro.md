# Audit Report: Probe 4 — install mashumaro, verify boltz predict --help

**Auditor:** Independent audit agent  
**Date:** 2026-09-11  
**Log audited:** `slurm-6462059.log`  
**Phase report examined:** `reports/phase_03_probe_4_install_mashumaro_verify_boltz_predict_h.md`

---

## Executive Summary

The probe 4 log (`slurm-6462059.log`) shows that `boltz predict --help` FAILED. The boltz CLI crashed on import before the `--help` text was ever displayed. Despite this, the phase report for this probe claims status "complete" with zero failures and describes a completely different procedure (a PROTAC ternary complex prediction run). The phase report also references the wrong SLURM log file. Additionally, the mashumaro version installed (3.22) is incompatible with boltz's declared requirements (3.14); a later probe had to uninstall 3.22 and replace it with 3.14 before boltz could start.

---

## Findings

### CRITICAL: boltz predict --help FAILED — the primary test objective was not met

**Source:** `slurm-6462059.log`, lines 9–20

The command `boltz predict --help` raised an import-time `ModuleNotFoundError` for `chembl_structure_pipeline` and exited before printing any help text:

```
ModuleNotFoundError: No module named 'chembl_structure_pipeline'
```

The traceback traces through `boltz/main.py` → `boltz/data/parse/fasta.py` → `yaml.py` → `schema.py`, which imports `chembl_structure_pipeline.exclude_flag`. The CLI never initialised. Nothing about boltz's predict interface was verified. The probe's stated objective was not achieved.

The job nonetheless continued to `=== done ===` (line 21) with no non-zero exit, meaning the SLURM job reported success even though the key assertion failed.

---

### CRITICAL: Wrong mashumaro version installed — introduces a version incompatibility

**Source:** `slurm-6462059.log` line 5; `slurm-6462167.log` lines 21, 56, 63

Probe 4 installed `mashumaro-3.22`. However, boltz==2.2.1 declares a dependency on `mashumaro==3.14` (exact pin). Evidence from the later probe (`slurm-6462167.log`) is unambiguous: it explicitly uninstalls mashumaro-3.22 (`Successfully uninstalled mashumaro-3.22`) and installs mashumaro-3.14 as part of the boltz dependency set. The later probe is the one that ultimately succeeds at running `boltz predict --help`.

Installing 3.22 instead of 3.14 is therefore the wrong action for the stated goal. Whether the version mismatch would cause runtime failures beyond the CLI startup is unknown, but it would cause `pip check` violations and could cause subtle behavioural differences with boltz's data serialisation.

---

### CRITICAL: Phase report references the wrong SLURM log file

**Source:** `reports/phase_03_probe_4_install_mashumaro_verify_boltz_predict_h.md`, Table A (Output Artifacts)

The phase report lists `slurm-6462167.log` (14.0 KB) as the artifact for this phase. The actual log for Probe 4 is `slurm-6462059.log` (22 lines, very short, ending in failure). `slurm-6462167.log` is a later job — it uninstalls mashumaro-3.22, performs a full bulk dependency reinstall, and runs a successful `boltz predict --help`. The phase report has been matched to the wrong job, making the traceability of this phase's results entirely invalid.

---

### CRITICAL: Phase report describes wrong procedure content — describes a prediction run, not a dependency probe

**Source:** `reports/phase_03_probe_4_install_mashumaro_verify_boltz_predict_h.md`, Section "Procedure"

The procedure section reads:

> "Boltz-2 structure prediction was performed to model the bridging geometry of ARV-471 PROTAC bound to estrogen receptor alpha (ERalpha, chain A, 258 amino acids) and cereblon (CRBN, chain B, 469 amino acids). The prediction was executed with 3 diffusion samples in PDB output format, seed 42, and no multiple sequence alignment, generating 3 candidate poses ranked by confidence score."

This describes an entirely different kind of work — an actual structure prediction campaign — not a dependency installation probe. The inputs listed (ARV471_ERalpha_CRBN_boltz_input.yaml, recycling_steps, diffusion_samples, seed 42) belong to a completely different phase. The probe 4 procedure was: pip install mashumaro, run boltz predict --help. That procedure is absent from the report.

The phase report's content appears to have been generated or copied from a downstream analysis phase and applied to this probe by mistake.

---

### CRITICAL: Phase report falsely claims success

**Source:** `reports/phase_03_probe_4_install_mashumaro_verify_boltz_predict_h.md`, fields `status` and Verification section

The report states:
- `status: "complete"`
- "1 tool call(s) ran in this phase, 0 of which reported a failure."

The actual probe 4 log shows an unambiguous failure. The phase record is incorrect and cannot be used to assert that probe 4 verified boltz functionality.

---

### MAJOR: Dependency conflict details not logged during mashumaro install

**Source:** `slurm-6462059.log`, lines 4–5

pip printed: "ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts."

The "following dependency conflicts" were never logged — either truncated, emitted to stderr and not captured, or cut off. The conflict almost certainly involved the mashumaro version pin (3.22 vs the boltz-required 3.14), but because it is not recorded, the full dependency state after the install cannot be reconstructed from the log alone.

---

### MAJOR: Silent failure — job script does not check exit code of boltz command

**Source:** `slurm-6462059.log`, lines 6–21

The structure of the job script is:
```
=== boltz predict --help ===
[command runs and crashes]
=== done ===
```

No exit-code check (`set -e`, `|| exit 1`, or equivalent) is visible. The `=== done ===` banner is printed regardless of whether the boltz command succeeded. Because SLURM reports job success based on the final script exit code (which is 0 here), the cluster job infrastructure would record this probe as successful. Any downstream decision logic that reads job status rather than log content would receive a false positive.

---

### MAJOR: Off-by-one between "Probe N" labels and "Phase N" indices — systematic across all probe reports

**Source:** `reports/` directory listing; all five phase report filenames and their frontmatter

Every report in the directory encodes a probe number that is one greater than its phase number:

| Filename prefix | Phase index (frontmatter) | Probe label in title |
|---|---|---|
| `phase_01` | 1 | Probe 2 |
| `phase_02` | 2 | Probe 3 |
| `phase_03` | 3 | Probe 4 |
| `phase_04` | 4 | Probe 5 |
| `phase_05` | 5 | Probe 6 |

The offset is consistent (phase_index N always corresponds to Probe N+1), strongly suggesting Probe 1 exists but is unrepresented in this directory — possibly a manually run or pre-cluster step. The offset is systematic rather than an isolated error, but it creates a persistent risk of misidentification when a reader cross-references "Probe 4" against phase records: phase_index 4 is Probe 5, not Probe 4.

---

### MAJOR: rm error at CUDA compat path silently ignored

**Source:** `slurm-6462059.log`, lines 7–8; also present in `slurm-6462167.log`, line 65–66

Both logs include:
```
/usr/bin/rm: cannot remove '/usr/local/cuda/compat/lib': Read-only file system
```

This occurs in a container entrypoint cleanup step, before boltz is invoked. It is silently ignored each time. The error does not appear to affect the boltz CLI (slurm-6462167.log succeeds despite it), but its presence in every job log without logging or handling means any actual CUDA compat regression would be indistinguishable from this known benign error.

---

## Verification

**GPU hardware identification correct.** Both the probe 4 log and every other log in this session consistently report NVIDIA GH200 120GB. The hardware-check section of the job script is functioning correctly.

**mashumaro-3.22 pip install command itself succeeded.** Line 5 of slurm-6462059.log shows `Successfully installed mashumaro-3.22 typing_extensions-4.16.0`. The installation action completed without a pip error. The problem is the version chosen (3.22), not the install mechanism.

**Import failure traceback is accurate and complete.** Lines 9–20 give a full Python traceback. The chain `boltz/main.py` → `fasta.py` → `yaml.py` → `schema.py` → `chembl_structure_pipeline.exclude_flag` is accurate; it correctly identifies the next missing dependency.

**boltz predict --help does succeed under correct conditions.** `slurm-6462167.log` (the later probe) demonstrates that after installing the full boltz-required dependency set including mashumaro==3.14 and chembl_structure_pipeline==1.2.2, the command prints the expected help text (lines 67–158). This provides a valid baseline for what a passing probe 4 should look like.

**Phase numbering offset is self-consistent.** While the probe/phase numbering is offset by one throughout, it is applied uniformly in filenames, frontmatter, and titles, so reports can still be located by probe label provided the offset is known.

---

## Summary Table

| ID | Severity | Finding |
|---|---|---|
| F1 | CRITICAL | `boltz predict --help` crashed with `ModuleNotFoundError`; primary test objective not met |
| F2 | CRITICAL | mashumaro-3.22 installed, but boltz requires mashumaro==3.14; later probe had to uninstall 3.22 |
| F3 | CRITICAL | Phase report references wrong SLURM log (`slurm-6462167.log` instead of `slurm-6462059.log`) |
| F4 | CRITICAL | Phase report procedure section describes a PROTAC prediction run, not a dependency install probe |
| F5 | CRITICAL | Phase report claims status "complete" / 0 failures despite actual probe failure |
| F6 | MAJOR | Dependency conflict details absent from log; full post-install state unverifiable |
| F7 | MAJOR | Job script does not check boltz exit code; SLURM records probe as success silently |
| F8 | MAJOR | Systematic off-by-one between phase_index N and Probe N+1 across all reports |
| F9 | MAJOR | CUDA compat rm error silently ignored in every job |
| V1 | VERIFIED CORRECT | GPU hardware identified correctly as NVIDIA GH200 120GB |
| V2 | VERIFIED CORRECT | pip install action completed; mashumaro-3.22 was placed in the venv |
| V3 | VERIFIED CORRECT | Traceback accurately identifies chembl_structure_pipeline as the next missing dependency |
| V4 | VERIFIED CORRECT | A passing `boltz predict --help` is demonstrated in slurm-6462167.log under correct conditions |
