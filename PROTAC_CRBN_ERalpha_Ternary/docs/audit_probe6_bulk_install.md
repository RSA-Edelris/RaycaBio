# Audit Report: Probe 6 — bulk-install remaining boltz deps with torch constraint

**Auditor:** Independent audit (Claude Sonnet 4.6)
**Audit date:** 2026-09-11
**Log file audited:** `/home/ubuntu/rayca-sessions/2d89c255-6bf5-4e5c-a4fb-99e4f253a979-1320c8c41b74/slurm-6462167.log`
**Phase report audited:** `/home/ubuntu/rayca-sessions/2d89c255-6bf5-4e5c-a4fb-99e4f253a979-1320c8c41b74/reports/phase_05_probe_6_bulk_install_remaining_boltz_deps_with_t.md`

---

## Check 1 — Phase report existence

**MAJOR: Phase report exists but contains wrong content for this phase.**

A phase report file does exist at `reports/phase_05_probe_6_bulk_install_remaining_boltz_deps_with_t.md`. The header correctly names this as "Probe 6 — bulk-install remaining boltz deps with torch constraint" and the file records the slurm log in its artifact table.

However, the Methods/Procedure section (section 45–65 of the report) describes a completely different task: "Structure prediction of PROTAC-mediated protein–protein complex using diffusion-based generative modeling" covering Boltz-2 prediction of an ARV-471 PROTAC ternary complex. This is description of a later inference run, not the dependency installation work that this probe actually performed.

Consequently the phase report does not document what was actually done in this phase. A reader consulting it for reproducibility would find a methods section that belongs to a different phase.

Additionally, the procedure table shows `Status: running` for the mis-described step, while the report header says `status: complete` — an internal self-contradiction within the report.

---

## Check 2 — Index and numbering errors

**MAJOR: Consistent off-by-one between probe numbers and phase numbers.**

All five phase reports in the `reports/` directory follow the pattern `phase_0N_probe_N+1_...`. That is, phase index 1 corresponds to probe 2, phase index 5 corresponds to probe 6. There is no report for probe 1 / phase 0. This systematic offset means either:

- Probe 1 was executed but never documented, and the study began numbering phases from 1 while probes from 2, OR
- The phase counter is 0-based internally but stored as 1-based in file names while the probe counter is 1-based, causing a permanent off-by-one.

Either way, the numbering is internally inconsistent across the two identifier schemes and creates potential for confusion when correlating a probe number to its phase report.

---

## Check 3 — Similar identifiers confused for one another

**MAJOR: torch version string recorded with a leading zero that does not match pip's normalised representation.**

Log line 3 (container version probe output) and line 5 (constraints file content) both record:

```
torch==2.7.0a0+7c8ec84dab.nv25.03
```

But pip's own output at line 8 reports the same installation as:

```
(2.7.0a0+7c8ec84dab.nv25.3)
```

The difference is `nv25.03` versus `nv25.3` — the leading zero in the numeric segment of the local version label. These are two different string representations of the same package. pip normalises numeric segments in local version labels (PEP 440), so `nv25.03` → `nv25.3` during comparison, and the constraint matched at runtime. However:

1. The version string written into the constraints file (`nv25.03`) was captured from `torch.__version__` or an equivalent raw source, which returns the unnormalised string, while pip normalises when reporting.
2. If the constraints file were reused on another system or audited by a tool that does strict string equality, `nv25.03` would not match what pip actually installed.

This is a real identifier mismatch between what was written to the constraints file and what pip reports the installed version to be. The protection worked in this run due to pip's normalisation, but the recorded constraint is not the canonical form of the version.

---

## Check 4 — Version pinning correctness

**MAJOR (same as Check 3, extended analysis).**

The torch constraint (`torch==2.7.0a0+7c8ec84dab.nv25.03`) was written to a constraints file and passed to pip during the bulk install. The result at line 8 shows torch was reported as "Requirement already satisfied" at version `2.7.0a0+7c8ec84dab.nv25.3` — torch was not modified.

The constraint functionally protected torch in this run. However, the version string discrepancy (`nv25.03` vs `nv25.3`) means the constraint file does not exactly match pip's canonical representation. Whether pip would enforce this as a hard pin in all invocation modes is not verified: with `--constraint`, pip treats it as an upper and lower bound, so a future `pip install` that sees only `nv25.3` installed and a constraint of `nv25.03` might attempt an install if normalisation were bypassed or if the version parsing differed.

The actual packages that were downgraded during the install confirm the constraint did its intended job for this one run:

| Package | Uninstalled | Installed |
|---|---|---|
| mashumaro | 3.22 | 3.14 |
| gemmi | 0.7.5 | 0.6.5 |
| biopython | 1.88 | 1.84 |
| modelcif | 1.8 | 1.2 |
| hydra-core | 1.3.6 | 1.3.2 |
| chembl_structure_pipeline | 1.2.4 | 1.2.2 |

These are all downgrades to meet boltz==2.2.1's exact pinned requirements. torch was correctly excluded from this list.

---

## Check 5 — Bare except or silent-failure patterns

**CRITICAL: pip dependency conflict details are missing from the log — a failure condition was silently swallowed or not captured.**

Log lines 62–63 read:

```
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
Successfully installed biopython-1.84 chembl_structure_pipeline-1.2.2 ...
```

The phrase "the following dependency conflicts" implies that a list of conflicting packages should follow. In current pip (≥22), this boilerplate is followed by lines identifying each conflict before the `Successfully installed` line. In this log the conflict list is entirely absent — line 62 ends the error message and line 63 immediately shows the success output.

