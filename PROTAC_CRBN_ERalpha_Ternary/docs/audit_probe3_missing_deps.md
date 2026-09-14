# Audit Report: Probe 3 — install remaining missing boltz deps on Isambard

**Audited log:** `slurm-6461898.log`  
**Phase report checked:** `reports/phase_02_probe_3_install_remaining_missing_boltz_deps_on_.md`  
**Auditor:** Independent Claude Code instance  
**Date:** 2026-09-11

---

## Executive Summary

The log for Probe 3 shows a dependency installation attempt that ended in failure: `boltz predict --help` crashes with `ModuleNotFoundError: No module named 'torchmetrics'`, and the import probe reports seven packages still missing. Multiple compounding errors exist in the phase report — wrong procedure content, wrong artifact reference, wrong size, and a false "0 failures" verdict. A critical internal contradiction between the import check and the CLI test reveals that the import check script is running against the wrong Python environment.

---

## Findings

### CRITICAL — Phase report procedure content is entirely wrong

The phase report `phase_02_probe_3_install_remaining_missing_boltz_deps_on_.md` describes a PROTAC ternary-complex structure prediction run (ARV-471 / ERalpha / CRBN, 3 diffusion samples, seed 42, pdb output) under the heading "Structure prediction of PROTAC-mediated protein–protein complex using diffusion-based generative modeling". This has nothing to do with what slurm-6461898.log actually contains. The actual log covers: venv creation, `pip install boltz pytorch-lightning`, an import check, and `boltz predict --help`. No structure prediction was performed in this probe. The procedure, rationale, inputs, and the "Status: running" field all belong to a different phase entirely.

The identical procedure content also appears verbatim in `phase_01_probe_2_fix_pytorch_lightning_missing_dep_in_bol.md`, which covers a different probe. Both phase reports were clearly stamped from the same wrong template.

### CRITICAL — Phase report references wrong output artifact (wrong file, wrong size)

The report's artifact table cites:

```
slurm-6462167.log | LOG | 14.0 KB | work | 315c97f0a382...
```

The correct log for Probe 3 is `slurm-6461898.log` (4.18 KB, timestamped 13:07). The file `slurm-6462167.log` (14.3 KB, timestamped 13:20) belongs to Probe 6 — a later bulk reinstall that finally produced a working `boltz predict --help`. The phase report for Probe 3 therefore has its provenance chain pointing at a different job with a different outcome, and the size does not match the actual Probe 3 log.

### CRITICAL — Phase report claims zero failures; the job plainly failed

The report states: "1 tool call(s) ran in this phase, 0 of which reported a failure." The actual log ends with:

```
File ".../pytorch_lightning/utilities/types.py", line 36, in <module>
    from torchmetrics import Metric
ModuleNotFoundError: No module named 'torchmetrics'
```

`boltz predict --help` exits with a traceback. The phase also exits with the import check reporting seven missing modules. A false "0 failures" verdict based on a job that terminates in an unhandled import error invalidates any downstream reliance on this phase report's verification section.

### CRITICAL — Import check and CLI test contradict each other for `pytorch_lightning`

The import check (log line 18) reports:

```
missing: ['pytorch_lightning', 'rdkit', 'biopython', 'gemmi', 'modelcif', 'hydra', 'omegaconf']
```

But the subsequent `boltz predict --help` traceback shows the boltz CLI gets past `from pytorch_lightning import Trainer, seed_everything` entirely. It fails three import levels deeper inside pytorch_lightning (at `torchmetrics`). This is only possible if `pytorch_lightning` IS importable from within the venv. The import check therefore used a different Python environment (most likely the system Python at `/usr/bin/python3`, not `/scratch/u6sp/hpcuser.u6sp/boltz_predict_venv/bin/python`). The import check gives false negatives for every package installed into the venv rather than the system Python. Any conclusions drawn from the "missing" list are unreliable.

---

### MAJOR — Silent installation: no confirmation that `pytorch-lightning` was installed

The `=== install boltz + pytorch-lightning ===` section (lines 6–14) produces only DEPRECATION warnings from pip about egg-installed packages already in the system environment. There is no `Successfully installed pytorch-lightning-...` line and no `Requirement already satisfied: pytorch-lightning` line. Under normal pip operation one of these two must appear on success; their absence means either the command failed silently, or pip could not resolve the requirement and exited without error. The probe script did not check the exit code of the pip call or validate the installation before proceeding, so this silent non-event was treated as a success.

