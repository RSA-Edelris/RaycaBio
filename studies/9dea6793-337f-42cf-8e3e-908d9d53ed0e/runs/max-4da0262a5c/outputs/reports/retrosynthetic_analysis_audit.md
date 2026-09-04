
## Scope

This audit checks the retrosynthetic analysis phase for completeness, internal consistency, structural correctness, and calibration of yield estimates and extrapolation flags. It does not re-derive routes independently; it checks that the claims made are traceable to stated assumptions and that nothing was silently omitted.

---

## Coverage check

All 14 compounds present in the SDF file were analysed. The task description said "12 drug-like targets" but RDKit parsing of the V3000 MDL file returned 14 non-null molecules. The discrepancy was noted and all 14 were included. No compound was silently skipped.

| Compound | Scaffold named | 3 independent routes | Forward synthesis | SM sourcing | Scoring table | Recommendation |
|---|---|---|---|---|---|---|
| 102EDL248 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 056EDL307 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 587EDL247 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| ED091205 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| ED205141 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| ED636906 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| ED249356 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| ED005228 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| ED963829 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| ED106680 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| test_001 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| test_002 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| test_003 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| test_004 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

**Result: all 14 compounds fully covered.**

---

## Structural correctness

Structures were parsed by RDKit from the V3000 MDL file using `SDMolSupplier(removeHs=False, sanitize=True)`. Canonical SMILES and molecular formulae were verified by RDKit and printed; these matched the visual structures shown in the grid PNG.

Stereochemical handling:
- Compounds with `MDLV30/STERAC1` notation (racemic, unresolved stereocenters) were correctly identified and the analysis noted that no asymmetric induction is mandated
- test_003 uses `MDLV30/STEABS` (absolute stereocenters) — this was handled; the glutarimide (S) and THIQ stereocenters were assigned
- Stereocenter counts from `Chem.FindMolChiralCenters(mol, includeUnassigned=True)` were reported per compound

**Known structural interpretation caveat**: ED106680 was initially described in session context as "morphinan-type" before RDKit parsing confirmed a galanthamine-type 5-6-5-5 ring system (4 stereocenters). The corrected scaffold assignment was used throughout the analysis.

---

## Yield estimate calibration

Yield estimates were assigned by analogy with literature precedent, not by quantum-chemical or ML prediction. The basis for each estimate was stated. Audit spot-checks:

| Step | Claimed yield | Stated basis | Assessment |
|---|---|---|---|
| test_002 Step 1 (C6-SNAr, aniline, 2,6-Cl₂-purine, 100 °C) | 75 % | Davies *Chem. Rev.* 2007 | Consistent with published ranges (65–85 % for arylamines at C6) |
| test_001 Step 4 Minisci (tertiary radical at C1-isoquinoline) | 35–45 % | Minisci *Acc. Chem. Res.* 1975; Duncton *MedChemComm* 2011 | Consistent with reported 30–55 % for tertiary radicals on isoquinolines under these conditions |
| test_004 Step 13 (α-fucosylation, BF₃·Et₂O, −60 °C) | 50 % (5:1 α/β) | Walvoort *J. Org. Chem.* 2012 | The cited paper reports 3:1 to 10:1 α/β depending on acceptor; 5:1 and 50 % yield is within this range but must be verified on this specific substrate — correctly flagged as extrapolation |
| 587EDL247 Route A CBS reduction | 90 %, >96 % ee | Corey *JACS* 1987 | Standard CBS yields for acetophenone-type substrates are 85–95 %; claim is within range |
| ED963829 Route B (spiro ring closure, 4 stereocenters) | 25 % overall | Staudinger ketene cycloaddition analogy | The 4-stereocenter count makes this the highest-risk compound in the set; the 25 % figure is a midpoint estimate from analogous [2+2] reactions; the extrapolation flag was correctly applied |

No yield estimate was found to be inconsistent with its stated basis. Yield estimates for multi-step routes with 6–10 steps predictably give overall yields of 5–30 %, consistent with published total synthesis programmes for comparable complexity.

---

## Extrapolation flag completeness

Eight extrapolation flags were issued (see main report). Audit assessment:

