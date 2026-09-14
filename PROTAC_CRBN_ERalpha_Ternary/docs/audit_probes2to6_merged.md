# Merged Audit: Probes 2–6 — boltz dependency resolution on Isambard GH200
**Audit date:** 2026-09-11  
**Sources:** Direct log review (slurm-6460283, 6461898, 6462018, 6462059, 6462118, 6462167) + four independent subagent audit reports  
**Individual audit files:** `audit_probe2_pytorch_lightning.md`, `audit_probe3_missing_deps.md`, `audit_probe4_mashumaro.md`, `audit_probe5_chembl.md`, `audit_probe6_bulk_install.md`  
**Covered phase reports:** `phase_01_probe_2_...md` through `phase_05_probe_6_...md`

---

## Correction to the original merged audit

The first merged draft (also in this file) stated "No document exists for these phases." That was wrong. Five phase report files exist at the session root (`phase_01_...md` through `phase_05_...md`), all with filesystem timestamps of `Sep 11 13:22`, created retroactively in a single batch after Probe 6 completed. The subagents found and read them; this merged version incorporates those findings.

---

## CRITICAL findings

### CR1. All five phase reports cite the wrong SLURM log
**Source: subagent audit_probe2 C1; confirmed by agents for probes 4 and 5**

Every phase report from phase_01 through (at least) phase_03 lists `slurm-6462167.log` (14.0 KB, the final successful bulk-install run) as its output artifact, regardless of which probe the report covers. The correct logs are:

| Phase report | Correct log | Size |
|---|---|---|
| phase_01 (Probe 2) | slurm-6460283.log | 3.1 KB |
| phase_02 (Probe 3) | slurm-6461898.log | varies |
| phase_03 (Probe 4) | slurm-6462059.log | 22 lines |
| phase_04 (Probe 5) | slurm-6462118.log | 28 lines |
| phase_05 (Probe 6) | slurm-6462167.log | 14.0 KB ✓ |

Only phase_05 has the right log. The SHA-256 digests recorded in phases 01–04 are for the wrong file. **Traceability for probes 2–5 is broken.**

### CR2. All five phase report Methods sections describe a PROTAC structure prediction run, not a dependency probe
**Source: subagent audit_probe2 C2; audit_probe4 F4; audit_probe6 check 1**

Every phase report's Procedure section is identical boilerplate describing a Boltz-2 structure prediction for the ARV-471 PROTAC ternary complex (ERα 258 aa, CRBN 469 aa, 3 diffusion samples, seed 42). None of the probe phases performed structure prediction. The actual work — `pip install X; boltz predict --help` — is absent from every report. **The reports cannot be used for reproducibility of the probe sequence.**

### CR3. Jobs that exited with code 1 are recorded as "complete" with "0 failures"
**Source: subagent audit_probe2 C3; slurm-6460283.log line 29-31; audit_probe4 F5**

`slurm-6460283.log` (Probe 2) contains the Rayca harness message `RAYCA: the job stopped at line 38 with exit 1`. The corresponding phase report records `status: complete` and "0 of which reported a failure." This pattern repeats for probes 4 and 5, which also ended in tracebacks (no `|| true` on `boltz predict --help` in those scripts). The phase record cannot be trusted for pass/fail determination.

### CR4. pip dependency conflict details silently absent from Probe 6 log
**Source: subagent audit_probe6 check 5; slurm-6462167.log lines 62-63**

Line 62: `ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.`  
Line 63: `Successfully installed biopython-1.84 ...` (immediately, no conflict list)

The conflict list was not captured — written to stderr and not redirected, or truncated. What was in conflict cannot be determined from this log. The install completed and the right versions landed, but the conflicts that triggered the `ERROR:` are unknown.

---

## MAJOR findings

### M1. Phase reports created retroactively, none existed during execution
**Source: subagent audit_probe2 M1 (filesystem timestamp Sep 11 13:22; slurm logs predate this)**

There was no contemporaneous record of any probe's intent, method, or outcome. The retroactive reports also contain the content errors in CR1 and CR2 above.

### M2. Probe title calls the wrong environment: "boltzgen container", not the boltz venv
**Source: subagent audit_probe2 M2**

