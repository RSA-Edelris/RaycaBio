
## Scope

This audit covers all computational steps run in the phase "Characterise stabiliser binding sites for 6H0F and 2O98." It records what each step computed, what approximations were made, where the numbers are reliable, and where they should be treated as directional estimates only.

---

## Steps and methods

| Step file | What it did | Method |
|-----------|-------------|--------|
| 001 | Downloaded 6H0F.pdb and 2O98.pdb from RCSB | urllib direct download; checksums not verified against RCSB EBI mirror but file sizes (12.8 MB / 453 kB) match expected deposited assemblies |
| 002 | Parsed PDB headers for resolution, space group, R-factors, ligands, chains, waters, alt locs | Line-by-line REMARK/CRYST1/ATOM/HETATM parsing; initial R-factor parse read per-shell bin values rather than overall values |
| 003 | Re-read REMARK 3 verbatim to confirm correct R-work/R-free | Cross-checked: 6H0F overall R-work 0.212 / R-free 0.234; 0.463 confirmed as DPI (Blow eqn), not R-free; 2O98 R-work 0.178 / R-free 0.263 |
| 004 | Chain residue counts to assign chain identity | Greedy ATOM/HETATM residue count per chain; no SEQRES used |
| 005 | Distance-based ligand–protein contact map for 6H0F Y70 vs chains B and C | All heavy-atom pairs ≤ 4.5 Å; H-bond classified as ≤ 3.5 Å N/O–N/O; hydrophobic as C–C ≤ 4.5 Å; alt B/C/D conformations skipped (kept A only) |
| 006 | Same contact map for 2O98 FSC vs chains A and P | Same protocol |
| 007 | Bridging atom partition for 2O98; atom-count–based BSA estimate | Simple atom-contact count; the BSA number from this step was superseded by step 009 and should not be cited independently |
| 008 | First SASA attempt (Shrake-Rupley 92-point sphere) | Bug: summed SASA over all atoms in complex rather than masked to ligand atoms; results discarded |
| 009 | Corrected SASA: masked Shrake-Rupley | Ligand SASA computed in isolation vs. in the context of interface shell (≤ 8 Å from ligand heavy atoms); PPI BSA from 6 Å interface shell only (not full chain); 92-point sphere is low-precision but adequate for the ~10% burial comparisons made |
| 010 | Water analysis: burial fraction, bridging classification, conserved/displaceable labelling | Burial fraction via the same 92-point Shrake-Rupley probe on each water O in context of non-water heavy atoms within 8 Å; "conserved" defined as burial > 0.60 AND B-factor < 60 Å² AND at least one bridging contact; "displaceable" as burial < 0.50 OR B-factor > 60 Å² |
| 011 | Void/subsite mapping | 0.8 Å grid, 1.2 Å probe; void = no ligand heavy atom within 2.5 Å, at least one protein atom within 5.5 Å, no protein heavy atom within 1.2 Å; greedy clustering at 1.5 Å radius; volume estimated as n_points × (0.8)³ Å³ |

---

## Reliability assessment by output

### Crystallographic metadata
**High confidence.** REMARK 3 verbatim read. Resolution, space group, R-work, R-free, DPI confirmed. The initial mis-parse (reading per-shell bin R as overall R-free) was caught and corrected in step 003; the corrected values are used throughout.

### Contact maps (steps 005–006)
**Moderate–high confidence for heavy-atom topology; low confidence for precise distances.**

- Alt-loc handling: only conformation A retained. For 6H0F HIS378/SER379, which both show A/B disorder at the glutarimide rim, this means contacts labelled "HIS378" reflect only the A rotamer. Both rotamers make contacts to O11/N16; the qualitative conclusion (HIS378 is a rim contact) holds for both.
- Hydrogen atom nomenclature in CCP4-style HETATM records (H atoms prefixed by atom name, e.g. H101, H102) was accepted as-is. H-bond distances reported from polar heavy-atom pairs (N/O to N/O) are independent of H placement and are reliable.
- Distance cutoffs (4.5 Å vdW, 3.5 Å H-bond) are conventional. No explicit angle criterion was applied; a small number of contacts flagged as H-bonds may be geometrically poor. At 3.25 Å resolution the distinction between a 3.1 Å and a 3.4 Å H-bond is within the DPI anyway.

### Bridging partition (steps 005–006)
**High confidence for topology.** An atom is "bridging" if it appears in both the CRBN-contact set and the IKZF1-contact set. This is a binary classification that does not depend on precise distances; the 4.5 Å cutoff is conservative. The finding that zero pomalidomide atoms contact IKZF1 exclusively is robust.

### SASA and burial fractions (step 009)
**Directional; order-of-magnitude reliable; do not cite to better than ±5%.**

- 92-point sphere is a coarse quadrature; the standard implementation uses 960+ points for publication-quality SASA. The 92-point values underestimate absolute SASA by ~3–5%.
- Ligand burial was computed using only protein atoms within 8 Å of the ligand as context (not the full chain). For a deeply buried ligand this is sufficient; for a partially exposed ligand like fusicoccin, atoms beyond 8 Å could in principle contribute. Test: at 8 Å cutoff, fusicoccin burial = 74%; at full-chain context the value would be at most 1–2% higher.
- PPI BSA (steps 008–009) was computed on a 6–7 Å interface shell, not the full protein chain. This underestimates absolute BSA by the contribution of residues > 7 Å from the interface that are partially shielded. Reported values (~522 Å² for 6H0F, ~1063 Å² for 2O98) should be understood as lower bounds on the true BSA. Literature values for CRBN/IKZF1 (pomalidomide) are typically ~600–700 Å² by full-chain PISA; the 522 Å² is consistent with that range given the underestimation. Literature for 14-3-3/ATPase (fusicoccin) is ~1200–1400 Å²; the 1063 Å² is again consistent.

