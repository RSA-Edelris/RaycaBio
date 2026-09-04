# Audit Report: Inventory of Available Docking Tools

**Auditor:** Independent audit agent  
**Date:** 2026-09-04  
**Phase audited:** "Inventory available docking tools"  
**Method:** Every claim below was cross-checked against the live tool schema returned by `mcp__rayca__aidd_tool_schema` for each tool ID. No memory or prior knowledge was used as the verification source.

---

## Meta-finding (required per audit brief)

**CRITICAL — No written specification document exists for this phase.**  
The findings were produced live from tool schema queries with no prior written specification to diff against. There is therefore no independent check that the correct tool IDs were queried, that the full tool catalogue was enumerated, or that the schema returned on the day of the original inventory matches what was captured here. Any schema change between the inventory run and this audit would be invisible. Future phases that rely on this inventory as authoritative should treat it as a snapshot requiring re-verification before a campaign run, not as a durable specification.

---

## Per-tool findings

### gnina

**VERIFIED CORRECT** — required inputs match exactly.  
Schema `required`: `["proteinFile", "ligandFile"]`. Claim states `proteinFile + ligandFile`. Exact match.

**VERIFIED CORRECT** — box parameter names are correct.  
Claim: `boxX/boxY/boxZ + width/height/depth`. Schema lists all six as optional with defaults (boxX=35, boxY=27, boxZ=35; width/height/depth=20). Names are exact and the claim correctly separates them from required inputs.

**VERIFIED CORRECT** — all nine output fields match exactly.  
Schema `output_fields`: `["best_affinity_kcal_mol", "best_cnn_affinity", "best_cnn_pose_score", "gpu_used", "mode", "num_poses", "output_file", "poses", "summary"]`. Claim lists all nine; no extras, no omissions.

**VERIFIED CORRECT** — CNN ensemble rescoring characterisation.  
The `cnnScoring` parameter enum confirms `rescore` and `refinement` modes; the `none` mode is described as "Smina-equivalent", corroborating the "fork of smina/AutoDock Vina" description.

---

### autodock-vina

**VERIFIED CORRECT** — required inputs match exactly.  
Schema `required`: `["receptorFile", "boxX", "boxY", "boxZ", "width", "height", "depth"]`. Claim matches exactly (7 fields).

**VERIFIED CORRECT** — all six output fields match exactly.  
Schema: `["affinities_kcal_mol", "best_affinity_kcal_mol", "num_poses", "poses_pdbqt", "receptor_pdbqt", "summary"]`. Claim lists all six; exact match.

**VERIFIED CORRECT** — RILC-BFGS characterisation.  
The `rilc_bfgs` parameter is present and its description reads "RILC-BFGS local-optimization method introduced in Vina-GPU 2.1", confirming both the version label and the algorithm claim.

**MAJOR — Ligand optionality misrepresented; silent no-ligand failure path not disclosed.**  
The claim states "optional: ligandFile or ligandSmiles." This is technically consistent with the schema (both fields appear in the `optional` list), but the schema description for `ligandFile` explicitly states: *"Provide EITHER ligandFile OR ligandSmiles (exactly one)."* Neither field is in the `required` array, meaning a tool call with no ligand at all passes schema validation and is silently submitted. This matches audit item #4 (a default that turns a failure into a success): a run with only the required box coordinates but no ligand would be dispatched without error, producing a meaningless result. The inventory does not flag this constraint.

**MAJOR — Required box fields carry default values that enable a silent wrong-origin docking run.**  
The schema marks `boxX`, `boxY`, `boxZ` as `required: true` but also sets `default: 0` on all three, and `width/height/depth` as `required: true` with `default: 10`. If the calling layer treats "has a default" as "can be omitted," a run would be accepted and docked with the search box centered at the origin (0, 0, 0) — almost certainly the wrong location for any real protein. The inventory does not note this risk. This is audit item #4: a default that silently turns a misconfigured run into an apparent success.

---

### autodock-gpu

**VERIFIED CORRECT** — all-optional schema confirmed.  
Schema `required`: `[]`, 0 required fields. Schema notes explicitly: *"No input is strictly required; defaults cover every field (a bare {} runs the canonical example)."* Claim states "required inputs: none (all optional, defaults cover example)." Exact match.

**VERIFIED CORRECT** — all eight output fields match exactly.  
Schema: `["best_binding_energy_kcal_mol", "binary", "dlg_file", "num_clusters", "num_lga_runs", "per_run_energies_kcal_mol", "ranking", "summary"]`. Claim lists all eight; exact match.

**VERIFIED CORRECT** — key optional inputs are correctly named and typed.  
`mapsFldFile` is type string, `file_format: fld`; `ligandFile` is type string, `file_format: pdbqt`. Both names and formats match the claim.

**MAJOR — "autodock-gpu requires pre-computed AutoGrid maps" overstates the constraint.**  
The schema is explicit: all fields optional, a bare `{}` invocation runs a fully baked-in example. The claim that the tool "requires pre-computed AutoGrid maps rather than a raw PDB" is true as a practical workflow requirement for non-example runs, but the word "requires" implies a schema-level hard constraint. Any agent consuming this claim may incorrectly treat the tool as non-runnable until maps are prepared, or may not understand that the tool can be smoke-tested against the baked example without any inputs. The claim should have qualified: "requires maps for real targets; no schema-required fields exist."

