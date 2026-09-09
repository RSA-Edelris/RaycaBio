# Independent Audit: lorlatinib_synthesis_critique.md

**Auditor:** Independent verification agent (Claude Sonnet 4.6)  
**Date of audit:** 2026-09-09  
**File audited:** `/home/ubuntu/rayca-sessions/949a49f6-eec2-4165-b118-f7ef228e18a9-aef5ffddf790/lorlatinib_synthesis_critique.md`  
**Audit scope:** Verification section (confidence table, unconfirmed-claims list, what-would-invalidate list, GitHub push audit block); cross-check of specific numerical values in the step-by-step critique, stereochemistry, protecting-group strategy, safety/scale table, and de-risking experiments; all items in the stated checklist (index errors, identifier confusion, single-data-point rules, "confirmed" vs "plausible" classification, reversed positional claims, internal contradictions, GitHub audit block validity).

---

## Summary classification

| Severity | Count |
|---|---|
| CRITICAL | 2 |
| MAJOR | 7 |
| VERIFIED CORRECT | 14 |

---

## CRITICAL findings

---

### CRITICAL-1: Concentration label in the volume/scale calculation is wrong by a factor of two

**Location:** Step 6 (line: "0.005 M in DMF = 200 L per kg substrate") and Purification section step 1 (line: "At 0.005 M and 40% yield, 1 kg of precursor in 200 L DMF gives ~350 g macrolactam before purification")

**Exact text checked (Step 6):**
> "0.005 M in DMF = 200 L per kg substrate. Above 100 g, reactor volume is the rate-limiting physical constraint."

**Exact text checked (Purification):**
> "At 0.005 M and 40% yield, 1 kg of precursor in 200 L DMF gives ~350 g macrolactam before purification."

**Arithmetic verification (full):**

The open-chain macrolactamisation precursor has a minimum MW equal to lorlatinib (406.4 g/mol) plus the water lost in amide-bond formation (+18.0 g/mol) plus the Boc protecting group on the C-7 amine (+100.1 g/mol), giving approximately 524.5 g/mol for the Boc-protected linear precursor. Even without any protecting groups, the ring-opened analogue is 424.4 g/mol. These bounds bracket every realistic precursor.

| Precursor MW (g/mol) | Moles per kg | Volume at 0.005 M | Volume at 0.01 M |
|---|---|---|---|
| 406.4 (lorlatinib, lower bound) | 2.46 | 492 L | 246 L |
| 424.4 (ring-open, no PG) | 2.36 | 471 L | 236 L |
| 524.5 (Boc-protected) | 1.91 | 381 L | 191 L |

The figure of 200 L per kg is consistent with 0.01 M and a Boc-protected precursor (~191 L), not with 0.005 M at any realistic precursor MW. For 200 L to hold at 0.005 M, the precursor would need to have MW = 1000 g/mol — roughly double the maximum plausible value.

**Cross-check with the "~350 g macrolactam" yield claim:**

At 0.005 M in 200 L: n_substrate = 0.005 × 200 = 1.00 mol. At 40% yield: 1.00 × 0.40 × 406.4 = 163 g macrolactam — far short of the stated 350 g.

At 0.01 M in 200 L: n_substrate = 0.01 × 200 = 2.00 mol. At 40% yield: 2.00 × 0.40 × 406.4 = 325 g ≈ "~350 g" (7% below, within rounding). This is the internally consistent calculation.

**Conclusion:** The 200 L and ~350 g figures are arithmetically consistent with 0.01 M, not 0.005 M. The document has attached the wrong concentration label (0.005 M) to a volume that was almost certainly calculated at 0.01 M. The stated concentration and volume cannot both be correct simultaneously for any plausible precursor.

**Why this is CRITICAL:** The volume calculation is the explicit justification for when reactor volume becomes a practical constraint. The document says "Above 100 g, reactor volume is the rate-limiting physical constraint." If the correct concentration is 0.01 M (not 0.005 M), then at 100 g the volume is ~19-25 L (not 38-49 L), and at 0.005 M (if one follows the stated recommended low-end concentration) the volume is roughly double what the document implies. A process chemist relying on this number to size a reactor will be wrong by approximately a factor of two at the critical 0.005 M operating point.

---

### CRITICAL-2: Experiment 3 de-risking solvent does not match the synthesis step it de-risks

**Location:** Step 4 vs Experiment 3

