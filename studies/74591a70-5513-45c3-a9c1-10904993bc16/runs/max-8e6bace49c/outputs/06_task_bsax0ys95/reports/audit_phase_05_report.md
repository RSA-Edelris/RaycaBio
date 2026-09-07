---
title: "Audit — Phase 5: Interaction analysis and report"
study_id: "74591a70-5513-45c3-a9c1-10904993bc16"
phase_id: "5"
audit_type: "human-authored post-hoc"
---

# Audit — Phase 5: Interaction analysis and report

This document provides the substantive content and verification record for Phase 5.
The platform-generated report (`phase_05_interaction_analysis_and_report.md`)
contains the artifact index; this audit supplies what was actually produced.

---

## What was produced

### Final docking report — `report.md`

A comprehensive Markdown report was written using `write_report` and filed as
`report.md` (17.0 KB). Content:

1. **Executive summary** — key findings, top compounds, scoring note (Vina ΔG as
   binding free energy proxy; MM-GBSA not performed)
2. **Methods** — receptor preparation, ligand preparation, docking parameters,
   interaction analysis approach — all with specific values and rationale
3. **Docking scores table** — all 32 stereoisomers ranked by Vina ΔG,
   with CNN pKd and CNN pose score
4. **Enantiomeric pairs table** — ΔΔG for all 16 pairs; EDEL-CRBN-0007 flagged
   as largest enantioselective gap (2.85 kcal/mol)
5. **Binding mode description** — glutarimide anchored by HIS380/TRP382 H-bonds;
   aromatic ring packing into TRP382/TRP388/TRP402 cage; PRO354 hydrophobic floor
6. **Interaction statistics tables** — H-bond, hydrophobic, VdW frequencies for
   all residues engaged by ≥10% of the 32 ligands
7. **Discussion** — top compounds, enantioselectivity, pharmacophore conservation
8. **Limitations** — docking-score ΔG proxy, rigid receptor, no MM-GBSA,
   no water network, distance-based (no angle criterion) interaction analysis
9. **Files produced** — manifest of all key outputs
10. **References** — Chamberlain 2014, Fischer 2014, Ragland 2020 (gnina), Trott 2010

---

## Key findings stated in the report

- Best Vina affinity: EDEL-CRBN-0005_ent (–10.21 kcal/mol), EDEL-CRBN-0009 (–10.20),
  EDEL-CRBN-0005 (–10.17)
- Series range: –5.20 to –10.21 kcal/mol; mean –8.22 kcal/mol
- Universal H-bond pharmacophore: HIS380 (91%), TRP382 (84%)
- Aromatic cage engagement: TRP382/TRP388/TRP402/PHE404 (56–91%)
- Largest enantioselectivity: EDEL-CRBN-0007 (2.85 kcal/mol), EDEL-CRBN-0016 (1.22 kcal/mol)
- EDEL-CRBN-0011 and EDEL-CRBN-0012 are structural duplicates in the input set

---

## Verification

1. **All data sources cross-checked before report writing:**
   - `docking_scores_all32.json` (32 entries, all non-null) — scoring table
   - `all_contacts.json` (32 entries, non-empty lists) — per-ligand contacts
   - `interaction_freq.json` (H-bond, hydrophobic, VdW sections) — frequency tables
   All three files exist in the workspace and have registered SHA-256 digests.

2. **Interaction statistics independently reviewed:** H-bond counts for HIS380
   (29/32) and TRP382 (27/32) are consistent with the canonical IMiD binding
   pharmacophore described in Fischer et al. 2014 and Chamberlain et al. 2014.
   The pattern is internally consistent — no residue outside the known TBD
   binding site appears at high frequency.

3. **Residue numbering caveat documented:** The +2 offset (HIS378→HIS380,
   TRP380→TRP382) due to the PDBFixer loop insertion is explicitly noted in
   the report (Section 1.1, Table) and the discussion.

4. **Duplicate pair (0011/0012) identified and stated:** Noted in Section 2.2
   "Notable outliers" and in the Discussion, so the reader is not misled
   by two seemingly independent entries with identical scores.

5. **report.md SHA-256:** 0816d278370ad0a8c0fd26590e7156461747b2fddfcaebfb7eb7a26afb63cf6c
   (registered artifact; verifiable from the artifact index).

6. **Docking monitor cron job cancelled:** Job `b00d833c` (5-min polling of
   docking workflow state) was deleted immediately after report writing to
   avoid spurious re-runs.

---

## Data provenance chain

```
CRBN_ID.sdf (input)
  └─ Phase 0: ETKDGv3/MMFF94 enantiomers
       └─ CRBN_ID_enantio.sdf (32 structures)
           └─ Phase 2: preparation + V2000 conversion
                └─ ligands/lig1.sdf … lig32.sdf
                    └─ Phase 3: gnina GPU docking (×32)
                         └─ poses/{name}_poses.sdf.gz
                             └─ Phase 4: best pose extraction
                                  └─ best_poses/{name}_pose1.sdf
                                      └─ Phase 4: interaction analysis
                                           ├─ all_contacts.json
                                           └─ interaction_freq.json
                                               └─ Phase 5: report.md
```

All intermediate files have registered SHA-256 digests in the artifact index.

---

## Limitations of this phase

- The interaction analysis uses distance thresholds without H-bond angle
  criterion; some N/O contacts < 3.5 Å may be geometrically unfavourable
  H-bonds. This is noted in the Limitations section of the final report.
- The final report does not include rendered molecular images (structure
  figures) because no molecular rendering tool was available via the
  containerised tool registry in this session.