**MINOR — Version "4.2.6" is not verifiable from the installed schema.**  
The schema does not include a version field. "4.2.6 (Scripps/Forli lab)" is asserted from prior knowledge or a source other than the schema query. The schema confirms LGA (Lamarckian Genetic Algorithm) from the `nrun` description: *"Number of independent Lamarckian Genetic Algorithm (LGA) runs."* The LGA label is verified; the version number is not.

---

### diffdock

**VERIFIED CORRECT** — required inputs match exactly.  
Schema `required`: `["protein_path", "ligand_description"]`. Claim matches exactly.

**VERIFIED CORRECT** — all five output fields match exactly.  
Schema: `["num_poses", "poses", "summary", "top_confidence", "top_pose_sdf"]`. Claim lists all five; exact match.

**VERIFIED CORRECT** — box-free characterisation confirmed.  
No box or grid parameters appear anywhere in the schema. The claim "box-free" is accurate.

**VERIFIED CORRECT** — small-molecule scope confirmed by schema language.  
The `ligand_description` description reads: *"DiffDock-L is designed for drug-like small molecules; it is not intended for large biomolecule 'ligands'."* This confirms the intended use case and supports the implicit small-molecule-docking characterisation.

---

### carsidock

**VERIFIED CORRECT** — required input matches exactly.  
Schema `required`: `["pdb_file"]`. Claim states `pdb_file`. Exact match.

**VERIFIED CORRECT** — all six output fields match exactly.  
Schema: `["ligands", "mode", "num_ligands", "num_poses_total", "output_dir", "summary"]`. Claim lists all six; exact match.

**VERIFIED CORRECT** — optional inputs correctly named.  
`sdf_file` and `smiles_file` are both present as optional fields in the schema. Names match the claim.

**VERIFIED CORRECT** — box-free characterisation confirmed.  
No box or grid parameters in schema. Correct.

**MINOR — sdf_file described as simply "optional" but schema description calls it practically required.**  
The schema marks `sdf_file` as optional, consistent with the claim, but the field description reads: *"Required to define the pocket in the default flow."* A run with only `pdb_file` and no `sdf_file` has no pocket definition. The inventory's bare "optional" label does not convey this. This is a lesser instance of the same silent-failure pattern noted under autodock-vina.

---

### af2dock

**VERIFIED CORRECT** — required inputs match exactly.  
Schema `required`: `["receptorFile", "ligandFile"]`. Claim matches exactly.

**VERIFIED CORRECT** — all six output fields match exactly.  
Schema: `["best_structure", "confidence", "iptm", "output_dir", "structures", "summary"]`. Claim lists all six; exact match.

**VERIFIED CORRECT** — protein–protein only characterisation confirmed by schema.**  
The `ligandFile` description reads: *"PDB structure file for your ligand protein"*; the `receptorFile` description reads: *"PDB structure file for your receptor protein."* Both are protein structures. The example input uses `antigen.cif` for both inputs. The claim "protein–protein only, not small molecules" is directly supported by the schema.

**VERIFIED CORRECT** — diffusion sampling characterisation confirmed.  
The `numSamples` and `numSteps` (denoising steps) parameters confirm diffusion-based sampling. The `iptm` output is consistent with AlphaFold-Multimer interface scoring.

---

## Additional claims (not per-tool schema fields)

**MAJOR — "gnina is the most battle-tested tool in prior sessions, best affinity −10.77 kcal/mol observed" is a single-data-point claim from episodic memory.**  
The inventory itself labels this as "derived from session memory." This is audit item #5: a rule or preference derived from a single (or undisclosed number of) prior data point(s). The value −10.77 kcal/mol is an observation from one ligand on one target in one prior run. It cannot be generalised to gnina being the most reliable tool for the current campaign's target or ligand class. This claim should not influence tool selection without independent corroboration.

---

## Summary table

| Tool | Required fields | Output fields | Other claims | Overall |
|---|---|---|---|---|
| gnina | VERIFIED CORRECT | VERIFIED CORRECT | VERIFIED CORRECT | Pass |
| autodock-vina | VERIFIED CORRECT | VERIFIED CORRECT | Ligand optionality: MAJOR; Box defaults: MAJOR | Flags |
| autodock-gpu | VERIFIED CORRECT | VERIFIED CORRECT | "Requires maps": MAJOR; Version: MINOR | Flags |
| diffdock | VERIFIED CORRECT | VERIFIED CORRECT | VERIFIED CORRECT | Pass |
| carsidock | VERIFIED CORRECT | VERIFIED CORRECT | sdf_file omission: MINOR | Minor flag |
| af2dock | VERIFIED CORRECT | VERIFIED CORRECT | VERIFIED CORRECT | Pass |
| Session memory claim | — | — | Single data point: MAJOR | Flag |
| Specification document | — | — | Does not exist: CRITICAL | Blocker |

---

## Recommended actions before using this inventory in a campaign

1. **Create a written specification document** recording tool IDs, schema hashes or version strings, and the date queried. Re-run schema queries at campaign start to detect any drift.
2. **autodock-vina**: Add a pre-flight check that exactly one of `ligandFile` / `ligandSmiles` is set before dispatching. Add a warning if box center coordinates are still at (0, 0, 0) after a user provides no coordinates.
3. **autodock-gpu**: Replace "requires pre-computed AutoGrid maps" with "requires maps for real targets; defaults run a baked streptavidin example" to avoid confusion between practical and schema-level requirements.
4. **gnina "best affinity" claim**: Treat as a rough orientation only. Do not use as a threshold for success or failure on the current campaign target without running a fresh benchmark.
5. **carsidock**: Document that `sdf_file` is functionally required to define the binding pocket for any real docking run despite its schema-optional status.
