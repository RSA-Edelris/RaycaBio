# Synthesis Critique: Lorlatinib (CHEMBL3286830)

**Date:** 2026-09-09  
**Compound:** (10R)-7-amino-12-fluoro-2,10,16-trimethyl-15-oxo-10,15,16,17-tetrahydro-2H-8,4-(metheno)pyrazolo[4,3-h][2,5,11]benzoxadiazacyclotetradecine-3-carbonitrile  
**CHEMBL ID:** CHEMBL3286830 (PF-06463922, lorlatinib)  
**MW:** 406.4 | **Formula:** C₂₁H₁₉FN₆O₂ | **Stereocentres:** 1 (C-10, R)  
**Route provenance:** Published Pfizer discovery synthesis (Johnson et al., *J. Med. Chem.* 2014) and process-chemistry publications. No session-specific route was found; the public compound was used. Every number and assignment below refers to CHEMBL3286830.

---

## Structural context

Key features: bridged 12-membered macrolactam, fused pyrazolopyrimidine, nitrile at C-3, primary amine at C-7, aryl fluorine at C-12, N-methyl at N-16, aryl ether oxygen in the macrocycle chain. One defined stereocentre at C-10 (R): bears CH₃, H, O-aryl (macrocycle), and C-17 (CH₂ adjacent to N-16).

---

## Synthesis stages critiqued

1. Pyrazole-carbonitrile fragment synthesis
2. Pyrazolopyrimidine bicyclisation and C-7 amino installation
3. Stereocentre-bearing chain fragment preparation
4. Linear coupling to open-chain macrolactamisation precursor
5. Macrolactamisation → deprotection → final purification

---

## Step-by-step critique

### Step 1 — Methylhydrazine + cyanoacetate cyclisation → 5-amino-1-methyl-1H-pyrazole-3-carbonitrile

**Most likely failure mode:** Regioisomeric N-methylation giving the 2-methyl isomer alongside the desired 1-methyl product. Typical ratio 3:1 to 6:1 in favour of 1-methyl isomer; varies with pH and solvent. Observable: two TLC spots of nearly identical Rf; ¹H NMR N-Me singlet shifts ~0.3 ppm between isomers. Separation by chromatography or recrystallisation required before proceeding.

**Safety note:** Methylhydrazine — probable carcinogen (IARC Group 2A), TLV 0.01 ppm, acutely toxic vapour. Contained handling mandatory above ~10 g; scrubbed exhaust required. Stockpile fragment at multi-gram scale in a single campaign.

---

### Step 2 — Condensation to pyrazolopyrimidine / C-7 amino installation

**Most likely failure mode:** The aminopyrazole is a 1,3-dinucleophile; incorrect regiochemistry at N-1 vs N-2 attack gives ring regioisomers. Observable: gummy residue resisting crystallisation; two LCMS products with identical mass and similar retention time. Run condensation in glacial AcOH at controlled temperature (80°C → cool). If using Buchwald amination to install C-7 amine, the C-3 nitrile may coordinate to Pd and cause catalyst poisoning — test on a model substrate lacking the nitrile before committing. If C-7 amine is introduced via nitro reduction, watch for incomplete reduction to hydroxylamine (difficult to remove chromatographically).

---

### Step 3 — Stereocentre-bearing fragment preparation (C-10, R)

**Substitution at C-10:** CH₃, H, O-aryl (macrocycle), C-17. C-10 is alpha to an ether oxygen, not a carbonyl, so the thermodynamic epimerisation driving force is lower than for a typical amino acid alpha carbon; nevertheless all downstream coupling steps are risks.

**Preferred route:** Commercial Boc-(R)-alanine or Boc-(R)-N-Me-alanine (chiral pool). Verify lot ee ≥ 99.5% by chiral SFC before use — commercial lots occasionally arrive at 98–99% ee.

**Alternative:** Asymmetric hydrogenation of alpha-dehydroamino acid precursor (Rh or Ru chiral catalyst). Typical ee 96–99.5%; requires upgrade by crystallisation or SFC.

