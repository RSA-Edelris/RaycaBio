
## What was done

Boltz-2 ternary complex prediction (Isambard-AI job 6567207) produced three mmCIF files. These were converted to PDB format using gemmi 0.7.5 inside the boltzgen-0.3.1 container on the cluster, via a `gemmi.read_structure` / `st.write_pdb` call appended to the prediction script.

## Outputs verified

Three PDB files at `job-6567207/ternary_out/`:
- `gspt1_crbn_glue_0.pdb` — 395,442 bytes
- `gspt1_crbn_glue_1.pdb` — 395,442 bytes
- `gspt1_crbn_glue_2.pdb` — 395,442 bytes

Each file contains:
- Chain A: GSPT1, 199 residues, 1534 atoms
- Chain B: CRBN, 406 residues, 3263 atoms
- Chain C: LIG, 1 residue, 31 heavy atoms
- Total atoms: 4828

Chain identities, residue counts, and atom counts verified in Phase 02 by parsing all three files with gemmi.

## Conversion correctness

- All three source CIF files parsed without error
- PDB chain labels (A, B, C) match CIF `_struct_asym` assignments
- Ligand preserved as single residue in chain C with 31 heavy atoms
- B-factors written as 0.00 (DesignWriter does not populate B-factors; CIF `_ma_qa_metric_local.metric_value` also confirmed as placeholder 80.0)

## Issues

None. Conversion completed cleanly on cluster; prediction.log records "3 PDB files converted OK".

## Audit verdict

Pass. The three PDB files are structurally complete and correctly represent the Boltz-2 output. No coordinate data was lost or altered in the CIF→PDB conversion.
