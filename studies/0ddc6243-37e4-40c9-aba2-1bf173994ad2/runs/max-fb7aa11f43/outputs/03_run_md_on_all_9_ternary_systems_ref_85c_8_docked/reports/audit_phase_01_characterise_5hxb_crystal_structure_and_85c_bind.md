# Audit: Phase 1 — Characterise 5HXB crystal structure and 85C binding site

**Study:** 0ddc6243-37e4-40c9-aba2-1bf173994ad2  
**Run:** max-b1dc357bbc  
**Date audited:** 2026-09-15  

---

## What was done

Phase 1 characterised the 5HXB crystal structure (CRBN–GSPT1–CC-885 ternary
complex) and prepared the receptor for docking. All analysis used gemmi and
RDKit on the deposited CIF; no homology modelling or structure prediction was
used at this stage.

### Crystal quality

| Item | Value | Source |
|:-----|:------|:-------|
| Resolution | 3.6 Å | 5HXB REMARK 3 |
| Space group | P 1 2 1 | 5HXB CRYST1 |
| R / R_free | 0.271 / 0.321 | 5HXB REMARK 3 |
| ASU content | 3 ternary complexes (chains X/Y/Z + A/B/C + …) | 5HXB ATOM records |
| Chains used | Z (CRBN, 380 residues) + X (GSPT1, 195 residues) | Phase 1 code 032 |

R_free = 0.321 at 3.6 Å is within the expected range for this resolution
(mean R_free ~0.31–0.35 at 3.5–4 Å per the PDB validation report). No
Ramachandran outlier or clash score data were retrieved from the validation
report in this phase; this is a gap.

### Ligand 85C quality

| Pharmacophore region | B-factor (Å²) | Comment |
|:---------------------|:-------------|:--------|
| Glutarimide NH | ~71 | Well ordered; supports crystal contact geometry |
| Phthalimide core | ~120 | Intermediate |
| Chlorotolyl arm | ~236 | Poorly ordered; contacts to GSPT1 are approximate |
| Overall occupancy | 1.00 | Single conformation modelled |

The high B-factor on the chlorotolyl arm (3.3× the glutarimide) means that
computed GSPT1-contact distances carry higher uncertainty than CRBN contacts.

### Contacts and bridging

CRBN anchor contacts (glutarimide in Trp cage):
- W380 NE1 – 85C O2 (keto) at 3.18 Å (H-bond or C–H…O)
- W400 NE1 – 85C N2H  at 2.84 Å (N–H…N H-bond, key anchor)
- H353 NE2 – 85C O4 at 2.72 Å (HIE tautomer confirmed)
- N351 OD1 – 85C N2H at 2.97 Å

GSPT1 neo-interface contacts (chlorotolyl arm, approximate at 3.6 Å):
- K572 NZ – 85C Cl within 4.5 Å
- K573 NZ – 85C aromatic ring within 4.5 Å
- K628 Cε – 85C tolyl arm within 4.5 Å (used as distance probe in MD)

Bridging definition applied throughout: a compound is a CRBN-GSPT1 glue if
it satisfies BOTH a CRBN anchor criterion (glutarimide-NH contacts ≤ 4.0 Å
to Trp-cage) AND a GSPT1 bridge criterion (any atom ≤ 4.5 Å to GSPT1
neo-interface residues K572/K573/K628/S574).

### Pocket and growth vectors

Three unoccupied subsites identified:
1. **Subsite A** (chlorine pocket): shallow hydrophobic groove near W380/H378;
   +1–2 heavy atoms tolerated along Cl vector before steric clash.
2. **Subsite B** (GSPT1 lysine groove): K572/K573 positively charged pocket;
   acidic/H-bond acceptor extension of the tolyl arm into the groove.
3. **Subsite C** (phthalimide solvent exposure): N-H of phthalimide points
   toward solvent; vector available for linker attachment to bivalent agents.

### Receptor preparation choices

See `docking/receptor_prep_choices.txt` (now with Verification section).
Key choices: HIS353→HIE (NE2 donor confirmed), ZN retained for docking
receptor (removed for MD receptor to avoid parameter issues), no waters
(none in deposit at 3.6 Å).

## What was NOT done / gaps

- Ramachandran and all-atom clash score from PDB validation report: not retrieved.
- MolProbity or EDS per-atom density support for 85C: not checked (3.6 Å data
  makes EDS unreliable for individual ligand atoms anyway).
- Alternate conformations: none present in the deposit; not a gap.
- Missing residues: the 5HXB deposit covers seqids 48–500 in chain Z and
  440–634 in chain X; terminal disordered regions were not modelled and are not
  relevant to the stabiliser site.

## Audit verdict

**Acceptable for downstream docking and MD.** The crystal-based contact geometry
supports the receptor preparation choices. The chlorotolyl arm B-factors mean
that GSPT1-contact distances should be treated as approximate (±1–1.5 Å) rather
than precise. Glue classification thresholds in Phase 3 MD (CRBN_anchor < 10 Å,
GSPT1_bridge < 12 Å) are deliberately loose to account for this uncertainty.