**Step 4 exact text:**
> "SNAr route (Cs₂CO₃, DMF, 80–100°C): C-7 amine must be Boc-protected before this step"

**Experiment 3 exact text:**
> "Test SNAr (Cs₂CO₃, DMSO, 80°C) and Mitsunobu (PPh₃/DIAD, THF, RT) on the fluoroaryl fragment + C-10 alcohol, with C-7 amine Boc-protected and unprotected in parallel."

**What was checked:** The solvent in the recommended synthesis (Step 4) is DMF; the solvent in the de-risking experiment (Experiment 3) is DMSO. These are different solvents with different polarity and coordinating ability. SNAr selectivity (O- vs N-arylation ratio) is solvent-dependent: DMF and DMSO can give meaningfully different results for nucleophilic aromatic substitution.

**Why this is CRITICAL:** Experiment 3 is explicitly the study that generates the Go/Abandon decision for O-arylation selectivity ("Go: ≥70% O-arylation, <5% N-arylation with Boc protection"). If the experiment passes in DMSO but the synthesis uses DMF (or vice versa), the data does not validate the synthesis step. A Go decision based on this experiment would provide false assurance. The de-risking experiment as written cannot confirm the safety of Step 4 as written. At minimum, both solvents must be tested; at best, Experiment 3 should be corrected to use DMF to match Step 4.

---

## MAJOR findings

---

### MAJOR-1: Step 5 epimerisation range and observable SFC ratio range are mutually inconsistent

**Location:** Step 5

**Exact text:**
> "HATU/DIPEA (3 eq), DMF, 0°C gives 5–20% (S)-epimer depending on activation time. Observable: single LCMS peak at correct mass but two peaks by chiral SFC (~88:12 to 95:5 ratio)."

**Check:** The stated SFC ratio range is 88:12 to 95:5. Converting to (S)-epimer percentage:
- 95:5 major:minor → 5% (S)-epimer
- 88:12 major:minor → 12% (S)-epimer

The SFC ratio range therefore covers 5–12% (S)-epimer. The stated text range is 5–20%. The upper end of the text range (20% S-epimer) would appear as an ~80:20 SFC ratio, which is not mentioned. The observable SFC data the document describes can only confirm the lower 60% of the claimed range. A chemist using the 88:12 observable as the "worst case to look for" would miss epimerisation events in the 12–20% zone — the operationally most damaging zone.

**This is a MAJOR internal inconsistency.** The document states a wider quantitative range (5–20%) in one clause and then immediately gives an example observable range (88:12 to 95:5) that only covers the bottom portion of that range without comment.

---

### MAJOR-2: Step 6 and Stereochemistry section state different upper bounds for macrolactamisation epimerisation

**Location:** Step 6 vs Stereochemistry section

**Step 6 exact text:**
> "Expect 5–15% (S)-epimer even at optimised conditions."

**Stereochemistry section exact text:**
> "Step 6 (macrolactamisation): second highest risk; ~5–10% erosion expected under best basic conditions"

**Check:** The upper bound stated in Step 6 is 15%. The upper bound in the Stereochemistry summary is 10%. These differ by 5 percentage points in the most operationally significant direction (overestimating safety). A chemist who reads only the Stereochemistry section (a natural executive-summary section) would plan for a maximum 10% loss, whereas the primary analysis (Step 6) warns of up to 15%. At ee requirements of ≥98%, the difference between a 10% and 15% epimer ceiling is the difference between needing one SFC pass vs two.

---

### MAJOR-3: NMP presented as an alternative to DMF without stating that its ICH limit is stricter, not looser

**Location:** Step 6 and Safety/scale table

**Step 6 exact text:**
> "ICH Class 2 limits on DMF (880 ppm) require rigorous removal; consider NMP (530 ppm) as alternative but re-optimise."

**Safety table exact text:**
> "DMF and NMP (ICH Class 2) | 880 and 530 ppm limits; reproductive toxicants"

**Check:** DMF ICH Q3C(R8) Class 2 limit: 880 ppm. NMP ICH Q3C(R8) Class 2 limit: 530 ppm. The NMP limit is 40% lower (more restrictive), meaning residual NMP is harder to bring within specification than residual DMF. The framing "consider NMP as alternative" implies NMP simplifies the regulatory problem of DMF removal; the opposite is true from an ICH limit standpoint. While NMP may have process chemistry advantages (boiling point, selectivity), the text as written gives a reader no indication that switching to NMP makes the residual solvent analytical challenge more difficult, not less. The document notes both numbers but does not comment on the direction of the comparison.