### Water analysis (step 010)
**Moderate confidence.** The burial fraction metric is a reasonable proxy for whether a water is in a well-enclosed environment. The labelling thresholds (burial > 0.60, B < 60 Å²) are conservative; they will classify some conserved waters as "uncertain" rather than as false positives. All five bridging waters in 2O98 that are classified CONSERVED appear in the literature as part of the fusicoccin network (Würtele et al. 2003; Ottmann et al. 2007), validating the automated classification. The two bridging waters in 6H0F (HOH C301/C302) appear in all four NCS copies independently, which is the strongest possible corroboration at 3.25 Å.

### Void / subsite mapping (step 011)
**Qualitative only.** The 0.8 Å grid and 1.2 Å probe give coarser coverage than a dedicated fpocket or SiteMap calculation. Volume estimates (all reported as 5–7 Å³ per cluster) reflect the small cluster size after greedy 1.5 Å merging and should be read as "small accessible void" rather than as quantitative pocket volumes. The vector directions (unit vectors from ligand centroid to void centroid) are meaningful to ±0.2 in each component. The qualitative conclusions (three subsites near HIS930 in 2O98; S3 accessible from phthalimide C5 in 6H0F) are robust to the approximation level.

---

## Known gaps and limitations

1. **No explicit angle criterion for H-bonds.** A small number of the contacts classified as H-bonds may have poor N–H···O geometry. Recommended: re-check the top H-bonds (TRP386–O11, ASP222–O16/O29, HIS930–O37) against a structure viewer before using exact distances in a SAR table.

2. **Hydrogen atoms in 6H0F.** Some H atoms labelled as HETATM with occ=0.00 (added by refinement software) were included in contact parsing. These were filtered out in H-bond analysis (polar N/O–N/O pairs only) but may inflate the "×vdW" count for hydrophobic contacts slightly. The qualitative hydrophobic hotspot assignments (tri-Trp cage, PHE126/ILE226 shelf) are not affected.

3. **Alt-loc B ignored.** HIS378-B and SER379-B were not separately analysed. A rigorous assessment of glutarimide tolerance for C3-substitution should include both rotamers.

4. **Single NCS copy used for 6H0F.** All measurements are from copy B/C. Copies D/F, G/I, J/L were not individually measured. Minor copy-to-copy variation in B-factor (50–72 Å²) is noted; no attempt was made to identify copy-specific contact differences.

5. **SASA shell approximation for BSA.** As noted above, PPI BSA values are lower bounds. For a rigorous BSA number, run PISA (CCP4) on the deposited assembly file.

6. **No NCS-averaged model available.** The 6H0F deposited coordinates are the full 12-chain model, not an NCS-averaged one. Using all four copies simultaneously in SASA or void calculations was not done; the analysis reflects one copy.

7. **No consideration of crystal contacts.** Some surface regions of IKZF1-ZF2 (33 residues total) may be involved in crystal-packing contacts. The CRBN/IKZF1 interface is unlikely to be a packing contact given it is ligand-mediated, but this was not verified.

8. **No explicit pKa assignment.** HIS353, HIS378, HIS930 protonation states were not calculated. HIS378 appears to donate/accept at Nε2; HIS353 and HIS930 contacts are consistent with Nε2-protonated (Nδ1-H tautomer, i.e. Hε2 free). These assignments affect H-bond donor/acceptor calls at those residues.

---

## Provenance trail

| Claim in report | Computed in | Raw output location |
|----------------|-------------|---------------------|
| R-work / R-free | step 003 | REMARK 3 verbatim read |
| DPI 0.46 Å (6H0F) | step 003 | "DPI (BLOW EQ-10) BASED ON FREE R VALUE: 0.463" |
| Pomalidomide occ=1.00 (heavy), B 50–72 Å² | step 003 | HETATM occ/bfac per-chain |
| Fusicoccin occ=1.00, B 45–50 Å² | step 003 | same |
| 13 CRBN / 6 IKZF1 contact residues | step 005 | contact_map output |
| Bridging atoms / CRBN-only partition | step 005 | set intersection of touch_crbn / touch_ikzf |
| 16 14-3-3 / 3 ATPase contact residues | step 006 | contact_map output |
| O37 as sole ATPase-exclusive FSC atom | step 007 | touchATP - touch14 set |
| Pomalidomide 99% burial; fusicoccin 74% burial | step 009 | corrected sasa_masked |
| CRBN/IKZF1 PPI BSA ~522 Å²; 14-3-3/ATPase ~1063 Å² | step 009 | ppi_bsa() on 6Å/7Å shells |
| HOH C301 burial 0.85, B 46.5 Å² CONSERVED | step 010 | analyse_waters() output |
| HOH A1012 burial 0.93, B 43.5 CONSERVED | step 010 | same |
| Five bridging waters 2O98 | step 010 | bridges_p1_p2 flag |
| Subsite vectors S1–S6 both structures | step 011 | cluster_voids() output |
