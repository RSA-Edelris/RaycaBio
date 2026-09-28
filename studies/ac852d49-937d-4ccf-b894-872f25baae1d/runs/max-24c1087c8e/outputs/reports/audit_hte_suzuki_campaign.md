# Audit Report: Phase 1 — Design HTE Campaign for Suzuki-Miyaura Coupling Optimisation

**Auditor:** Independent reviewer  
**Date:** 2026-09-15  
**Session:** ac852d49-937d-4ccf-b894-872f25baae1d  
**Phase report path:** reports/phase_01_design_hte_campaign_for_suzuki_miyaura_coupling_.md

---

## Finding 0 — No Artifact Was Written for This Phase

**MAJOR**

A phase report file exists at `reports/phase_01_design_hte_campaign_for_suzuki_miyaura_coupling_.md`, but it is a metadata shell only. Its content under every section reads:

> "No records were captured for this phase."  
> "No tool call is on record for this phase."  
> "No output file was registered."

The design work was delivered as a conversational response and was never written to a file. No table, no plate-map grid, no condition list, no rationale document, and no BO comparison was persisted as an artifact. This violates basic reproducibility requirements: the experiment cannot be set up from the record alone, and the design cannot be reviewed, version-controlled, or shared with a CRO without reconstructing it from a chat transcript.

**Impact:** Reproducibility is broken for this phase. Every claim checked below had to be supplied by the review prompt rather than read from the document — which also means this audit cannot rule out transcription errors in the claims themselves. Corrective action: rerun or reconstruct the phase and write output to a structured artifact (CSV plate map, JSON or markdown condition table, and a brief narrative rationale).

---

## Check 1 — Index and Numbering Errors

### 1a. Well counts

**VERIFIED CORRECT**

4 catalysts × 4 bases × 3 solvents = 48 unique conditions. 48 × 2 replicates = 96 wells, filling exactly one standard 96-well plate. The arithmetic is correct.

### 1b. "40 unique tested combinations" from removing 16 control wells

**VERIFIED CORRECT (with a note on presentation)**

Starting from 48 unique conditions × 2 = 96 wells: replacing 8 condition-pairs with control pairs removes 16 wells, leaving 80 wells for 40 unique test conditions. The three quantities — 16 wells, 8 well-pairs, 40 unique combinations — are mutually consistent: 8 pairs × 2 = 16; 96 − 16 = 80; 80 ÷ 2 = 40; equivalently 48 − 8 = 40 unique conditions.

The formula as reportedly written ("48 − 8 (pairs) = 40") does conflate units (subtracting pairs from unique-condition count) but arrives at the correct result because the numbers happen to cancel. This is a presentation issue worth clarifying in any written version.

---

## Check 2 — Similar Identifiers Confused

### 2a. Replicate-block row labels: E = Cat-C, not Cat-A

**CRITICAL**

The plate map assigns rows A–D to rep-1 in catalyst order Cat-A, Cat-B, Cat-C, Cat-D. Rows E–H are labelled as rep-2 of the same four catalysts. However, the row assignments reported are: E = Cat-C, not Cat-A. If this is accepted as stated, the second replicate block does not start at the same catalyst as the first. This means:

- Row E ↔ Cat-C (expected: Cat-A)
- Row F ↔ Cat-D (expected: Cat-B)
- Rows G and H ↔ Cat-A and Cat-B (expected: Cat-C and Cat-D)

Any analysis that treats row-index as a proxy for replicate identity, or any downstream parsing script that maps row E → Cat-A, will systematically misassign half the plate. Yield data for Cat-A wells in rep-2 would be attributed to Cat-C and vice versa. This would corrupt all catalyst-level statistics and any structure–activity inference.

**Corrective action:** The plate map must be regenerated so that rep-2 rows E–H repeat the same catalyst ordering as rep-1 rows A–D (E=Cat-A, F=Cat-B, G=Cat-C, H=Cat-D), or the actual intended ordering must be explicitly documented and verified before any liquid-handling script is run.

### 2b. Ambiguous label convention "A-X" / "B-X" in the grid key

**MAJOR**

The key reportedly states: "A-X = first-block assignment, B-X = second-block assignment." In the same grid, rows are also named A through H, and catalysts are named Cat-A through Cat-D. The letter "A" therefore collides across three namespaces simultaneously: (i) the plate row letter, (ii) the block identifier in the key, and (iii) the catalyst suffix. A label such as "A-A" could be parsed as (row A)-(catalyst A), (first block)-(catalyst A), or (row A)-(first base). This ambiguity cannot be resolved without an additional disambiguation rule, and no such rule is reported.