---

### MAJOR-4: TPPO removal difficulty rated "Confirmed" on the basis of community knowledge only

**Location:** Verification table, claim row 7

**Exact text:**
> "TPPO removal difficulty above 50 g | Confirmed (process chemistry community knowledge) | Well-documented in process chemistry literature; TPPO log P and polarity make it chromatographically persistent with many polar drug-like products"

**Check:** Every other "Confirmed" entry in the Verification table cites a specific primary document: IARC Monograph, ACGIH TLV, ICH Q3C(R8) Table 2, ICH Q3D Table A.2.1. This entry uses "process chemistry community knowledge" and "well-documented in process chemistry literature" without naming the literature. That basis supports at most "Plausible" by the standards applied to the other rows in the same table. The entry is therefore inconsistently classified relative to its peers.

The substantive claim (TPPO is chromatographically persistent at scale) is chemically reasonable and widely accepted, but the confidence label "Confirmed" is inflated relative to the evidence basis stated.

---

### MAJOR-5: IARC citation for "Group 2A" classification of methylhydrazine uses an anachronistic volume number

**Location:** Verification table, claim row 1

**Exact text:**
> "Methylhydrazine IARC Group 2A, TLV 0.01 ppm | Confirmed | IARC Monograph Vol. 4 / ACGIH TLV documentation"

**Check:** IARC Monograph Volume 4 was published in 1974 (title: "Some Aromatic Amines, Hydrazine and Related Substances, N-Nitroso Compounds and Miscellaneous Alkylating Agents"). The IARC carcinogenicity classification system using Group 1 / Group 2A / Group 2B / Group 3 was not formalised until IARC Supplement 4 (1982) and was systematically applied to earlier evaluations in IARC Supplement 7 (1987). Volume 4 (1974) used qualitative language from the pre-group era, not the Group 2A designation. Citing Volume 4 as the source of the Group 2A classification is therefore anachronistic: the Group 2A label was assigned in a later document (Supplement 7 or a subsequent re-evaluation), not in Volume 4 itself.

The TLV 0.01 ppm component of the claim is supported by ACGIH documentation and is not affected by this issue.

**Why this is MAJOR:** The Verification table marks this claim "Confirmed." If the cited source (Vol. 4) does not contain the Group 2A classification by that name, the confirmation claim is inaccurate. The correct Group 2A citation should reference IARC Supplement 7 (1987) or the relevant subsequent monograph update. This is not a trivial bibliographic issue: the distinction between Group 2A ("probably carcinogenic") and Group 2B ("possibly carcinogenic") affects what containment tiers and regulatory controls are triggered.

---

### MAJOR-6: "What would invalidate" drops a critical qualifier from Experiment 1 Go criterion

**Location:** Verification section, "What would invalidate conclusions"

**Experiment 1 Go criterion (De-risking section):**
> "Go: ≥35% monomer yield at ≤0.01 M under at least one condition."

**What would invalidate (Verification section):**
> "If the macrolactamisation model study (Experiment 1) shows ≥35% monomer yield: the step-6 concerns are addressable and the route proceeds."

**Check:** The Experiment 1 Go criterion requires ≥35% yield **at ≤0.01 M**. The Verification section rephrases this as "≥35% monomer yield" with no concentration qualifier. These are not equivalent. A yield of ≥35% at 0.05 M (the highest screening concentration in Experiment 1, and a concentration the main text identifies as oligomerisation-prone) would satisfy the Verification section's phrasing but would NOT satisfy Experiment 1's Go criterion and would NOT validate the route at practical concentrations. A decision-maker reading only the Verification section as a summary would reach the wrong conclusion about what constitutes a passing result.

---

### MAJOR-7: Step 1 regioisomer ratio stated as established fact in body; flagged as unconfirmed literature analogy in Verification — two different confidence levels for the same claim

**Location:** Step 1 vs Verification "Claims not independently confirmed"

**Step 1 exact text:**
> "Typical ratio 3:1 to 6:1 in favour of 1-methyl isomer; varies with pH and solvent."

**Verification table:**
> "N-methylation regioisomer ratio 3:1 to 6:1 | Plausible range | Consistent with general pyrazole N-alkylation literature; exact ratio substrate-dependent and not confirmed on this specific substrate"

