# Audit Report: 2026-09-18 Pocket Detection Tool Survey
**Audited file:** `sessions/2026-09-18-pocket-detection-survey.md`  
**Audit date:** 2026-09-18  
**Evidence sources:** live platform tool registry (`find_capability`, `aidd_tool_schema` for `fpocket`, `grasp`, `pickpocket`, `pykvfinder`); git log at `/tmp/raycabio-push`

---

## CRITICAL Findings

### C-1 — No spec document exists for this phase

**Item checked:** Audit instruction 1.

No document exists anywhere in `/tmp/raycabio-push` or in the session directory that defines what this phase was supposed to produce: required tools, required output fields, coverage criteria, or acceptance conditions. The survey cannot be checked for completeness because there is no agreed definition of "complete." Every claim of correctness below is limited to internal consistency and agreement with the live registry — it cannot address omissions relative to an unstated brief.

**Severity:** CRITICAL — invalidates any completeness claim.

---

## MAJOR Findings

### M-1 — pickpocket "GPU Required: No (CPU)" is factually incomplete and may be wrong in practice

**Item checked:** Audit instruction 6 (claim stated as fact from a single data point).

The survey table states:

> `pickpocket` | ... | No (CPU)

The live `pickpocket` schema (`aidd_tool_schema('pickpocket')`) documents the `model_type` parameter with four options: `rf`, `svm`, `mlp`, and `deep`. The `deep` option is explicitly described as:

> "TensorFlow/Keras deep neural network (**GPU-accelerated**)"

The "No (CPU)" claim is true only for the three default model types. The `deep` model type is GPU-accelerated. The claim was not derived from the full schema; it appears to have been inferred from the tool's category (geometry-based / fpocket2 + STRIDE) without reading the complete input contract. A reader who trains or runs pickpocket with `model_type: "deep"` will encounter GPU requirements the survey says do not exist.

**Evidence:** `pickpocket` schema, `model_type` field, `enum: ["rf", "svm", "mlp", "deep"]`, description of `deep`: "TensorFlow/Keras deep neural network (GPU-accelerated)."

**Severity:** MAJOR — may mislead compute planning.

---

### M-2 — GrASP "GPU Required: Yes" stated as definitive fact; evidence is a single tool-summary phrase

**Item checked:** Audit instruction 6 (claim derived from a single data point).

The survey states:

> `grasp` | ... | **Yes** (bolded)

The `grasp` schema contains no explicit `requires_gpu: true` field, no runtime fallback description, and no note that the tool refuses to run without a GPU. The sole basis for the "Yes" claim is the tool summary's phrase "GPU-native identification of druggable binding sites." "GPU-native" typically means the model was built and optimised for GPU and will either fail or be impractically slow on CPU — but that distinction is not confirmed by the schema. The claim is plausible and probably correct, but it is stated as established fact on the strength of two words in a one-line summary. It has not been verified by attempting a CPU-only run or by reading a hardware-requirements note.

**Evidence:** `grasp` schema — no `requires_gpu` field; summary text only says "GPU-native."

**Severity:** MAJOR — stated with more certainty than the evidence supports; could cause incorrect resource allocation if the tool can in fact fall back to CPU.

---

## VERIFIED CORRECT

The following claims were checked against the live registry and confirmed accurate.

### V-1 — All four tool IDs present in registry
`fpocket`, `pykvfinder`, `pickpocket`, `grasp` each returned a valid schema from `aidd_tool_schema`. No tool ID was fabricated or mistyped.

### V-2 — fpocket output field names correct
Document claims: `top_pocket_druggability`, `top_pocket_score`.  
Registry `output_fields`: `["n_pockets", "output_structure", "pocket_files", "pockets", "structure_stem", "summary", "top_pocket_druggability", "top_pocket_score"]`.  
Both field names confirmed present and spelled correctly.

### V-3 — GrASP output field names correct
Document claims: `max_druggability`, `mean_surface_druggability`.  
Registry `output_fields`: `["colored_structure", "max_druggability", "mean_surface_druggability", "num_atoms", "num_surface_atoms", "summary", "top_atoms"]`.  
Both field names confirmed present and spelled correctly.

### V-4 — pickpocket method description correct
Document states: "Runs fpocket2 + STRIDE secondary structure."  
Registry summary: "It runs fpocket2 (classical alpha-sphere pocket detection) and stride (secondary structure)." Confirmed.

### V-5 — pyKVFinder and pickpocket correctly have no druggability score
Document marks both as "No" in the Druggability Score column.  
- `pykvfinder` output_fields: `area`, `avg_depth`, `avg_hydropathy`, `cavity_pdb`, `frequencies_pdf`, `max_depth`, `n_cavities`, `residues`, `results_toml`, `summary`, `volume` — no druggability field. Confirmed.  
- `pickpocket` output_fields: `columns`, `command`, `metrics`, `n_pockets`, `n_positive`, `output_dir`, `pockets`, `results_tsv`, `summary` — no druggability field. Confirmed.

### V-6 — pocketgen and pocketflow correctly categorised as generative/downstream
Document: "pocketgen — re-designs residues within a known binding site given protein + ligand."  
Registry: "Given a protein structure and a bound ligand, it re-designs the residues within the binding site." Match confirmed.

Document: "pocketflow — grows novel molecules from a pocket PDB."  
Registry: "Given a protein binding-pocket PDB it autoregressively grows novel, chemically…" Match confirmed.

### V-7 — `grasp` not confused with `grasp-jax`
The registry contains two tools sharing the GRASP name: `grasp` (druggable-site prediction) and `grasp-jax` (protein-complex structure prediction with experimental restraints — entirely different). The survey uses `grasp` throughout and correctly attributes Graph Attention Site Prediction to it. No identifier confusion is present in the document.

### V-8 — 4-Phase Pipeline numbering is consistent and 1-based
Phases are labelled Phase 1, 2, 3, 4 throughout. Next Steps are numbered 1–4. No 0-based / 1-based confusion, no skipped or repeated index.

### V-9 — Commit landed
`git log` at `/tmp/raycabio-push` confirms commit `ea3b94b` with message "session 2026-09-18: pocket detection tool survey and cryptic pocket workflow design." The file exists and is tracked. The document date (2026-09-18), filename date, commit date, and current date are all consistent.

---

## Summary Table

| ID | Severity | Description |
|---|---|---|
| C-1 | CRITICAL | No spec document — completeness cannot be verified |
| M-1 | MAJOR | pickpocket GPU claim wrong for `deep` model type |
| M-2 | MAJOR | GrASP "GPU Required: Yes" stated as fact from summary text alone |
| V-1–V-9 | VERIFIED CORRECT | Tool IDs, output field names, method descriptions, categorisation, numbering, commit |
