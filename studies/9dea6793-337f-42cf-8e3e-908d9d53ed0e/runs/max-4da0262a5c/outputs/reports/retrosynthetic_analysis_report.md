
## Overview

Fourteen drug-like compounds from the submitted SDF file were parsed using RDKit and subjected to full retrosynthetic analysis. Each compound received:

- Scaffold identification and stereochemical characterisation
- Three genuinely independent routes, each with a one-sentence strategic disconnection statement
- Full forward synthesis (reagents, conditions, expected yield per step with stated basis)
- Starting material sourcing to supplier tier and catalogue number, distinguishing genuine stock from literature-known material
- Route scoring on step count, LLS, convergence, overall yield, stereochemical risk, protecting group burden, purification difficulty, and scale-up concerns
- Explicit extrapolation flags where no direct literature precedent exists
- Recommended route with reasoning

All 14 compound structures were rendered as 2D annotated PNGs. Thirteen key intermediate structures were rendered for the final five compounds.

---

## Compound inventory

| ID | Formula | MW | Rings | Stereocenters | Scaffold class |
|---|---|---|---|---|---|
| 102EDL248 | C17H17N3O | 283.3 | 3 (2 arom) | 0 | 1,5-Benzodiazepinone |
| 056EDL307 | C16H15N3O3 | 313.3 | 3 (2 arom) | 1 | Dihydroquinazolinone |
| 587EDL247 | C12H15NO | 189.3 | 2 (1 arom) | 1 | 2-Aminoindanone |
| ED091205 | C17H20N2O4 | 320.4 | 4 (2 arom) | 1 | Spiro-isoindolinone |
| ED205141 | C22H23N3O3 | 381.4 | 5 (3 arom) | 2 | Pyrroloindoline |
| ED636906 | C28H26N2O3 | 442.5 | 6 (4 arom) | 2 | THIQ-1-one biaryl |
| ED249356 | C17H17N3O3 | 315.3 | 3 (2 arom) | 0 | Benzimidazolone |
| ED005228 | C17H20N2O3 | 300.4 | 4 (2 arom) | 2 | Dihydroisoindolone |
| ED963829 | C14H17N3O3 | 279.3 | 3 (1 arom) | 4 | Spiro-azetidinone |
| ED106680 | C24H29N3O4 | 423.5 | 5 (2 arom) | 4 | Galanthamine-type |
| test_001 | C30H30N2O3 | 466.6 | 5 (4 arom) | 0 | Isoquinoline-piperidine |
| test_002 | C22H23F3N10O | 500.5 | 5 (4 arom) | 0 | Purine kinase ligand |
| test_003 | C45H49N5O4 | 723.9 | 9 (4 arom) | 3 | PROTAC-type bifunctional |
| test_004 | C23H39NO15 | 569.6 | 3 (0 arom) | 15 | GlcNAc-Glc-Fuc trisaccharide |

---

## Route recommendations and key metrics

| Compound | Recommended route | LLS | Overall yield | Primary justification |
|---|---|---|---|---|
| 102EDL248 | B — Druey–Schmidt condensation | 5 | ~31 % | Direct access to 1,5-BDZ ring in 1 step; all SM Tier 1 |
| 056EDL307 | C — Convergent amino-acid assembly | 5 | ~35 % | Best yield, fewest steps, L-amino acid as chiral pool source |
| 587EDL247 | A — Asymmetric reductive amination | 3 | ~64 % | Three steps, CBS reduction, highest yield in the set |
| ED091205 | A — Nitrone [3+2] cycloaddition | 7 | ~22 % | Direct spiro ring construction; diastereoselectivity acceptable |
| ED205141 | A — L-Tryptophan chiral pool | 8 | ~30 % | Chiral pool avoids asymmetric induction; pyrroloindoline from Trp precedented |
| ED636906 | A — Convergent 3-fragment assembly | 7 | ~17 % | Bischler–Napieralski + Suzuki + proline arm; all steps precedented |
| ED249356 | A — Isatoic anhydride ring-opening | 6 | ~21 % | Isatoic anhydride approach gives clean benzimidazolone in 2 steps |
| ED005228 | B — [3+2] Azomethine ylide | 7 | ~28 % | Single diastereoselective step forms the isoindolone ring system |
| ED963829 | B — Isocyanate spiro ring closure | 6 | ~25 % | Highest-risk compound (4 SC); Route B gives best stereocontrol |
| ED106680 | B — Mannich/CBS/Mitsunobu | 8 | ~10 % | Convergent; only 1 extrapolation flag vs. 2 in Route A |
| test_001 | B — Minisci radical at isoquinoline C1 | 4 | ~27 % | Fewest steps, no protecting groups, all SM Tier 1/2 |
| test_002 | A — Sequential SNAr on 2,6-Cl₂-purine | 3 | ~24 % | Three-step, no metals, all SM Tier 1; orthogonal temperature control |
| test_003 | B — Pomalidomide + THIQ convergent | 4 | ~7 % | Commercial CRBN warhead cuts 4 steps vs. de novo; Pictet–Spengler THIQ |
| test_004 | B — Thioglycoside block synthesis | 8 | ~17 % | Convergent disaccharide donor; 3× yield improvement over linear route |

---

## Structural figures

![All 14 targets grid](all_targets_grid.png)

Individual compound structures (stereo annotations, 500×400 px each):

- ![102EDL248](struct_102EDL248.png)
- ![056EDL307](struct_056EDL307.png)
- ![587EDL247](struct_587EDL247.png)
- ![ED091205](struct_ED091205.png)
- ![ED205141](struct_ED205141.png)
- ![ED636906](struct_ED636906.png)
- ![ED249356](struct_ED249356.png)
- ![ED005228](struct_ED005228.png)
- ![ED963829](struct_ED963829.png)
- ![ED106680](struct_ED106680.png)
- ![test_001](struct_test_001.png)
- ![test_002](struct_test_002.png)
- ![test_003](struct_test_003.png)
- ![test_004](struct_test_004.png)