**Unconfirmed claims list:**
> "The exact regioisomer ratio for Step 1 N-methylation on this specific pyrazole substrate has not been confirmed by experiment in this session. The 3:1 to 6:1 range is a literature analogy."

**Check:** The step-by-step text presents "3:1 to 6:1" as a "typical ratio" without any qualification — language that implies documented experimental data. The Verification section correctly characterises it as a literature analogy not confirmed on this substrate. The two sections present materially different confidence levels for the same quantitative claim within the same document. A reader who reads only the step-by-step critique (the primary working section) will treat this as a known datum, not an analogy. This is not a matter of editorial style: the regioisomer ratio directly determines whether Step 1 is a purification problem (3:1 → manageable) or a synthesis bottleneck (worse than 3:1 → must redesign).

---

## VERIFIED CORRECT

The following claims were checked and held up against primary sources, internal arithmetic, or universally accepted chemical knowledge.

---

### VC-1: Lorlatinib molecular formula and MW

**Text:** "Formula: C₂₁H₁₉FN₆O₂ | MW: 406.4"  
**Check:** Lorlatinib (PF-06463922, CHEMBL3286830) molecular formula C₂₁H₁₉FN₆O₂, MW 406.43. The formula and rounded MW are correct. The IUPAC name in the document is the accepted systematic name for lorlatinib. Consistent with published Pfizer compound data and the IUPAC name embedded in the document.

---

### VC-2: Single stereocentre at C-10 (R), consistent throughout document

**Text (header):** "Stereocentres: 1 (C-10, R)"  
**Text (IUPAC):** "(10R)-..." at start of IUPAC name  
**Check:** The (10R) designation appears at the start of the IUPAC name. The Structural context, Stereochemistry section, and all step references (Steps 3, 5, 6) consistently use C-10 (R) for the single stereocentre. No contradictory stereocentre numbering was found anywhere in the document. Internal consistency confirmed throughout all seven sections.

---

### VC-3: DMF ICH Q3C Class 2 limit, 880 ppm

**Text:** "ICH Class 2 limits on DMF (880 ppm)" and Verification: "DMF ICH Class 2, 880 ppm limit | Confirmed | ICH Q3C(R8) Table 2"  
**Check:** ICH Q3C(R8) Table 2 lists DMF (N,N-dimethylformamide) as a Class 2 solvent with PDE = 8.8 mg/day. At 10 g/day maximum drug product intake, this gives a concentration limit of 880 ppm. The value 880 ppm is correct.

---

### VC-4: NMP ICH Q3C Class 2 limit, 530 ppm

**Text (safety table):** "DMF and NMP (ICH Class 2) | 880 and 530 ppm limits"  
**Check:** ICH Q3C(R8) lists 1-methyl-2-pyrrolidinone (NMP) as a Class 2 solvent with PDE = 5.3 mg/day, giving a concentration limit of 530 ppm at the standard 10 g/day intake. The value 530 ppm is correct. (Note: the implication that NMP is a simpler regulatory alternative to DMF is MAJOR-3 above; the numerical value itself is correct.)

---

### VC-5: Pd ICH Q3D oral PDE, 100 μg/day

**Text:** "Pd residues | ICH Q3D oral limit 100 μg/day" and Verification: "Pd ICH Q3D oral limit 100 μg/day | Confirmed | ICH Q3D Table A.2.1 (oral route, permitted daily exposure)"  
**Check:** ICH Q3D Table A.2.1 specifies the oral PDE for palladium as 100 μg/day. This is correct.

---

### VC-6: Mitsunobu reaction inverts configuration at C-10

**Text (Step 4):** "Mitsunobu route (PPh₃/DIAD): Configuration at C-10 inverts; verify handedness assignment before use."  
**Check:** The Mitsunobu reaction proceeds via an SN2 mechanism at the alcohol carbon with inversion of configuration. This is a foundational principle of the reaction, established by Mitsunobu and confirmed in thousands of synthetic examples. The configuration-inversion warning is correct.

---

### VC-7: DIPEA conjugate acid pKa ~11, collidine ~7

**Text (Step 5):** "Replace DIPEA with 2,4,6-collidine (pKa ~7 vs ~11)"  
**Check:** The conjugate acid of DIPEA (N,N-diisopropylethylamine) has pKa ≈ 11.4 in MeCN/water systems; "~11" is a correct approximation. 2,4,6-Collidine (2,4,6-trimethylpyridine) has pKa ≈ 7.3; "~7" is a correct approximation. The relative basicity difference stated is directionally and numerically correct.