**Impact:** Any downstream data entry, LIMS import, or analysis script that parses well labels from this key is at risk of silent misassignment. The convention must be replaced with a non-overlapping scheme (e.g., numeric rows, spelled-out catalyst names, or separate fields for block, row, and reagent identity).

---

## Check 3 — Chemistry Factual Claims

### 3a. 4-Bromoanisole: electron-donating methoxy slows oxidative addition vs aryl iodides

**VERIFIED CORRECT**

This claim is accurate on both counts. (i) Aryl bromides undergo oxidative addition to Pd(0) more slowly than aryl iodides; the C–Br bond is stronger and the substrate is less electrophilic at carbon. (ii) The para-methoxy group is electron-donating by resonance, which further reduces the electrophilicity of the ipso carbon and retards oxidative addition relative to an unsubstituted or electron-poor aryl bromide. Using an electron-rich aryl bromide as the model substrate is therefore a deliberate choice of a challenging substrate, which is scientifically sound.

### 3b. Cs₂CO₃ and bulky monophosphines "synergistic" for electron-rich aryl bromides

**MAJOR**

The claim couples two individually true statements into a specific synergy that is not well established:

1. Bulky biaryl monophosphines (SPhos, RuPhos, XPhos) are highly effective for coupling of electron-rich aryl bromides — this is well-documented (Buchwald et al.).
2. Cs₂CO₃ is a mild, poorly soluble carbonate base used in many Pd-catalysed couplings.

However, the specific pairing of Cs₂CO₃ with bulky monophosphines is not the basis of the established efficacy. The phosphines promote oxidative addition through steric and electronic effects on Pd that are base-independent. In practice, K₃PO₄ and K₂CO₃ are more commonly recommended alongside these ligands in optimised Suzuki protocols. Cs₂CO₃ can be used and does work, but it is not specifically the co-activator of the phosphine. Presenting this as a documented "synergy" overstates the evidence and may misdirect the base-screening design toward Cs₂CO₃ over more effective base choices.

**Impact:** If Cs₂CO₃ is included at the expense of a stronger base (K₃PO₄) partly because of this claimed synergy, the base panel may be suboptimal.

### 3c. CsF described as "poorly compatible with phosphine-free Pd(OAc)₂"

**MAJOR — claim appears to be incorrect**

CsF is a standard base in Suzuki-Miyaura couplings and has been used with Pd(OAc)₂ in numerous published procedures, including ligand-free systems. CsF activates boronic acids efficiently by generating the tetracoordinate boronate [ArB(OH)₃]⁻ that undergoes transmetallation. Its mild, non-hygroscopic character makes it attractive precisely for simple Pd(OAc)₂ systems. The fluoride anion does not deactivate Pd(OAc)₂ in the way that, for example, strongly coordinating anions or reducing agents can. There is no well-documented literature precedent for describing this combination as "poorly compatible."

**Impact:** If CsF is excluded from or scored poorly in the base panel on this basis, the panel may miss a productive reagent option. The exclusion criterion should be replaced with an experimentally grounded one or CsF should be included.

### 3d. UPLC internal standard 1,3,5-trimethoxybenzene — co-elution risk with 4-methoxybiphenyl

**VERIFIED CORRECT (choice is reasonable; co-elution is unlikely)**

Under standard reversed-phase C18 UPLC conditions, 4-methoxybiphenyl (two phenyl rings plus one methoxy; estimated logP ≈ 3.3–3.6) is substantially more lipophilic than 1,3,5-trimethoxybenzene (one ring with three methoxy groups; estimated logP ≈ 1.8–2.0). The product would elute considerably later than the internal standard. Co-elution under typical aqueous acetonitrile or methanol gradients is not expected. The choice of 1,3,5-trimethoxybenzene as internal standard is reasonable.

---

## Check 4 — Arithmetic

### 4a. 4 × 4 × 3 = 48

**VERIFIED CORRECT**

### 4b. 48 × 2 = 96 (one plate)

**VERIFIED CORRECT**

### 4c. CCD run count: 2³ + 6 axial + 6 centre = 20

**VERIFIED CORRECT**

A face-centred central composite design (CCD) in 3 factors has: 2³ = 8 factorial corner points; 2 × 3 = 6 face-centred axial points (one on each face of the cube, at α = 1); plus centre replicates. With 6 centre replicates: 8 + 6 + 6 = 20 runs. The stated total of 20 is correct.

### 4d. "40 unique tested combinations": see Check 1b above — VERIFIED CORRECT.

---