**Epimerisation risk at this stage:** Low if chiral pool option A is used and fragment stored at –20°C as Boc salt.

---

### Step 4 — Aryl ether formation (O-arylation, C-10 oxygen to fluoroaryl ring)

**SNAr route (Cs₂CO₃, DMF, 80–100°C):** C-7 amine must be Boc-protected before this step; unprotected amine competes as nucleophile. Failure: two LCMS products at same or +14 Da (N-arylation byproduct, more polar). If conversion stalls below 80%, do not increase temperature above ~120°C — Boc cleavage + simultaneous N-arylation becomes catastrophic.

**Mitsunobu route (PPh₃/DIAD):** Configuration at C-10 inverts; verify handedness assignment before use. Critical operational problem: TPPO produced in equimolar quantity; co-precipitates with polar products and is very difficult to remove above 50 g. Avoid this route beyond discovery scale. DIAD: exothermic oxidant, slow addition and temperature monitoring (<15°C addition) mandatory above 50 g.

---

### Step 5 — Linear amide coupling to open-chain macrolactamisation precursor

**Most likely failure mode:** Epimerisation at C-10 during HATU activation. HATU/DIPEA (3 eq), DMF, 0°C gives 5–20% (S)-epimer depending on activation time. Observable: single LCMS peak at correct mass but two peaks by chiral SFC (~88:12 to 95:5 ratio). Standard RP-HPLC will not resolve the epimers.

**Mitigation:** Replace DIPEA with 2,4,6-collidine (pKa ~7 vs ~11); reduces but does not eliminate epimerisation. Alternatively use PyOxim or T3P as activating reagent. Run gram-scale model coupling and check SFC before committing to full linear assembly.

---

### Step 6 — Macrolactamisation (critical step; will determine programme success)

**Recommended conditions:** HATU (1.1 eq), DIPEA (3 eq), DMF, 0.005–0.01 M, 0°C, syringe-pump addition over 2 h, warm to RT. Expected yield: 40–60%.

**Failure mode 1 — oligomerisation (most likely if concentration > 0.02 M):** Bimolecular reaction competes with intramolecular closure. Observable: broad featureless LCMS baseline, n=2 and n=3 oligomer peaks, turbid or gummy reaction mixture on concentration, isolated yield <15%. Fix: lower concentration, inverse addition of substrate into coupling reagent.

**Failure mode 2 — epimerisation at C-10 during ring closure:** Activated ester intermediate allows proton abstraction at C-10 before ring closure. Expect 5–15% (S)-epimer even at optimised conditions. Not visible by standard LCMS; requires chiral SFC on every lot.

**Failure mode 3 — solvent volume at scale:** 0.005 M in DMF = 200 L per kg substrate. Above 100 g, reactor volume is the rate-limiting physical constraint. ICH Class 2 limits on DMF (880 ppm) require rigorous removal; consider NMP (530 ppm) as alternative but re-optimise. Both solvents carry reproductive toxicity classifications.

---

### Step 7 — Global deprotection (C-7 Boc removal, TFA/DCM or HCl/dioxane)

**Most likely failure mode:** Liberation of the C-7 free base as a poorly soluble TFA salt, causing precipitation during the reaction. Operational complication rather than a chemical failure. Free base recovery requires basification with dilute NH₃ or K₂CO₃ and careful extraction. Heating to 40°C in neat TFA resolves incomplete deprotection if the amine is buried. All other functional groups (macrolactam, nitrile, aryl ether, pyrazole) are stable to TFA. If Cbz is used instead and H₂/Pd-C deprotection is performed, verify macrolactam ring stability to reductive conditions on a model first.

---

## Stereochemistry — full account

**Number of stereocentres:** One. C-10, (R).

**How set:** Chiral pool (preferred) — (R)-alanine or (R)-N-Me-alanine derivative introduced at Step 3. No asymmetric synthesis required; ee dictated by commercial material quality. Alternative: asymmetric hydrogenation (96–99.5% ee, requires upgrade).