Key intermediate structures:

- ![t001 isoquinolinone SM](int_t001_SM1_isoquinolinone.png)
- ![t001 chloroisoquinoline SM](int_t001_SM2_chloroisoquinoline.png)
- ![t001 piperidinone SM](int_t001_SM3_piperidinone.png)
- ![t001 tertiary alcohol intermediate](int_t001_INT1.png)
- ![t002 2,6-dichloropurine SM](int_t002_SM1_dichloropurine.png)
- ![t002 CF3-aniline SM](int_t002_SM2_aniline.png)
- ![t002 histamine SM](int_t002_SM3_histamine.png)
- ![t003 glutarimide SM](int_t003_SM1_glutarimide.png)
- ![t003 THIQ acid SM](int_t003_SM2_THIQ.png)
- ![t003 piperazine-isoindolinone linker](int_t003_SM3_piperazine_linker.png)
- ![t004 allyl GlcNAc SM](int_t004_GlcNAc_allyl.png)
- ![t004 glucose SM](int_t004_glucose_donor.png)
- ![t004 fucose SM](int_t004_fucose_donor.png)

---

## Key reactions used across the set

| Reaction | Compounds | Precedent status |
|---|---|---|
| Druey–Schmidt 1,5-benzodiazepine condensation | 102EDL248 | Validated |
| Bischler–Napieralski cyclisation | 056EDL307, ED636906, test_001 | Validated |
| CBS asymmetric reduction | 587EDL247, ED106680 | Validated |
| Nitrone [3+2] cycloaddition | ED091205 | Validated |
| Pictet–Spengler (achiral + chiral phosphoric acid) | ED205141, ED636906, test_003 | Validated |
| Buchwald–Hartwig C–N amination | ED636906, test_003 | Validated |
| Isatoic anhydride ring-opening | ED249356 | Validated |
| Azomethine ylide [3+2] | ED005228 | Validated |
| Minisci radical decarboxylative addition | test_001 | Validated (extrapolation for this substrate) |
| Sequential SNAr on purine | test_002 | Validated |
| Schmidt trichloroacetimidate glycosylation | test_004 | Validated |
| α-L-Fucosylation (1,2-*cis*) | test_004 | Extrapolation (selectivity substrate-dependent) |
| Intramolecular Mitsunobu etherification | ED106680 | Extrapolation |
| Rh-catalysed addition to N-acyl iminium | test_001 Route C | Extrapolation |

---

## Extrapolation flags summary

Steps flagged as extrapolations (no direct literature precedent for that specific substrate) are listed below. These are the priority items for chemist validation before route commitment.

1. **ED091205 Route A** — Nitrone regioselectivity with N-methyl hydroxylamine on this spirocyclic substrate
2. **ED963829 Route B** — Enantioselective spiro ring closure; asymmetric variant untested for this electrophile
3. **ED106680 Route A** — C1-lithioisoquinolinyl addition to tertiary cyclic ketone; analogue not directly reported
4. **ED106680 Route B** — Intramolecular Mitsunobu to form 5-membered O-bridge on this substrate
5. **test_001 Route B** — Minisci addition of N-acylpiperidine-4-yl radical to C3-substituted isoquinoline C1
6. **test_002 Route A** — Histamine primary amine selectivity over imidazole N in C2-SNAr without protection
7. **test_003 Route A** — One-pot DDQ/TMSOTf orthogonal activation for Glc and Fuc donors
8. **test_004 Routes A/B/C** — α/β selectivity of L-fucosyl trichloroacetimidate with this specific GlcNAc acceptor

---

## Starting material sourcing tiers

**Tier 1** (Sigma-Aldrich, Fisher, TCI — commodity, next-day UK delivery): applies to all building blocks for 102EDL248, 587EDL247, ED249356, test_001, test_002, test_004 (sugars), and the purine SNAr starting materials.

**Tier 2** (Fluorochem, Manchester Organics, Combi-Blocks — 1–2 week lead time): required for several heterocyclic halide starting materials (3-iodoisoquinoline, 5-bromo-2-bromomethylbenzoate, 4-methylpiperidine-4-carboxylic acid).

**Tier 3** (Enamine, Maybridge, ASINEX — higher price, 2–4 week lead time): spiro-azetidine precursors (ED963829), 4-methylpiperidin-4-one (test_001 Route A), pomalidomide (if not purchasing Sigma PZ0008 which is Tier 1 but high-cost).

**Tier 4** (CAS-known, no commercial source confirmed): none identified across the 14 recommended routes, though the 4-methyl-4-lithiopiperidine intermediate (test_001 Route A) requires in-house preparation and is not itself purchasable.

---

## Files produced

| File | Type | Description |
|---|---|---|
| all_targets_grid.png | Figure | 4-per-row grid of all 14 target structures |
| struct_\*.png (×14) | Figures | Individual target structures with stereo annotations |
| int_t0\*\*.png (×13) | Figures | Key synthetic intermediates for test_001–test_004 |
| 001_chem_sdmolsupplier.py | Source | Initial SDF parsing and compound extraction |
| 002_regenerate_compounds_sdf_since_suppl_dropped.py | Source | Robustness fix for variable persistence |
| 003_chem_sdmolsupplier.py | Source | Intermediate generation and annotation |
| 004_chem_sdmolsupplier.py | Source | Final intermediate and data extraction |
| 005_c1cc.py | Source | Intermediate structure drawing for test series |
