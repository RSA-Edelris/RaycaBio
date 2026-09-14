# Phase 12 — Constrained YAML Generation and Job Submission (ARV-001 to ARV-010, Dual Pocket Constraints)

## Summary

Ten Boltz-2 YAML input files were generated for the second PROTAC series prediction run,
each carrying dual `pocket` constraints derived from the ARV-471 model_0 reference structure
(job 6465991). One constraint anchors the CRBN warhead (glutarimide) to the CRBN binding
groove; the second anchors the ERα warhead (THN/phenol) to the ERα LBD pocket. The
constrained job was submitted to Isambard-AI GH200 as job **6540879** (run max-c3c67525e4).

---

## Objective

Repeat the 10-compound ternary complex prediction series with warhead pocket constraints, so
that neither the glutarimide nor the THN/phenol warhead floats away from its cognate binding
site during diffusion sampling. This addresses the primary reliability limitation of the
unconstrained job 6534300: CRBN orientation was unconstrained in no-MSA mode, making the
`lig→CRBN iptm` cooperativity proxy unreliable for the bottom-ranked compounds.

---

## Methods

### Pocket constraint derivation

Pocket residues were identified from the ARV-471 ternary complex reference structure:
`ARV471_ERalpha_CRBN_model_0.pdb` (job 6465991, model_0, best by overall confidence score
0.4778; see `phase_10_arv471_pdb_export.md`).

**Warhead atom identification.** RDKit 2026.03.4 was used to perform substructure
matching on the ARV-471 SMILES
(`O=C1CC[C@H](N2Cc3cc(N4CCN(CC5CCN(c6ccc([C@@H]7c8ccc(O)cc8CC[C@@H]7c7ccccc7)cc6)CC5)CC4)ccc3C2=O)C(=O)N1`)
against two SMARTS patterns:

| Warhead | SMARTS | SMILES atom indices | PDB atom names |
|:---|:---|:---|:---|
| Glutarimide (CRBN) | `O=C1CC[C@@H](N*)C(=O)N1` | 0,1,2,3,4,5,6,51,52,53 | O51,C55,C87,C99,C102,N85,C86,C56,O52,N81 |
| THN/phenol (ERα) | `[C@@H]1c2ccc(O)cc2CC[C@@H]1c1ccccc1` | 23–39 | C101,C79,C69,C60,C72,O53,C66,C77,C88,C100,C103,C80,C70,C58,C57,C59,C71 |

**Residue enumeration.** For each warhead, all protein heavy atoms (chains A and B) within
5.0 Å of any warhead atom were collected. Residue numbers are 1-indexed and refer to the
domain sequences in the YAML (ERα LBD 258 aa, CRBN TBD 469 aa), not full-protein numbering.

| Constraint | Chain | Residues (1-indexed) |
|:---|:---:|:---|
| Glutarimide → CRBN pocket | B | 111,112,113,114,125,240,241,246,249,250,261,263,264,266 |
| THN/phenol → ERα pocket | A | 47,50,53,54,57,88,91,92,95,98,108,125,128,129,132,225,228,229 |

Note: the glutarimide also shows ERα residues 238 and 243 within 5 Å in the reference
pose, but these reflect the specific ternary geometry of ARV-471 model_0 rather than the
intrinsic CRBN pocket. They were excluded from the CRBN pocket constraint to avoid
over-constraining the ERα–CRBN interface.

### YAML generation

A Python script read SMILES from the existing unconstrained YAMLs
(`ARV_001_ERalpha_CRBN_boltz_input.yaml` through `ARV_010_ERalpha_CRBN_boltz_input.yaml`)
and wrote 10 constrained YAMLs to `constrained_yamls/`. Each YAML follows Boltz-2 version 1
format with `msa: empty` for both protein chains and two `pocket` constraints (Boltz-2 only;
`max_distance: 6.0` Å, `force: false`):

```yaml
version: 1
sequences:
  - protein: {id: [A], sequence: <ERα 258 aa>, msa: empty}
  - protein: {id: [B], sequence: <CRBN 469 aa>, msa: empty}
  - ligand:  {id: [C], smiles: <compound SMILES>}
constraints:
  - pocket:
      binder: C
      contacts: [[B, 111], [B, 112], ..., [B, 266]]
      max_distance: 6.0
  - pocket:
      binder: C
      contacts: [[A, 47], [A, 50], ..., [A, 229]]
      max_distance: 6.0
```

### Cluster job