## Check 5 — Product Stability Used to Eliminate Time as a Variable

**MAJOR**

The claim reportedly made is: "no known product degradation pathway for 4-methoxybiphenyl under these conditions" — and this claim is used to justify fixing reaction time at 16 h and removing it from the design space.

This reasoning contains a logical error. Product stability under the reaction conditions means the product does not decompose after it forms; it does not mean that all catalyst/base/solvent combinations reach comparable conversion at 16 h. The relevant question for time as a variable is whether yield continues to change with time, i.e., whether the reaction has reached a plateau under all conditions. For conditions involving sluggish catalysts, bulky substrates, or bases that activate boronic acid slowly, 16 h may not be sufficient. Some conditions might show 40% yield at 16 h and 85% yield at 24 h.

The statement about product stability addresses degradation kinetics, not forward-reaction kinetics. Eliminating time as a variable requires showing either (a) all conditions give maximum yield by 16 h, or (b) time-course data from at least representative conditions, neither of which is a property of the product alone. Fixing time at 16 h may introduce a confound where slow conditions are underscored relative to fast ones, misranking the catalyst and base panels.

---

## Check 6 — Plate Map Label Convention

See Check 2a (CRITICAL — E = Cat-C, not Cat-A) and Check 2b (MAJOR — ambiguous "A-X" key) above. Both findings originate in the plate map section and are reported there in full.

---

## Check 7 — Bayesian Optimisation Efficiency Claim

**MAJOR — lower bound arithmetic is inconsistent with the stated parameters**

The claim reportedly states: BO would need "34–55 experiments in 4–6 sequential rounds," with the breakdown "10–15 seed + 4–5 rounds × 8 experiments per round."

Checking the arithmetic:

| Bound | Seed | Rounds | Per round | Total |
|-------|------|--------|-----------|-------|
| Minimum (as stated) | 10 | 4 | 8 | 10 + 32 = **42** |
| Maximum (as stated) | 15 | 5 | 8 | 15 + 40 = **55** |

The stated lower bound is **34**, but the formula gives **42**. To obtain 34 from the described components:

- 10 seeds + 3 rounds × 8 = 34 — but this requires 3 minimum rounds, not 4.
- Alternatively, 10 seeds + 4 rounds × 6 = 34 — but this requires 6 per round, not 8.

No combination of the stated parameters (seed 10–15, rounds 4–5, 8 per round) yields 34. The lower bound appears to derive from a different set of parameters than those written — possibly an earlier draft with 3–5 rounds instead of 4–5, or 6 experiments per round instead of 8, that was not updated when the other numbers changed.

**Impact:** The comparison between HTE and BO is used to justify the campaign design. An underestimated BO lower bound makes BO appear more efficient than the numbers actually support, potentially affecting the strategic framing of the work. The stated range should be corrected to 42–55 (using 4–5 rounds) or the round count should be revised to 3–5 (giving 34–55).

---

## Summary Table

| Check | Severity | Finding |
|-------|----------|---------|
| 0 | MAJOR | No artifact written; phase exists only in conversation transcript |
| 1a | VERIFIED CORRECT | 4×4×3=48; 48×2=96; plate fills correctly |
| 1b | VERIFIED CORRECT | 16 wells / 8 pairs / 40 combinations are mutually consistent |
| 2a | CRITICAL | Row E assigned Cat-C in rep-2; should be Cat-A — systematic well misassignment |
| 2b | MAJOR | "A-X / B-X" key ambiguous across row, block, and catalyst namespaces |
| 3a | VERIFIED CORRECT | 4-bromoanisole EDG description and oxidative-addition comparison are accurate |
| 3b | MAJOR | Cs₂CO₃ + bulky phosphine "synergy" overstated; two true statements, not a documented pairing |
| 3c | MAJOR | CsF described as poorly compatible with Pd(OAc)₂; claim appears incorrect — CsF is routinely used with Pd(OAc)₂ |
| 3d | VERIFIED CORRECT | 1,3,5-trimethoxybenzene IS is reasonable; no co-elution with product expected |
| 4c | VERIFIED CORRECT | CCD 20-run count correct: 8+6+6=20 |
| 5 | MAJOR | Product stability used to eliminate time variable; conflates degradation with reaction-progress kinetics |
| 6 | (see 2a, 2b) | Plate map errors fully reported under Check 2 |
| 7 | MAJOR | BO lower bound 34 inconsistent with stated parameters; formula gives 42, not 34 |

**CRITICAL findings: 1**  
**MAJOR findings: 6**  
**VERIFIED CORRECT: 5**