| Flag | Appropriate? |
|---|---|
| ED091205 — nitrone regioselectivity on spirocyclic substrate | Yes — the exact substrate class is not in the Baran/Padwa nitrone literature |
| ED963829 — enantioselective spiro closure | Yes — asymmetric Staudinger for this N-heterocycle not reported |
| ED106680 Route A — C1-Li-isoquinolinyl + cyclic tertiary ketone | Yes — tertiary ketone partners for isoquinolinyl-Li are not commonly reported |
| ED106680 Route B — intramolecular Mitsunobu etherification | Yes — 5-membered ring Mitsunobu etherification yields are substrate-dependent; Tsunoda 1988 is an analogy, not an identity |
| test_001 Route B — Minisci on C3-substituted isoquinoline | Yes — C3 substituent effect on C1 regioselectivity needs verification |
| test_002 — histamine N-selectivity without protection | Yes — imidazole N vs. primary amine competition is substrate/temperature-dependent |
| test_003 Route C one-pot orthogonal glycosylation | Yes — this specific Glc/Fuc combination not reported in one-pot form |
| test_004 — α-Fuc selectivity on this acceptor | Yes — selectivity is notoriously acceptor-dependent for fucosyl donors |

**No missing extrapolation flags were identified** in the recommended routes. Three additional steps in non-recommended routes also carry extrapolation risk (noted in scoring tables).

---

## Starting material sourcing audit

Tier assignments were checked for the recommended routes:

- **Tier 1 claims verified**: 2,6-Dichloro-9H-purine (Sigma D5765 — confirmed catalogue item, commodity), histamine dihydrochloride (Sigma H7125 — confirmed), tyramine (Sigma T90344 — confirmed), L-fucose (Sigma F2252 — confirmed), allyl GlcNAc (Sigma A7882 — confirmed), pomalidomide (Sigma PZ0008 — confirmed but note high unit price ~£180/100 mg, Tier 1 by availability not cost)
- **Tier 2 claims**: 3-Iodoisoquinoline (Fluorochem) — confirmed as Tier 2 specialty item; 4-methylpiperidine-4-carboxylic acid — Fluorochem or Combi-Blocks, Tier 2 confirmed
- **No Tier 4 (literature-only) materials** in any recommended route — verified

**One potential misclassification**: pomalidomide listed as Tier 1 (Sigma PZ0008). It is genuinely available next-day from Sigma as a research chemical, but at ~£180/100 mg it would be Tier 1 by delivery speed but Tier 3 by cost. The tier definition used throughout this analysis was based on availability not price; the cost implication was flagged in the text ("high-cost").

---

## Independence of routes

Routes were assessed for genuine disconnection independence. Each recommended route uses a different key bond-forming strategy:

- test_001: organolithium addition (A) vs. Minisci radical (B) vs. Rh-iminium (C) — genuinely independent
- test_002: SNAr C6-first (A) vs. C2-first via fluoride (B) vs. Buchwald (C) — genuinely independent
- test_003: de novo glutarimide (A) vs. pomalidomide warhead (B) vs. Suzuki late-stage (C) — genuinely independent
- test_004: imidate sequential (A) vs. thioglycoside block (B) vs. one-pot orthogonal (C) — genuinely independent

No two routes within any compound share the same key ring-forming or stereocentre-setting step.

---

## Limitations and items for chemist follow-up

1. **No independent second annotator** for route labeling (construction vs. concession steps). A single annotator (this analysis) was used throughout; ideally, a second synthetic chemist would validate the strategic disconnection labels and ideality scores before route commitment.

2. **Yield estimates are order-of-magnitude, not TOSCA-model predictions**. Steps marked "extrapolation" could fail entirely or give very different yields; the overall yield figures for routes containing extrapolation flags carry ±50 % relative uncertainty.

3. **Purification difficulty was assessed qualitatively** (column, crystallisation, or potential co-elution noted). No actual logP/logD-based chromatography modeling was performed.

4. **test_004 protecting group deprotection sequence** was described but not fully optimised. The order of Bn removal (H₂/Pd-C) vs. TBS removal (TBAF) should be experimentally verified — TBAF can open certain sugar acetates and the NHAc is stable but the order matters.

5. **ED963829** (4 stereocenters, spiro-azetidine) carries the highest stereochemical risk in the set. The recommended route gives a racemate; if enantiopure material is needed, a chiral resolution or asymmetric ketene [2+2] protocol must be established — this is not described in detail and is a significant gap.

6. **ChemSketch representation**: The visual output consists of RDKit-generated 2D structure PNGs with stereo annotations. Full retrosynthetic scheme diagrams (with retrosynthetic arrows, intermediate numbering, and reagent blocks) were not generated as graphical files; these would need to be produced in ChemDraw or similar software by the chemist using the forward synthesis text as input.

---

## Verdict

The analysis is complete for all 14 compounds, internally consistent, and the extrapolation flags are appropriately placed. Yield estimates are consistent with the stated precedents. No Tier 4 starting materials appear in recommended routes. The primary limitation is single-annotator route labeling and the absence of graphical retrosynthetic scheme files. The eight extrapolation flags are the chemist's first-priority experimental checks.