---

### VC-8: Commit hash format — 40 valid hexadecimal characters

**Text:** `` `6194a7247832b612812ca65d3771af8eb619c31d` ``  
**Check:** Character count = 40. Character set: 6, 1, 9, 4, a, 7, 2, 4, 7, 8, 3, 2, b, 6, 1, 2, 8, 1, 2, c, a, 6, 5, d, 3, 7, 7, 1, a, f, 8, e, b, 6, 1, 9, c, 3, 1, d — all in the range 0–9 and a–f. The hash is a valid SHA-1 format (40 lowercase hex characters). No non-hex characters are present.

---

### VC-9: File count in GitHub push audit matches listed files

**Text:** "Files committed: 4 (lorlatinib_synthesis_critique.md, run.json, study README.md, STUDIES.md)"  
**Check:** Four distinct file names are listed: (1) lorlatinib_synthesis_critique.md, (2) run.json, (3) README.md (study-level), (4) STUDIES.md. The count "4" matches the enumeration. No counting error.

---

### VC-10: Step 6 oligomerisation threshold is above the recommended concentration range

**Text (Step 6):** "Failure mode 1 — oligomerisation (most likely if concentration > 0.02 M)" vs recommended "HATU (1.1 eq), DIPEA (3 eq), DMF, 0.005–0.01 M"  
**Check:** 0.005 M and 0.01 M are both below 0.02 M. The recommended operating window is safely below the identified problematic threshold. Internally consistent.

---

### VC-11: Epimerisation claims correctly classified as "Plausible" (not "Confirmed") in the Verification table

**Text (Verification table):** "Epimerisation at C-10 under HATU/DIPEA: 5–20% (S)-epimer | Plausible | ..."  
**Check:** The document does not mark this "Confirmed" and explicitly lists it in the "Claims not independently confirmed" section. The classification as Plausible accurately reflects that the value is a literature analogy, not a measurement on this substrate. The confidence level is not inflated. This is one of the two critical-path numbers (the other being macrolactamisation yield), and both are correctly characterised as unconfirmed estimates.

---

### VC-12: Macrolactamisation yield 40–60% correctly classified as "Plausible"

**Text (Verification table):** "HATU/DIPEA macrolactamisation at 0.005–0.01 M, 40–60% yield | Plausible | ..."  
**Check:** Correctly marked Plausible. Correctly listed in the unconfirmed claims. Experiment 1 is specifically designed to generate this number. No false confidence is introduced by the classification.

---

### VC-13: Step 5 SFC ratio range numerically consistent with the lower portion of the stated epimerisation range

**Text (Step 5):** "two peaks by chiral SFC (~88:12 to 95:5 ratio)"  
**Check:** 95:5 → 5% (S)-epimer; 88:12 → 12% (S)-epimer. Both values fall within the stated 5–20% range. (Note: MAJOR-1 addresses the separate problem that the SFC range given does not cover the upper portion of the 5–20% range. This VC entry confirms only that the SFC numbers given are internally consistent with the lower half of the range.)

---

### VC-14: Methylhydrazine TLV 0.01 ppm (ACGIH component of the claim)

**Text:** "Methylhydrazine — probable carcinogen (IARC Group 2A), TLV 0.01 ppm"  
**Check (TLV only):** ACGIH assigns methylhydrazine (CAS 60-34-4) a TLV-TWA of 0.01 ppm (skin notation). This value is correct. (Note: the IARC Group 2A citation to "Monograph Vol. 4" is addressed as MAJOR-5 above; that finding applies to the IARC citation component only, not to the TLV value.)

---

## Appendix: Arithmetic summary for CRITICAL-1

For reference, the document's two claimed values and the single concentration that is consistent with each:

| Claimed quantity | Stated concentration | Volume implied by arithmetic | Concentration implied if volume is correct |
|---|---|---|---|
| 200 L per kg substrate (MW ~524 g/mol Boc-precursor) | 0.005 M | 381 L at 0.005 M | **~0.0095 M ≈ 0.01 M** |
| ~350 g macrolactam from 200 L at 40% yield | 0.005 M | 163 g at 0.005 M in 200 L | **~0.01 M gives ~325 g** |

Both figures (200 L and 350 g) are consistent with 0.01 M and a realistic precursor MW. The document labels them as being at 0.005 M; that label is wrong by approximately a factor of two.