This means either:
- The conflict lines were written to stderr and not captured in the Slurm log (which would mean the log is incomplete for auditing purposes), OR
- pip's output was truncated or redirected before reaching the log.

The result is that it is not possible to verify from this log what packages were in conflict. The install completed, but the conflicts that triggered an `ERROR:` message are unknown. This constitutes a silent-failure condition in the logging setup — an error fired, its details were not recorded, and the phase was reported as successful.

---

## Check 6 — Conclusion derived from a single data point

**MAJOR: Phase report's verification claim is based on a single tool call with no independent check.**

The Verification section of the phase report states: "1 tool call(s) ran in this phase, 0 of which reported a failure." A single pip invocation is the entire evidence base. No independent import test (`python -c "import boltz"`) or version check was run to confirm boltz is actually importable and functional after the dependency shuffle. The `boltz predict --help` in the log is a positive signal, but it is captured in the same single tool call as the install itself. If that tool call had a scripting error that caused `boltz predict --help` to run from a cached binary unaffected by the install, the single-call evidence would not catch it.

---

## Check 7 — Reversed positional arguments

**VERIFIED CORRECT: No reversed positional arguments detected.**

The pip install output (lines 6–63) shows a standard `pip install boltz==2.2.1 -c <constraints>` pattern. The `boltz predict --help` invocation (lines 64–158) shows the standard Click `boltz predict [OPTIONS] DATA` synopsis. No evidence of reversed argument order was found in the log.

---

## Check 8 — boltz predict --help completeness

**VERIFIED CORRECT: The --help output is complete and untruncated.**

The `boltz predict --help` output spans lines 67–157 and shows:
- A proper `Usage:` line with the correct positional argument (`DATA`)
- A complete options block covering all named parameters including advanced options (`--affinity_mw_correction`, `--write_embeddings`, `--no_kernels`, etc.)
- A terminal `--help  Show this message and exit.` line (line 157)
- The `=== done ===` sentinel on line 158

There is no truncation, no mid-option cutoff, and the Click CLI structure is intact. The output demonstrates a working CLI.

One environmental noise item is present immediately before the help output (lines 65–66):

```
/usr/bin/rm: cannot remove '/usr/local/cuda/compat/lib': Read-only file system
rm: cannot remove '/usr/local/cuda/compat/lib': Read-only file system
```

These errors originate from the container's CUDA compatibility layer setup script (not from boltz itself) and do not affect boltz's operation. They are noted but are not a boltz issue.

---

## Output Artifact Table in Phase Report

**MAJOR: Four of the five listed output artifacts were not produced by this phase.**

The Output Artifacts table in the phase report lists five files:

1. `slurm-6462167.log` — correctly attributed to this phase
2. `phase_01_probe_2_...md` — report from Phase 1
3. `phase_02_probe_3_...md` — report from Phase 2
4. `phase_03_probe_4_...md` — report from Phase 3
5. `phase_04_probe_5_...md` — report from Phase 4

Items 2–5 are pre-existing reports from prior phases. Listing them as outputs of Phase 5 / Probe 6 inflates the artifact count and misattributes provenance. The verification statement "5 file(s) were produced and registered" is incorrect — only 1 file was produced.

---

## Verification

Two checks came back clean with no issues found:

**No reversed positional arguments.** The pip install and `boltz predict --help` invocations use standard argument order throughout. No positional argument reversal was detected in the log.

**`boltz predict --help` output is complete and untruncated.** Lines 67–157 of slurm-6462167.log show the full Click options block including advanced flags (`--affinity_mw_correction`, `--write_embeddings`, `--no_kernels`) and the terminal `--help  Show this message and exit.` line. The `=== done ===` sentinel follows on line 158. No truncation or mid-option cutoff is present; the CLI is functional.

**Container image used:** `boltzgen-0.3.1.sif` at `/projects/u6sp/containers/boltzgen-0.3.1.sif` (Apptainer, aarch64). The venv Python was `/scratch/u6sp/hpcuser.u6sp/boltz_predict_venv/bin/python` (Python 3.12, inheriting system-site-packages from the container).

---

## Summary Table

| # | Check | Severity | Finding |
|---|---|---|---|
| 1 | Phase report existence | MAJOR | Report exists but its Methods/Procedure section describes a different phase (Boltz-2 structure prediction), not dependency installation |
| 2 | Index/numbering errors | MAJOR | Consistent off-by-one between probe numbers (starting at 2) and phase numbers (starting at 1); no probe 1 / phase 0 present |
| 3 | Similar identifiers confused | MAJOR | torch version recorded as `nv25.03` in constraints file but pip reports installed version as `nv25.3`; mismatched string representations of the same version |
| 4 | Version pinning correctness | MAJOR (same root) | Constraint functionally protected torch in this run via pip normalisation, but the pinned string is not pip's canonical form |
| 5 | Silent failure / bare except | CRITICAL | pip fired an ERROR about dependency conflicts but the conflict list is absent from the log; failure details were silently dropped or not captured |
| 6 | Rule from single data point | MAJOR | Successful completion claimed on the basis of a single tool call; no independent importability or function check was performed after the dependency shuffle |
| 7 | Reversed positional arguments | VERIFIED CORRECT | No reversed argument order detected in pip or boltz invocations |
| 8 | boltz predict --help completeness | VERIFIED CORRECT | Output is complete, all options shown, proper terminal line present, no truncation |
| — | Output artifacts | MAJOR | Phase report lists 4 pre-existing reports from earlier phases as artifacts of this phase; artifact count is inflated from 1 to 5 |
| — | Report internal consistency | MAJOR | Report header says `status: complete` but procedure table says `Status: running`; contradiction within the same document |