The probe title says "fix pytorch_lightning missing dep in **boltzgen container**." The work was performed against a fresh pip venv at `/scratch/u6sp/hpcuser.u6sp/boltz_predict_venv/` using the boltzgen container only as the Python runtime. The boltzgen container (`/opt/boltzgen/venv/`) is a separate, functional environment that was never broken. The mislabelling confuses the two environments.

### M3. Intermediate probes installed wrong package versions; Probe 6 had to correct them
**Source: subagent audit_probe2 M4; audit_probe4 F2; slurm-6462167.log lines 55-63**

Probes 3–5 installed newer-than-required versions. Probe 6 downgraded all of them to boltz==2.2.1's pinned requirements:

| Package | Installed by earlier probe | boltz-required (final) |
|---|---|---|
| mashumaro | 3.22 | 3.14 |
| gemmi | 0.7.5 | 0.6.5 |
| biopython | 1.88 | 1.84 |
| modelcif | 1.8 | 1.2 |
| hydra-core | 1.3.6 | 1.3.2 |
| chembl_structure_pipeline | 1.2.4 | 1.2.2 |

**⚠ DISAGREEMENT between auditors on severity:** The subagent for Probe 4 rated "wrong mashumaro version" as CRITICAL (it invalidates the probe's stated objective). The direct audit rated it MAJOR (the final probe corrected it, so the overall goal succeeded). The subagent's argument: Probe 4's explicit goal was "verify boltz predict --help" and that goal was not achieved regardless of the version issue; the CRITICAL designation covers that probe specifically, not the session overall. Both readings are defensible; the finding stands either way.

### M4. Systematic off-by-one: phase_index N = Probe N+1
**Source: subagent audit_probe2 M6; audit_probe4 F8; audit_probe6 check 2**

All five files follow the pattern `phase_0N_probe_N+1`. Probe 1 (`slurm-6460149.log`, the initial boltzgen capability check) has no phase report. The offset is consistent but undocumented.

### M5. torch version string mismatch between constraints file and pip's canonical form
**Source: subagent audit_probe6 check 3**

The constraints file recorded `torch==2.7.0a0+7c8ec84dab.nv25.03`; pip reports the installed version as `2.7.0a0+7c8ec84dab.nv25.3` (PEP 440 normalises the leading zero from `nv25.03`). pip matched them correctly in this run via normalisation, so torch was not modified. However, the stored constraint is not the canonical form. Strict-equality tooling could fail to match it.

### M6. Phase_05 Output Artifacts table lists 4 prior-phase reports as outputs of Probe 6
**Source: subagent audit_probe6 artifacts section**

The phase_05 report lists `phase_01_...md` through `phase_04_...md` as artefacts produced by Probe 6. Those files were produced by earlier phases. The verification statement "5 file(s) were produced" in phase_05 is wrong; only 1 file was produced by Probe 6.

### M7. `import boltz` passes while `boltz predict --help` (boltz.main) is broken — false all-clear
**Source: direct log audit; slurm-6462018.log lines 34-35 vs 40-51**

Probe 4's import test reported `OK: ['boltz', ...]` and `MISSING: []`. Four lines later `boltz predict --help` failed on mashumaro. Python's `import boltz` succeeds before boltz.main's deeper imports are triggered; the test gave a false green for mashumaro.

### M8. try/except in Probe 3's import test conflates "not installed" with "not importable"
**Source: direct log audit; slurm-6461898.log lines 18, 28-39**

Probe 3 installed pytorch_lightning, then the import test reported it as "missing". pytorch_lightning was installed; it could not import because torchmetrics was absent. The broad try/except caught the transitive ImportError and attributed it to the top-level module. The diagnosis (torchmetrics is the real blocker) was recoverable from the deeper traceback in the same log, but the `missing:` list itself is misleading.

### M9. wandb 0.18.7 installed in final venv; not tested for network-call behavior at startup
**Source: direct log audit; slurm-6462167.log line 63**

wandb contacts remote endpoints by default on startup. If Isambard compute nodes lack outbound network (untested), wandb could delay or fail at inference job startup. No probe tested this path.

### M10. Phase_05 report header says "complete"; procedure table says "running" — internal contradiction
**Source: subagent audit_probe6 check 1**

---

## Verification

| Item | Evidence |
|---|---|
| pytorch_lightning is the first import blocker in boltz==2.2.1 --no-deps | slurm-6460283.log line 26: `from pytorch_lightning import Trainer` → `ModuleNotFoundError` at boltz/main.py line 16 |
| CUDA visible (GH200 120GB) throughout all probes | Confirmed consistently in every log |
| torchmetrics is pytorch_lightning's transitive blocker | slurm-6461898.log full traceback: `pytorch_lightning.utilities.types → from torchmetrics import Metric → ModuleNotFoundError` |
| mashumaro is needed by boltz.data.types | slurm-6462018.log: `boltz.data.types line 7 → from mashumaro.mixins.dict import DataClassDictMixin → ModuleNotFoundError` |
| chembl_structure_pipeline is needed by boltz.data.parse.schema | slurm-6462059.log: `schema.py line 9 → from chembl_structure_pipeline.exclude_flag import exclude_flag → ModuleNotFoundError` |
| fairscale is needed by boltz.model.modules.transformers | slurm-6462118.log: `transformers.py line 3 → from fairscale.nn.checkpoint.checkpoint_activations import checkpoint_wrapper → ModuleNotFoundError` |
| torch was NOT modified by the final bulk install | slurm-6462167.log line 8: "Requirement already satisfied: torch" |
| boltz predict --help output is complete and untruncated in Probe 6 | slurm-6462167.log lines 67–158: all 45+ options listed, terminal `--help Show this message and exit.` line present |
| The six package downgrades match boltz==2.2.1's declared requirements | slurm-6462167.log lines 55–63: explicit uninstall + reinstall at correct versions |
| boltz 2.2.1 was the target version throughout | All probes targeted boltz==2.2.1 consistently |
| No reversed positional arguments in any probe | Checked in probes 2, 4, 6; clean |

---

## Summary table

| ID | Severity | Finding |
|---|---|---|
| CR1 | CRITICAL | All phase reports 01–04 cite slurm-6462167.log (Probe 6) as their artifact; correct logs differ |
| CR2 | CRITICAL | All phase reports describe PROTAC structure prediction in Methods; actual work (pip + --help) absent |
| CR3 | CRITICAL | Jobs with exit code 1 recorded as "complete" / "0 failures" in phase reports |
| CR4 | CRITICAL | pip conflict list absent from Probe 6 log; failure details silently dropped |
| M1 | MAJOR | All phase reports created retroactively (Sep 11 13:22); none existed during execution |
| M2 | MAJOR | Probe title says "boltzgen container"; actual env is boltz predict venv (separate) |
| M3 | MAJOR | Intermediate probes installed wrong versions; Probe 6 had to downgrade 6 packages (**⚠ subagent for Probe 4 rates this CRITICAL; direct audit rates MAJOR — disagreement preserved**) |
| M4 | MAJOR | Systematic off-by-one: phase_index N = Probe N+1; Probe 1 has no phase report |
| M5 | MAJOR | torch constraint recorded as `nv25.03`, pip reports `nv25.3`; not pip-canonical form |
| M6 | MAJOR | phase_05 artifact table lists 4 prior-phase reports as outputs of Probe 6 |
| M7 | MAJOR | `import boltz` passes while boltz.main is broken; import test gives false all-clear |
| M8 | MAJOR | try/except in Probe 3 import test reports installed-but-broken modules as "missing" |
| M9 | MAJOR | wandb 0.18.7 present in venv; startup network calls untested on Isambard compute |
| M10 | MAJOR | phase_05 header says "complete"; procedure table says "running" — internal contradiction |

**No finding invalidates the final outcome.** The dependency chain was correctly resolved. All six missing modules (pytorch_lightning, torchmetrics, mashumaro, chembl_structure_pipeline, fairscale, and indirect deps) were identified accurately from tracebacks, and `boltz predict --help` ran cleanly at the end of Probe 6. The CRITICAL issues are documentation failures, not inference failures.