**Steps where epimerisation risk is real:**
- Step 5 (linear amide coupling): highest risk; HATU-mediated activation, expect 5–20% (S) under standard conditions
- Step 6 (macrolactamisation): second highest risk; ~5–10% erosion expected under best basic conditions
- Any step using NaH, LiHMDS, or strong base within two bonds of C-10: avoid entirely

**Confirmation of configuration:** Measure ee by chiral SFC (Chiralpak IA-3 or Lux i-Cellulose-5, CO₂/MeOH gradient) at open-chain precursor stage and again on macrolactam before deprotection. Do not rely on optical rotation alone — signal-to-noise is poor and the epimer may have similar specific rotation.

**Fallback if poor selectivity:** Preparative SFC on Chiralpak IA; ~2–5 kg/day per instrument is feasible and is the standard pharmaceutical fallback. Adds ~$500–1000/g at early clinical scale. If macrolactamisation consistently gives <90:10 dr, redesign the linear precursor to prevent base access to C-10 during activation (pre-formed NHS ester, ring-close under neutral conditions).

---

## Protecting group strategy

**The only group requiring routine protection is the C-7 primary amine.**

The C-7 amine must be protected during: O-arylation (competing N-arylation), any HATU coupling (competing acylation), and any electrophilic step.

**Recommended PG: Boc**
- Orthogonal to Cs₂CO₃/DMF O-arylation (stable to 100°C) ✓
- Orthogonal to HATU/DIPEA coupling ✓
- Orthogonal to Pd/Buchwald conditions (≤100°C) ✓
- Removed cleanly with TFA/DCM in one step; does not affect macrolactam, nitrile, aryl ether, or pyrazole ✓
- NOT stable to: strong acid (HCl/dioxane), >120°C in DMF, Lewis acids (AlCl₃, BBr₃)

**Alternative PG: Cbz** — removed by H₂/Pd; orthogonal to Boc if a second amine requires differentiation. Not recommended here because H₂/Pd late in the sequence requires checking all functional groups for sensitivity.

**Is a protecting-group-free route realistic?** Marginally possible if the C-7 amine is installed last by reduction of a nitro group after macrolactamisation. The nitro group also activates the ring toward SNAr (useful). Risk: late-stage aromatic nitro reduction (Fe/AcOH preferred; H₂/Pd feasible but verify macrolactam stability first) exposes the full assembled structure to reductive conditions. Recommended as a second-generation redesign after first-generation Boc route has delivered material for early biology — not the place to start.

---

## Safety and scale concerns

| Concern | Agent | When it becomes a real constraint |
|---|---|---|
| Methylhydrazine | Probable carcinogen, TLV 0.01 ppm | >10 g: contained reactor + scrubber; >100 g: specialist containment |
| DIAD/DEAD (Mitsunobu) | Exothermic diazodicarboxylate; irritant | >50 g: slow addition + T monitoring mandatory; avoid at kg scale |
| TPPO (Mitsunobu byproduct) | Chromatographically inseparable | >50 g: throughput-limiting; switch to SNAr before scale-up |
| HATU macrolactamisation at high dilution | 200 L DMF per kg substrate | >100 g: reactor volume dominates; pilot plant needed above ~0.5 kg |
| DMF and NMP (ICH Class 2) | 880 and 530 ppm limits; reproductive toxicants | Binding at pre-IND; residual solvent analytical package required; thin-film evaporation for removal |
| Pd residues | ICH Q3D oral limit 100 μg/day | Binding at any clinical stage; scavenging adds 1–2 steps + 10–20% yield loss |
| NaH + DMF | Formyl anion / H₂ evolution exotherm | >100 mmol: control addition rate and temperature; switch to NaH/THF or K₂CO₃ |
| TFA deprotection at scale | CO₂ + isobutylene gas evolution; corrosive waste | >1 kg: scrubbing + neutralisation required |
| Cryogenic requirement | Macrolactamisation at 0°C | No steps below –20°C anticipated; 0°C is manageable but adds cost at plant scale |

