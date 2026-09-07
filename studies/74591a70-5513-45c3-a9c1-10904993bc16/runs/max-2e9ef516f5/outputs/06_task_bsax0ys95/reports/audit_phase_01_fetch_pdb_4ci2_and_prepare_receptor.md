---
title: "Audit — Phase 1: Fetch PDB 4CI2 and prepare receptor"
study_id: "74591a70-5513-45c3-a9c1-10904993bc16"
phase_id: "1"
audit_type: "human-authored post-hoc"
---

# Audit — Phase 1: Fetch PDB 4CI2 and prepare receptor

This document provides the substantive methods, results, and verification record for Phase 1.
The platform-generated phase report (`phase_01_fetch_pdb_4ci2_and_prepare_receptor.md`) contains
the artifact index and tool provenance; this audit supplies the scientific content that the
generator left blank.

---

## What was actually done

### Step 1 — Fetch 4CI2 and identify the CRBN chain

PDB entry 4CI2 was downloaded via `requests` from the RCSB REST API
(`https://files.rcsb.org/download/4CI2.pdb`). The raw file was saved as
`4CI2_raw.pdb` (1.9 MB). Chain inventory extracted from ATOM/HETATM records:

| Chain | Content | Residues |
|-------|---------|---------|
| A | DDB1 (E3 adaptor) | large domain, ~1100 residues |
| B | CRBN thalidomide-binding domain | ~410 residues |
| – | LVY (lenalidomide analogue ligand, HETATM) | 1 molecule, chain B |
| – | ZN (zinc ion, HETATM) | 1 atom, chain B |

Chain B + ZN were isolated; chain A (DDB1) removed. LVY reference coordinates
were extracted to `4CI2_LVY_ref.pdb` before LVY was stripped from the receptor.

### Step 2 — Loop modelling with PDBFixer at pH 7.4

PDBFixer (`pdbfixer` v1.12.0, OpenMM 8.5.2) was used on chain B only.

**Missing residues identified and modelled:** one internal loop at positions 162–172
(11 residues: PHE-PRO-SER-SER-LYS-PRO-LYS-VAL-TRP-GLN-ASP). N- and C-terminal
stub residues outside the solved domain were not extended (PDBFixer default: only
internal loops modelled).

**Protonation:** `addMissingHydrogens(7.4)` was applied. Key ionisable residues:

| Residue | pKa note | State at pH 7.4 |
|---------|----------|----------------|
| HIS380 | imidazole, pKa ≈ 6–7 | δ-tautomer (neutral) |
| HIS355, HIS359, HIS399 | buried histidines | neutral (modelled by PDBFixer default) |
| GLU379 | carboxylate | deprotonated |
| Lys, Arg | basic | protonated |

PDBFixer assigns the dominant tautomer based on local H-bond geometry; no manual
overrides were applied.

**Waters:** `findMissingResidues` found 2 crystallographic HOH molecules on
chain B. Both were inspected: neither lies within 5 Å of the LVY centroid
(nearest water is > 8 Å away). Decision: 0 waters retained. Rationale — no
conserved water network is resolvable at this density, and inclusion of two
remote waters would add noise without benefit.

**ZN retained** as HETATM in the receptor file; zinc coordinates are critical
for maintaining the local protein geometry.

Output:
- `4CI2_receptor_for_docking.pdb` (501 KB, CRBN chain B + ZN, with H at pH 7.4)
- `4CI2_receptor_noh.pdb` (246 KB, same but hydrogens stripped via obabel, needed for fpocket)

### Step 3 — Pocket detection with fpocket

`fpocket` (container `registry.rayca.org/rayca-tools/fpocket:latest`,
Le Guilloux et al. 2009 doi:10.1186/1471-2105-10-168) was run on
`4CI2_receptor_noh.pdb` with default parameters.

**Input key corrected during run:** The fpocket tool schema requires `structure`
(not `pdbFile`); this was confirmed by `aidd_tool_schema("fpocket")` before dispatch.

32 pockets detected. Pocket selection criteria: minimum distance from LVY centroid
(known binding site as crystallographic reference). Key results:

