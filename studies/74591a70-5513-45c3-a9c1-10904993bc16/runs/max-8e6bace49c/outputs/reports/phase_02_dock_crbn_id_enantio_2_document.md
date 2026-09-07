
## Objective

Dock all 22 stereoisomers from `CRBN_ID_enantio_2.sdf` against the CRBN binding site of PDB 4CI2 (LVY ligand pocket), generating 5 poses per compound, using gnina GPU-accelerated docking.

---

## Receptor Preparation

**Source**: PDB 4CI2, chain B. CRBN in complex with LVY (thalidomide analogue).

| Choice | Decision | Rationale |
|--------|----------|-----------|
| Chain | B (CRBN) | Chain A is DDB1; LVY binds CRBN chain B |
| Missing atoms/loops | Modelled with PDBFixer | Several short loops absent in crystal |
| Protonation | pH 7.4 via PDBFixer `addHydrogens` | Simulate physiological buffer conditions |
| Histidine | PDBFixer default (HIS) — later fixed to HID/HIE for MM-GBSA | 12 δ-protonated (HID), 1 ε-protonated (HIE at Res 264) |
| Crystallographic waters | Removed | Not needed for gnina implicit-hydrogen docking |
| Co-crystallised LVY ligand | Removed | Box centred on its former position |
| Zinc ion (ZN, HETATM) | Retained in docking receptor | Located at 75.76, 152.11, 31.43 Å — outside LVY pocket |
| Final atom count | 6 188 ATOM records (chain B) | |

**Output**: `4CI2_receptor_for_docking.pdb`

### Docking Box

Centred on the LVY ligand centroid in the 4CI2 crystal structure:

| Parameter | Value |
|-----------|-------|
| Centre (x, y, z) | 85.06, 154.79, 13.38 Å |
| Dimensions (box) | 22 × 22 × 22 Å³ |
| Defined by | gnina `boxX/boxY/boxZ` + `width/height/depth` |

The 22 Å box fully encloses the LVY binding pocket (tri-tryptophan cage + flanking loops) while excluding the DDB1 interface.

---

## Docking Protocol

**Software**: gnina v1.x (containerised, GPU accelerated via Rayca sandbox).

| Parameter | Value |
|-----------|-------|
| Poses per ligand | 5 |
| Scoring | AutoDock Vina affinity (kcal/mol) + gnina CNN affinity/CNN pose score |
| Exhaustiveness | default (8) |
| GPU | Yes (sandbox GPU) |
| File passing | `files={'receptor.pdb': content, 'ligand.sdf': content}` — bare filenames, content-based |

**Note on file passing**: gnina is containerised and cannot access host filesystem paths. Files must be passed via the `files={}` parameter with bare filenames (not host paths or `/work/` prefixes). This was discovered and fixed during the run.

All 22 compounds were docked individually (22 gnina calls). 0 failures.

---

## Results

All 22 stereoisomers docked successfully.

### Top 10 by gnina Vina Affinity

| Rank | Compound | Affinity (kcal/mol) | CNN Affinity | Poses |
|------|----------|--------------------:|-------------:|------:|
| 1 | Compound_10_ent2 | −10.23 | 6.22 | 5 |
| 2 | Compound_4_s8 | −9.63 | 7.39 | 5 |
| 3 | Compound_8_ent2 | −9.60 | 6.94 | 5 |
| 4 | Compound_4_s12 | −9.52 | 7.29 | 5 |
| 5 | Compound_10_ent1 | −9.47 | 6.68 | 5 |
| 6 | Compound_4_s4 | −9.39 | 7.40 | 5 |
| 7 | Compound_4_s16 | −9.23 | 7.22 | 5 |
| 8 | Compound_4_s13 | −9.15 | 6.86 | 5 |
| 9 | Compound_4_s9 | −8.69 | 7.21 | 5 |
| 10 | Compound_4_s5 | −8.67 | 7.10 | 5 |

Full ranked results in `docking2_ranked.json`.

**Compound 4 dominance**: 8 of the top 13 positions occupied by Compound 4 stereoisomers, reflecting the rigidity and complementarity of the bicyclic scaffold to the tri-tryptophan cage.

**Enantiomeric selectivity observed**:
- Compound_10: ent2 (−10.23) vs ent1 (−9.47) — 0.76 kcal/mol preference
- Compound_1: ent2 (−7.80) vs ent1 (−6.60) — 1.2 kcal/mol preference
- Compound_8: ent2 (−9.60) vs ent1 (−6.92) — 2.68 kcal/mol strong preference

---

## Output Artifacts

| File | Size | Description |
|------|-----:|-------------|
| `docking2_results.json` | — | Full gnina output (all poses, all scores, all 22 compounds) |
| `docking2_ranked.json` | — | Ranked summary (affinity, CNN, parent compound) |
| `best_poses2/` | — | 5 poses per compound as SDF (22 files) |
| `best_poses2_top1/` | — | Best pose only per compound (22 SDF files, MM-GBSA input) |
| `ligs2/` | — | Individual input SDF files per compound (gnina input) |

---

## Limitations

- Receptor is treated as rigid; CRBN loop flexibility and side-chain rearrangement are not sampled.
- Crystallographic waters at the binding site are not included; water-mediated contacts may be missed.
- Single gnina docking run per compound; stochastic variation not assessed.
- CNN scores (gnina) complement Vina affinity but are not calibrated binding free energies.