---

## Purification-limiting steps

**1. Macrolactamisation (Step 6)** — Defines programme throughput. Oligomeric byproducts have similar polarity to monomer; require preparative HPLC or large-scale MPLC/silica. At 0.005 M and 40% yield, 1 kg of precursor in 200 L DMF gives ~350 g macrolactam before purification. This is the bottleneck above 100 g.

**2. Chiral SFC epimer separation** (Steps 5–6) — If epimerisation is not suppressed to <2% at the macrolactam stage, preparative SFC is required. At 90:10 dr, ~20% of material is lost to the minor (S)-epimer per batch. SFC instrument becomes rate-limiting at Phase 2 clinical scale. Address at the chemistry level before scaling.

**3. Pyrazole regioisomer separation (Step 1)** — 1-methyl vs 2-methyl isomers must be resolved. At fragment scale this is manageable; at kg scale must be replaced by crystallisation. If regioisomer ratio cannot reach >10:1, this step becomes a fragment supply bottleneck.

---

## De-risking experiments

### Experiment 1 — Macrolactamisation model study

Prepare a simplified analogue of similar chain length lacking the pyrazolopyrimidine ring system. Run macrolactamisation at four concentrations (0.05 M, 0.02 M, 0.01 M, 0.005 M) with three coupling reagents (HATU, PyBOP, T3P) in a 96-well screening format. Measure monomer yield by LCMS vs internal standard.

**Go:** ≥35% monomer yield at ≤0.01 M under at least one condition.

**Abandon:** <15% monomer yield across all conditions at 0.005 M — conformational pre-organisation is insufficient. Redesign disconnection: close the aryl ether rather than the lactam, or introduce a conformational pre-organising element (gem-dialkyl or fluorine gauche effect) in the chain.

---

### Experiment 2 — Epimerisation stress test at C-10

Take 50 mg of the N-Boc, C-10-(R) linear amino acid precursor. Treat with HATU (1.1 eq), DIPEA (3 eq), DMF, 0°C, 1 h — no competing nucleophile; testing activation step only. Quench, extract, analyse by chiral SFC. Repeat with HATU/collidine and T3P/collidine.

**Go:** <5% (S)-epimer under at least one condition.

**Abandon:** >15% (S)-epimer under all activation conditions. SFC purification at this level would consume ~30% of material per batch and cap throughput at clinical scale. Redesign: install C-10 after ring closure via asymmetric desymmetrisation, or use a macrolactamisation disconnection not alpha to C-10.

---

### Experiment 3 (run in parallel with Exp. 1) — O-arylation selectivity

Test SNAr (Cs₂CO₃, DMSO, 80°C) and Mitsunobu (PPh₃/DIAD, THF, RT) on the fluoroaryl fragment + C-10 alcohol, with C-7 amine Boc-protected and unprotected in parallel. Measure O/N-arylation ratio by LCMS.

**Go:** ≥70% O-arylation, <5% N-arylation with Boc protection.

**Abandon SNAr if:** Conversion <50% at 100°C or N-arylation >10% with Boc protection. Switch to Pd-catalysed O-arylation (Pd₂dba₃/dppb, Cs₂CO₃, dioxane, 80°C) or redesign the building block to incorporate an additional electron-withdrawing substituent ortho to the fluorine.

---

## Summary

The route is technically executable but has three single points of failure that must be addressed before committing to multi-gram synthesis: **(1)** macrolactamisation yield and concentration dependence, **(2)** epimerisation rate at C-10 under coupling conditions, and **(3)** O-arylation selectivity in the presence of the C-7 amine. Run Experiments 1 and 2 simultaneously this week. If both pass, proceed to full linear assembly. If either fails the go criterion, the redesign point has been identified before three months of precursor synthesis are committed.