The DEPRECATION messages do confirm that `lightning_utilities` and `lightning_thunder` are installed as eggs in the system env. These are distinct packages from `pytorch_lightning` and do not satisfy the import requirement.

### MAJOR — `mashumaro` version installed in intermediate probe (3.22) conflicts with what `boltz==2.2.1` pins (3.14)

While not directly in slurm-6461898.log, the chain of probes that followed Probe 3 is relevant to interpreting it. `slurm-6462059.log` (Probe 4) installs `mashumaro-3.22`. `slurm-6462167.log` (Probe 6) then uninstalls 3.22 and installs the pinned `mashumaro-3.14` (required by `boltz==2.2.1`). Similarly, `biopython-1.88` installed in Probe 4 was downgraded to `1.84`, and `gemmi-0.7.5` was downgraded to `0.6.5`, because the full `boltz==2.2.1` dependency resolution demands specific older versions. Installing newer versions in intermediate probes without constraining to the boltz pin is a recurrent pattern that produces a broken state until the full constrained reinstall in Probe 6.

### MAJOR — `chembl_structure_pipeline` version installed (1.2.4) differs from what `boltz==2.2.1` requires (1.2.2)

`slurm-6462118.log` (Probe 5) installs `chembl_structure_pipeline-1.2.4`. `slurm-6462167.log` confirms that `boltz==2.2.1` pins `chembl_structure_pipeline==1.2.2` and uninstalls the 1.2.4 version before installing 1.2.2. The intermediate probe therefore installed a version that boltz actively rejects. This error is not in Probe 3's log itself but directly follows from the pattern of piecemeal installation without consulting the full boltz==2.2.1 dependency tree.

---

## Verification

- **GPU identification is consistent.** slurm-6461898.log reports `NVIDIA GH200 120GB` (UUID GPU-1bfccac2-...). All other probes report GH200 nodes. The compute tier is consistent.
- **Venv path is consistent.** All probes reference `/scratch/u6sp/hpcuser.u6sp/boltz_predict_venv/` as the installation target.
- **The `/usr/local/cuda/compat/lib` read-only error is benign.** It appears on every probe log as part of the container entry-point and does not affect any probe step.
- **The `boltz` package version installed in the venv is confirmed as `2.2.1`.** slurm-6460283.log (Probe 2) shows `boltz 2.2.1 cuda True`, and slurm-6462167.log's `pip install boltz==2.2.1` confirms "Requirement already satisfied: boltz==2.2.1 in ...boltz_predict_venv". The boltz package itself was correctly installed and persisted across probes.
- **Phase file naming and numbering are internally consistent.** Phase reports are numbered 01–05 corresponding to Probes 2–6 (Probe 1, a boltzgen CLI probe in slurm-6460149.log, was not given a phase report). The `phase_index` field in each report frontmatter matches its filename prefix.
- **The `=== done ===` sentinel at the end of slurm-6461898.log is reached**, confirming the job script itself ran to completion even though the work it performed did not achieve the goal.

---

## Summary Table

| # | Severity | Finding |
|---|----------|---------|
| 1 | CRITICAL | Phase report procedure/content describes PROTAC structure prediction, not dep installation |
| 2 | CRITICAL | Phase report cites wrong output artifact (`slurm-6462167.log`, 14 KB) instead of `slurm-6461898.log` (4.18 KB) |
| 3 | CRITICAL | Phase report claims 0 failures; job ends in unhandled `ModuleNotFoundError` |
| 4 | CRITICAL | Import check and boltz CLI test contradict each other for `pytorch_lightning`, indicating import check used wrong Python environment (system, not venv) |
| 5 | MAJOR | `pip install pytorch-lightning` produces no output and no error, making the silent failure invisible to the probe script |
| 6 | MAJOR | Intermediate probes install wrong versions of `mashumaro` (3.22 vs pinned 3.14) and `biopython` (1.88 vs pinned 1.84) relative to `boltz==2.2.1` requirements |
| 7 | MAJOR | `chembl_structure_pipeline-1.2.4` installed in Probe 5 conflicts with `boltz==2.2.1`'s pin of `==1.2.2` |
| 8 | VERIFIED | GPU environment, venv path, and boltz 2.2.1 installation are consistent across all probes |
| 9 | VERIFIED | Phase file numbering (01–05 = Probes 2–6) is internally consistent |