Identical hardware and settings to job 6534300 (Isambard-AI GH200, `boltzgen-0.3.1.sif`,
`boltz_predict_venv`, `--no_kernels` required for aarch64):

```
boltz_run.py predict <yaml> --cache $CACHE --accelerator gpu --model boltz2
    --diffusion_samples 3 --sampling_steps 50 --recycling_steps 3
    --output_format pdb --num_workers 0 --seed 42 --no_kernels
```

---

## Output Files

### Constrained YAML files (session root: `constrained_yamls/`)

| File | Ligand HA | SHA-256 (first 12) |
|:---|:---:|:---|
| `ARV_001_constrained.yaml` | 53 | — |
| `ARV_002_constrained.yaml` | 51 | — |
| `ARV_003_constrained.yaml` | 55 | — |
| `ARV_004_constrained.yaml` | 45 | — |
| `ARV_005_constrained.yaml` | 48 | — |
| `ARV_006_constrained.yaml` | 51 | — |
| `ARV_007_constrained.yaml` | 54 | — |
| `ARV_008_constrained.yaml` | 57 | — |
| `ARV_009_constrained.yaml` | 60 | — |
| `ARV_010_constrained.yaml` | 87 | — |

### Cluster job

| Field | Value |
|:---|:---|
| Job ID | 6540879 |
| Run ID | max-c3c67525e4 |
| Cluster | Isambard-AI Phase 2 (GH200, aarch64) |
| Submitted | 14 Sep 2026 |
| Walltime requested | 90 min |
| GPUs | 1 × GH200 |
| Status at phase close | submitted (queued) |

---

## Verification

**SMILES round-tripped from existing YAMLs.** SMILES for each compound were read from the
unconstrained YAMLs (themselves verified in phase_02 against the SDF source). No SMILES were
re-extracted from the SDF or typed by hand.

**Pocket residues derived from primary PDB coordinates.** The 5 Å distance calculation was
performed on ATOM/HETATM records from `ARV471_ERalpha_CRBN_model_0.pdb` directly. The
chain C HETATM count (54 atoms) and chain assignments (A=ERα, B=CRBN, C=ligand) were
confirmed before the distance search.

**Warhead substructure match confirmed.** RDKit returned non-empty matches for both
SMARTS patterns. Glutarimide matched 10 atoms (indices 0–6, 51–53); THN/phenol matched
17 atoms (indices 23–39). Total 27 distinct atoms covering both warhead ends. The piperazine-
piperidine linker atoms (indices 7–22, 40–50) were not included in either warhead set.

**Boltz-2 pocket constraint syntax confirmed from source.** The constraint format was read
from `/scratch/u6sp/hpcuser.u6sp/boltz_predict_venv/lib/python3.12/site-packages/boltz/data/parse/schema.py`
on Isambard (line 972–975 of the docstring example and lines 1527–1561 of the parser).
Multiple pocket constraints per binder are supported in Boltz-2 (the Boltz-1 single-binder
restriction does not apply). Residue indices in `contacts` are 1-indexed; the parser applies
`r - 1` internally. `max_distance` defaults to 6.0 if omitted.

**YAML spot-checked.** `ARV_001_constrained.yaml` was printed and confirmed to contain:
sequences for chains A, B, C; two `pocket` constraint blocks; correct binder `C`; contacts
in nested-list YAML format (parsed identically to inline `[B, 111]`).

---

## Limitations

- Pocket constraints are soft (penalty-based, not hard clamps). Boltz-2 can still produce
  poses where the ligand violates the distance requirement if the energy landscape strongly
  favours an alternative geometry. The `force: false` default (soft constraint) was retained.
- Pocket residues were derived from a single reference pose (ARV-471 model_0). If the
  true binding pose of another compound differs substantially, the reference pocket may
  over-constrain or mis-direct that compound's prediction.
- No MSA is used for either protein chain. CRBN pLDDT was ~35 in the unconstrained run;
  the pocket constraints narrow the CRBN orientation but do not guarantee high-confidence
  CRBN placement.
- ARV-010 (87 HA, PEG-13 linker) had ETKDGv3 conformer failure in job 6534300. The same
  failure may recur; if it does, ARV-010 results remain noise regardless of constraints.
- seed=42, as in the previous run. Changing the seed would produce different diffusion
  trajectories; no ensemble statistics are available from a single seed.

---

## References

- Passaro S, Corso G, Wohlwend J et al. Boltz-2: Towards Accurate and Efficient Binding
  Affinity Prediction. bioRxiv 2025. doi:10.1101/2025.06.14.659707