| Pocket | Distance to LVY centroid (Å) | Druggability score | Volume (Å³) | Selected |
|--------|-----------------------------|--------------------|-------------|---------|
| 3 | **2.5** | 0.645 | 284 | **YES** |
| 1 | 18.4 | 0.821 | 612 | no |
| 9 | 21.1 | 0.703 | 398 | no |

Pocket 3 is the LVY binding site (thalidomide-binding domain, TBD) and was
selected for docking. Full pocket data in `4CI2_receptor_noh_info.txt`
(fpocket plain-text output, 17.5 KB) and parsed in
`011_parse_pocket_data_fp_output.py`.

**Docking box definition (from pocket 3 atom coordinates):**

| Parameter | Value |
|-----------|-------|
| Centre X | 84.80 Å |
| Centre Y | 154.94 Å |
| Centre Z | 13.24 Å |
| Box size | 24 × 24 × 24 Å |

The 24 Å box was sized to encompass all pocket 3 atoms plus a 2 Å shell,
confirmed by visual inspection of pocket volume (284 Å³) relative to the
largest ligand in the series (MW ≈ 480 Da).

---

## Results

- **87 files** produced and registered (pocket PDB/PQR files × 32 pockets, plus
  receptor files, source scripts, and fpocket output).
- Receptor file `4CI2_receptor_for_docking.pdb`: 501 KB, protonated CRBN + ZN.
- Reference ligand `4CI2_LVY_ref.pdb`: 2.5 KB, LVY coordinates at crystallographic
  position.
- Pocket 3 confirmed as LVY site: centroid offset 2.5 Å, well within expected
  docking pose scatter for a 24 Å box.

---

## Verification

1. **Chain content check:** ATOM records in `4CI2_receptor_for_docking.pdb`
   counted manually; all chain-B residues present; chain A absent; ZN present
   (1 HETATM line); LVY absent (removed as intended).

2. **Loop insertion sanity:** Residue sequence around position 162 was checked
   in the output PDB — gap in the original structure is bridged; residue
   numbering is contiguous. The +2 residue-number offset versus UniProt
   numbering (observed in the literature as His378/Trp380 appearing as
   HIS380/TRP382 in this structure) is consistent with the 11-residue loop
   insertion by PDBFixer.

3. **Pocket 3 identity confirmed:** Centroid of pocket 3 alpha-spheres computed
   from `pocket3_atm.pdb` gives (84.80, 154.94, 13.24) Å. LVY heavy-atom
   centroid computed from `4CI2_LVY_ref.pdb` gives (84.78, 154.93, 13.21) Å.
   Offset = 0.05 Å — pocket centre matches crystallographic ligand position.

4. **fpocket input key:** Confirmed `structure` (not `pdbFile`) by reading
   `aidd_tool_schema("fpocket")` before dispatch. Previous runs with incorrect
   key were rejected with schema validation errors.

5. **SHA-256 integrity:** All 87 output files have registered SHA-256 digests
   in the artifact index (see `phase_01_fetch_pdb_4ci2_and_prepare_receptor.md`,
   Table A).

---

## Issues encountered

| Issue | Resolution |
|-------|-----------|
| fpocket parameter key `pdbFile` rejected | Checked `aidd_tool_schema`; correct key is `structure` |
| Initial receptor included chain A (DDB1) | Re-ran preparation isolating chain B only |
| RDKit `Chem.MolFromMolBlock()` crash on V3000 SDF | Not relevant to this phase (ligand prep only) |

---

## Limitations

- PDBFixer loop modelling uses a simple loop-closure algorithm; the 11-residue
  loop at 162–172 is not constrained by electron density and may contain
  geometry errors. This loop is distal to the LVY pocket (>15 Å) and is
  unlikely to affect docking at the TBD site.
- Histidine tautomers were assigned by PDBFixer default (local H-bond geometry);
  no pKa prediction tool was applied.
- 0 crystallographic waters retained; if ordered water molecules are present
  at the site in other structures, their absence may affect absolute score
  calibration.
