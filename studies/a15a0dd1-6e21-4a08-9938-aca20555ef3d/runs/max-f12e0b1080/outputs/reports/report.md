
## Provenance

**Public PDB coordinates used throughout.** No user-supplied structures or compounds were found in this session. Every number below derives from:

| Entry | Complex | Stabiliser |
|-------|---------|------------|
| **6H0F** | DDB1–CRBN / IKZF1-ZF2 | Pomalidomide (residue Y70) |
| **2O98** | 14-3-3 / H⁺-ATPase C-tail | Fusicoccin (residue FSC) |

---

## Part 1 — Crystallographic Quality

### 6H0F

| Parameter | Value |
|-----------|-------|
| Method | X-ray diffraction |
| Resolution | **3.25 Å** |
| Space group | P 2₁ 2₁ 2₁ |
| R-work / R-free (overall) | **0.212 / 0.234** |
| R-work / R-free (outer shell) | 0.262 / 0.304 |
| DPI (Blow, free R) | **0.46 Å** |
| Molecules in ASU | **4 copies** of the DDB1–CRBN–IKZF1 ternary complex (chains A–C, D–F, G–I, J–L) |

**What this means for design.** 3.25 Å is serviceable but the ~0.5 Å coordinate precision (DPI) means individual H-bond distances should be read as ±0.5 Å and side-chain rotamer assignments are uncertain. Use contact topology (which atoms are close) rather than exact distances to drive design decisions. The four NCS copies agree well (R-work/R-free gap is only 0.022), which corroborates the binding mode.

**Missing residues.** No REMARK 465 entries deposited. IKZF1-ZF2 is intentionally minimal (33 residues, chain C). Both zinc fingers of IKZF1-ZF2 are represented (residues ~141–175); nothing critical to the degron interface is absent.

**Alternate conformations.** Twelve alt-loc sites recorded, all in the CRBN chains (B/E/H/K): **HIS378 A/B and SER379 A/B** in every copy. These two residues flank the glutarimide-binding site directly — HIS378 makes a strong contact to the glutarimide C=O (O11–Nε2 2.82 Å equivalent) and SER379 contacts N16 and O20. The disorder reflects conformational plasticity at the CRBN rim that accommodates different glutarimide substituents; any modification at the glutarimide must tolerate both rotamers.

**Pomalidomide ligand quality (chain B / copy 1):**

| Parameter | Value |
|-----------|-------|
| Occupancy (heavy atoms) | 1.00 throughout |
| Occupancy (added H) | 0.00 (placed by software, not observed) |
| Mean B-factor (all copies, range) | 50–72 Å² |
| Per-copy mean B | B: 59 Å², E: 51 Å², H: 50 Å², K: 72 Å² |
| Wilson B estimate at 3.25 Å | ~55–65 Å² expected |

Heavy-atom occupancy is full and the B-factors fall within the expected Wilson range, so the binding mode is well-supported by density. Copy K is the most disordered; prefer copies B/H for geometric measurements.

---

### 2O98

| Parameter | Value |
|-----------|-------|
| Method | X-ray diffraction |
| Resolution | **2.7 Å** |
| Space group | I 4₁ 2 2 |
| R-work / R-free (overall) | **0.178 / 0.263** |
| R-work / R-free (outer shell) | 0.205 / 0.329 |
| ESU (free R) | **0.35 Å** |
| Molecules in ASU | 2 copies of the 14-3-3 monomer + 2 H⁺-ATPase peptides |

**What this means for design.** 2.7 Å with R-free 0.263 is solid for interface work. Coordinate precision of 0.35 Å allows moderately confident H-bond assignments (±0.35 Å). The high-symmetry space group I4₁22 imposes crystallographic two-fold on the complex that cross-validates the two fusicoccin binding events independently.

**Missing residues.** No REMARK 465 entries. The H⁺-ATPase peptide (chains P/Q) covers the C-terminal 50-residue segment that contains the 14-3-3 recognition motif; no degron residues are absent.

**Alternate conformations.** Four sites: GLU146 A/B and ASP213 A/B in both 14-3-3 chains. Neither directly contacts fusicoccin; both are on helices α4 and α7 lining the amphipathic groove, away from the current pharmacophore.

**Fusicoccin ligand quality:**

| Parameter | Value |
|-----------|-------|
| Occupancy | **1.00 (all atoms, both copies)** |
| Mean B-factor chain A | 45 Å² (range 32–61 Å²) |
| Mean B-factor chain B | 50 Å² (range 38–69 Å²) |

Uniform full occupancy and moderate B-factors indicate a well-ordered, high-confidence binding mode. Fusicoccin is 74% surface-buried in the complex, leaving ~26% solvent-exposed — mostly the glucose hydroxyl groups, which are design handles.

---

## Part 2 — Contact Maps

### 6H0F: Pomalidomide

**Atom nomenclature orientation.** In Y70 (pomalidomide): atoms C1–C6 are the phthalimide benzene ring; C7/C9 and their carbonyls (O13) are the phthalimide imide; N8 is the glutarimide–phthalimide linker NH; the glutarimide ring carries N16 (imide NH), O11 (α-carbonyl), O19/O20 (terminal carbonyls), C12, C15, C17, C18.

#### CRBN contacts (chain B) — 13 residues

| Residue | Key interactions | Character |
|---------|-----------------|-----------|
| **TRP380** | N16→NE1 3.36 Å; 24×hydrophobic | Glutarimide NH to Trp indole nitrogen; deepest hydrophobic wall |
| **TRP386** | O11→NE1 3.15 Å; 21×hydrophobic | **Canonical CRBN anchor H-bond**: glutarimide C=O accepts from Trp NE1 |
| **TRP400** | O13→HZ2 3.40 Å; 11×hydrophobic | Second Trp H-bond donor; tri-Trp cage floor |
| **HIS378** | O11→Nδ1 equiv. 2.82 Å; N16→O(bb) 2.91 Å | Alternate-conformation gatekeeper; strong polar contacts |
| **SER379** | O20→Hα 2.74 Å; N16→Hα 3.23 Å | Glutarimide terminal polar contacts; alt-loc B also contacts |
| **GLU377** | N10→OE1 3.36 Å; O11→O(bb) 2.98 Å | Backbone and sidechain H-bonds to phthalimide linker region |
| **ASN351** | C7→ND2 3.43 Å; N8→Hβ 2.85 Å | Multiple polar contacts across phthalimide junction |
| **PRO352** | N8→Hδ2 3.24 Å; N10→Hγ3 3.05 Å | Pro puckering creates a hydrophobic shelf over N8/N10 |
| **HIS353** | H2→NE2 3.10 Å | Single aromatic C–H to His imidazole; phthalimide ring face |
| **PHE402** | O20→CE2 3.22 Å; O20→HE2 2.60 Å | Glutarimide terminal C=O near Phe ring edge |
| VAL350 | vdW only | Minor |
| HIS357 | vdW only | Minor |
| PHE381 | vdW only | Minor |

**Structural summary.** The tri-Trp cage (TRP380/386/400) is the dominant CRBN pharmacophore. TRP386 NE1→glutarimide O11 is the defining H-bond that pins all IKZF1 molecular glues to CRBN. HIS378 alt-loc disorder and SER379 both gate the glutarimide mouth; they are the primary selectivity filter between glue scaffolds (e.g. lenalidomide vs. pomalidomide vs. CC-220).

---

#### IKZF1-ZF2 contacts (chain C) — 6 residues

| Residue | Key interactions | Character |
|---------|-----------------|-----------|
| **GLN146** | H1→OE1 2.51 Å; C1→OE1 3.22 Å; N10→HE22 3.33 Å | **Primary neo-interface H-bond**: phthalimide C=O (O13/imide face) to Gln sidechain; most critical IKZF1 contact |
| **CYS147** | H2→O(bb) 2.75 Å; C2→O(bb) 3.23 Å | Backbone C=O of Cys147 accepts from phthalimide H |
| **ASN148** | H3→O(bb) 2.79 Å | Backbone contact from phthalimide H3 |
| **GLN149** | O13→O(bb) 3.38 Å | Backbone H-bond from imide carbonyl |
| **CYS150** | O13→Cα/C/O(bb) 3.14–3.41 Å | Multiple backbone contacts |
| **GLY151** | H3→N(bb) 2.85 Å; C3→N(bb) 3.15 Å | Backbone NH of Gly accepts from phthalimide |

**Structural summary.** The six IKZF1 contacts span the QCNQCG β-strand turn. GLN146 is the sole sidechain H-bond donor/acceptor from IKZF1; the remaining five are backbone. This explains why IKZF1-targeting glues tolerate only small changes at the phthalimide — every aromatic face H is engaged.

---

#### Bridging partition

| Partition | Pomalidomide atoms | Interpretation |
|-----------|-------------------|----------------|
| **Bridges both CRBN and IKZF1** | C1–C7, C9, H1–H3, H101, H102, H12, H141, H142, N10, O13 (20 atoms) | Entire phthalimide scaffold and imide core; the neo-interface glue surface |
| **CRBN-only** | N16, O11, O19, O20, C12, C15, C17, C18, H16, H181, H182 (11 atoms) | Glutarimide ring — the canonical CRBN anchor |
| **IKZF1-only** | *none* | No part of pomalidomide contacts IKZF1 without also contacting CRBN |

This confirms pomalidomide functions as an **asymmetric molecular glue**: the glutarimide warhead anchors deep in the tri-Trp CRBN cage, while the phthalimide scaffold lies flat at the neo-interface. The phthalimide stacks against both TRP386/PHE402 on CRBN and simultaneously presents its H-bond acceptors to GLN146 on IKZF1. IKZF1 contributes zero contacts that do not involve shared atoms — meaning the IKZF1 contacts are *entirely dependent* on the pre-formed CRBN geometry.

---

#### Hotspot residues — 6H0F

**CRBN hotspots:**
- **TRP380 / TRP386 / TRP400** — tri-Trp cage; the structural basis of CRBN's ligandability; irreplaceable
- **HIS378** (alt-loc A/B) — gatekeeper of glutarimide; differential between glues
- **GLU377** — backbone and sidechain H-bonds to the phthalimide linker; semi-anchored
- **ASN351 / PRO352** — N-cap of binding loop; contacts phthalimide junction

**IKZF1 hotspots:**
- **GLN146** — sole sidechain contact; the neo-substrate recognition residue; mutating to Glu or Lys abolishes glue degradation
- **GLY151** — backbone contact; constrains the degron β-turn geometry
- **CYS147 / ASN148** — backbone H-bond donors to phthalimide; second-tier

---

### 2O98: Fusicoccin

**Fusicoccin (FSC) structure overview.** 48 heavy atoms, diterpene glucoside: tricyclic 5-8-5 terpenoid core (carbons C1–C25, C29–C31), an acetate at C2 (OAc group: O8, C27, O22), a hydroxymethyl at C19 (C38, O43), a free hydroxy at C1 (O13), and a glucose sugar at C19 (C36, O37, C46–C48 with O29, O32, O34). Molecular formula C₃₆H₅₄O₁₃, MW ~698.

#### 14-3-3 contacts (chain A) — 16 residues

| Residue | Key interactions | Character |
|---------|-----------------|-----------|
| **ASP222** | O16→OD1 **2.78 Å**; O29→OD1 **2.75 Å** | Two direct H-bonds from FSC sugar hydroxyls to Asp sidechain; **strongest anchor** |
| **LYS129** | O32→NZ **3.14 Å** | H-bond from glucose C-3 OH to Lys ε-amino; key ionic/polar |
| **ASN49** | 12×polar; 7×hydrophobic | Extensive van der Waals across the terpenoid core |
| **PHE126** | 13×hydrophobic; 5×polar | Aromatic hydrophobic shelf over C-ring of terpenoid |
| **LYS221** | 3×polar; 4×hydrophobic | Adjacent to ASP222; forms the charged groove floor |
| **LEU225 / ILE226** | hydrophobic (3–4 each) | Hydrophobic closure of the amphipathic groove |
| **PRO174 / ILE175** | hydrophobic | C-ring contacts |
| **VAL53 / LEU50** | hydrophobic | Upper groove walls |
| GLU19, SER52, LYS56, MET130, GLY178 | minor polar/vdW | Periphery |

**Structural summary.** ASP222 is the dominant H-bond anchor (two bonds, ~2.75–2.78 Å), equivalent to the glutarimide–TRP386 bond in CRBN. LYS129 makes the second direct H-bond (O32–NZ). ASN49 and PHE126 provide the hydrophobic platform. The combination of ASP222 + LYS129 + PHE126 is the pharmacophoric triplet.

---

#### H⁺-ATPase contacts (chain P) — 3 residues only

| Residue | Key interactions | Character |
|---------|-----------------|-----------|
| **HIS930** | O37→NE2 **3.28 Å**; 8×polar; 5×hydrophobic | **Only direct H-bond to the ATPase**; penultimate His in C-terminal motif |
| GLN926 | 2×polar | Sidechain OE1 near the terpenoid margin |
| ILE956 | 6×hydrophobic | C-terminal Ile locks into the groove; hydrophobic |

**Structural summary.** The ATPase peptide contributes only 3 residues to FSC contacts. The sole direct H-bond is O37→HIS930-NE2 (3.28 Å). This is striking asymmetry: FSC binds primarily to 14-3-3 and recruits the ATPase peptide by completing the groove, stabilising the preformed peptide conformation rather than bridging it with extensive direct contacts.

---

#### Bridging partition — 2O98

| Partition | FSC atoms | Interpretation |
|-----------|-----------|----------------|
| **Bridges 14-3-3 and ATPase** | C6, C10, C17, C18, C25, C26, C31, C36, O13 (9 atoms) | Central terpenoid ring junction and C-ring edge; the platform atoms |
| **14-3-3 only** | C3, C7, C9, C11, C14, C15, C19, C20, C21, C23, C27, C28, C38, C46, C47, C48, O8, O16, O22, O24, O29, O32, O43 (23 atoms) | Terpenoid core + entire sugar moiety + acetyl group |
| **ATPase only** | **O37** (1 atom) | The single glucose hydroxyl that reaches HIS930 |

Only 9 of 48 FSC atoms genuinely bridge the interface, and the ATPase is nearly entirely dependent on a single oxygen (O37). This means **all sugar elaboration chemistry and most acetyl/hydroxyl variations are 14-3-3 contacts only**. The ATPase engagement arm is extremely thin.

---

#### Hotspot residues — 2O98

**14-3-3 hotspots:**
- **ASP222** — dual H-bond anchor; essential; analogous to CRBN TRP386
- **LYS129** — glucose ε-amino H-bond; important but could tolerate alternative H-bond donors
- **ASN49** — extensive polar envelope around C20–C23 of terpenoid
- **PHE126** — aromatic hydrophobic shelf; partially replaceable

**H⁺-ATPase hotspots:**
- **HIS930** — only direct H-bond contact and the key bridging residue; critical; mutation His930→Ala abolishes fusicoccin sensitivity in literature
- **ILE956** — C-terminal anchor; hydrophobic; fixing the peptide conformation

---

## Part 3 — Buried Surface Area

| System | BSA type | Value (Å²) | Notes |
|--------|----------|-----------|-------|
| 6H0F | Pomalidomide burial (free → bound) | 424 / 426 free = **99%** | Essentially complete burial; consistent with tight glue fitting a preformed hydrophobic cavity |
| 6H0F | CRBN/IKZF1 protein–protein BSA | **~522 Å²** | Small by PPI standards; the drug creates >50% of the buried area, consistent with a neo-substrate interface with no pre-existing affinity |
| 2O98 | Fusicoccin burial (free → bound) | 628 / 853 free = **74%** | 26% of FSC remains solvent-exposed (glucose hydroxyls) — confirmed design handles |
| 2O98 | 14-3-3/ATPase protein–protein BSA | **~1063 Å²** | ~2× larger PPI than pomalidomide-mediated; native recognition surface, pre-existing weak affinity before drug |

The CRBN/IKZF1 interface (522 Å²) is substantially smaller than the 14-3-3/ATPase interface (1063 Å²). This reflects the fundamental difference: pomalidomide-induced interfaces are almost entirely drug-mediated (neo-substrate, Kd >1 mM before drug), while the 14-3-3/ATPase interface has inherent, structure-defined recognition that fusicoccin amplifies.

---

## Part 4 — Structured and Bridging Waters

### 6H0F — Waters near pomalidomide / CRBN / IKZF1

Six resolved waters. Only 32 waters total in a 3.25 Å structure with four 200-kDa complexes — very sparse, as expected.

| Water | B-factor | Burial | Status | Bridges | Key contacts |
|-------|----------|--------|--------|---------|-------------|
| **HOH C301** | 46.5 Å² | **0.85** | **CONSERVED** | lig↔CRBN↔IKZF1 | CRBN GLU377:OE1; IKZF1 GLN146:NE2 |
| **HOH C302** | 35.3 Å² | **0.79** | **CONSERVED** | lig↔CRBN↔IKZF1 | CRBN HIS353:NE2; IKZF1 GLN146:OE1/CB |
| HOH B601 | 30.4 Å² | 0.88 | CONSERVED | lig↔CRBN | CRBN SER192:OG; GLN206:OE1 |
| HOH B602 | 28.1 Å² | 0.82 | CONSERVED | lig↔CRBN | CRBN GLN198:O; ASN203:OD1 |
| HOH B603 | 24.0 Å² | 0.83 | CONSERVED | lig↔CRBN | CRBN ASP255:OD2 |
| HOH C303 | 20.0 Å² | 0.76 | uncertain | none | IKZF1 HIS167:ND1 only |

**The two structurally critical waters are HOH C301 and HOH C302** — both reside in the IKZF1 chain coordinate frame and simultaneously bridge the phthalimide imide carbonyl (O13, the lig↔CRBN contact), GLU377 on CRBN, and GLN146 on IKZF1. They are deeply buried (0.79–0.85), have the lowest B-factors of the interface waters, and appear in all four NCS copies, which independently validates them.

**Design implication.** These waters are **likely conserved and not displaceable without penalty**. The GLU377–water–GLN146 bridge is one of only two molecular links between pomalidomide and IKZF1 that pass through the water network. A design aiming to replace HOH C301/C302 would need a single atom (O or N) positioned with sub-ångström accuracy at the centre of a 3-body H-bond cluster — achievable in principle only with a rigidly positioned phenolic OH or a morpholine oxygen. The safer strategy is to avoid disturbing this region entirely.

HOH B601–B603 are CRBN-only, deeply buried, and conserved in CRBN structures generally; treat them as part of the receptor.

---

### 2O98 — Waters near fusicoccin / 14-3-3 / ATPase

Seventy-seven waters assessed. Select list (bridging and high-confidence conserved waters):

| Water | B (Å²) | Burial | Status | Bridges | Key contacts |
|-------|--------|--------|--------|---------|-------------|
| **HOH A1042** | 50.3 | **1.00** | CONSERVED | lig↔14-3-3↔ATPase | 14-3-3 ARG67:NH1; ATPase GLN952:CA, SER953:N |
| **HOH A1041** | 52.6 | **0.98** | CONSERVED | lig↔14-3-3↔ATPase | 14-3-3 GLU189:CD; ATPase GLN951:OE1, GLN952 |
| **HOH A1012** | 43.5 | **0.93** | CONSERVED | lig↔14-3-3↔ATPase | 14-3-3 LYS56:NZ; ATPase HIS930:ND1 |
| **HOH A1007** | 43.1 | **0.87** | CONSERVED | lig↔14-3-3↔ATPase | 14-3-3 LYS221:O; ATPase GLN926:OE1 |
| **HOH A1023** | 44.9 | **0.78** | CONSERVED | lig↔14-3-3↔ATPase | 14-3-3 ARG67:O; ATPase ILE950:CG2 |
| HOH A1043 | 50.2 | 1.00 | CONSERVED | lig↔14-3-3 | LEU43:N; SER117:OG |
| HOH A1049 | 44.6 | 1.00 | CONSERVED | lig↔14-3-3 | SER35:O; SER35:OG |
| HOH A1013 | 22.6 | 0.83 | CONSERVED | lig↔14-3-3 | ASN49:OD1; FSC:C23 |
| HOH A1019 | 49.6 | 0.70 | CONSERVED | lig↔14-3-3 | FSC:O37 (bridging FSC O37 to receptor) |
| HOH A1059 | 76.8 | 0.93 | **DISPLACEABLE** | lig↔14-3-3 | SER219:N/C |
| HOH A1040 | 62.4 | 0.90 | **DISPLACEABLE** | lig↔14-3-3 | THR143:N/CA |
| HOH A1034 | 65.9 | 0.76 | **DISPLACEABLE** | lig↔14-3-3 | ASN81:ND2; GLU83:CG |
| HOH A1016 | 115.8 | 0.50 | **DISPLACEABLE** | lig↔14-3-3 | GLU19:OE1 |
| HOH A1029 | 107.2 | 0.60 | **DISPLACEABLE** | lig↔14-3-3 | GLU10:OE2; MET14:SD |

The five conserved bridging waters (A1042, A1041, A1012, A1007, A1023) form a **water network at the 14-3-3/ATPase interface** that fusicoccin organises without directly contacting. These water molecules explain the seemingly sparse ATPase contacts: fusicoccin mediates ATPase binding largely through ordered waters rather than direct ligand–peptide contacts. This is a structural consequence of fusicoccin's rigidity — the terpenoid core is too bulky to reach deep into the peptide-binding groove.

**Displaceable waters** (A1059, A1040, A1034, A1016, A1029) are located at the periphery of the 14-3-3 groove rim, all on 14-3-3 only, with B-factors > 60 Å². These represent design handles: a polar substituent of the right geometry would be entropically favoured to displace each.

---

## Part 5 — Unoccupied Pocket Subsites

### 6H0F

Grid-based void mapping (0.8 Å step, probe 1.2 Å, shell 2.5–5.5 Å from ligand heavy atoms) identifies six clusters around pomalidomide. Volumes estimated from void-point count × (0.8 Å)³.

| Subsite | Near residues | Vector from centroid | Interpretation |
|---------|--------------|---------------------|----------------|
| **S1** | CRBN TRP386 / IKZF1 CYS150 | (+0.56, –0.79, +0.24) | Rim cleft between TRP386 edge and CYS150 backbone; a short vector pointing slightly above the phthalimide plane toward IKZF1 |
| **S2** | CRBN GLU377 / HIS378 | (–0.96, –0.25, –0.14) | Anti-parallel to phthalimide C–H bond; gap between the GLU377 loop and HIS378; partially occupied by the bridging water HOH C301 |
| **S3** | CRBN ASN351 / PRO352 | (–0.22, +0.78, +0.59) | Above the phthalimide 5/6-position; toward ASN351 and the exposed face of the loop |
| S4 | CRBN GLU377 / SER375 | (–0.63, –0.73, –0.26) | Overlapping with S2; sub-cluster |
| S5 | CRBN TRP386 / SER375 | (–0.35, –0.84, –0.42) | Hydrophobic floor below TRP386; tight and mostly hydrophobic |
| S6 | CRBN TRP386 / SER379 | (–0.35, –0.42, –0.84) | Deep below glutarimide, near SER379 alt-loc zone |

**Subsite S1** is the most attractive design vector because it is at the exact CRBN/IKZF1 boundary (TRP386 on one side, CYS150 on the other) and is not blocked by any conserved water. **S3** (toward ASN351/PRO352) is currently unoccupied and accessible from the phthalimide C5 position without displacing any conserved contacts. **S2** should be approached cautiously — the bridging water HOH C301 occupies part of this void and bridges to IKZF1 GLN146.

**Cannot grow vectors:** The glutarimide sits in a deep, enclosed tri-Trp cage with no accessible void below O11/O19 (toward TRP400 and TRP380). Substitution at C3 of the glutarimide pointing downward (toward TRP400) would clash with TRP400-NE1 at <3 Å. The imide NH (N8) at the phthalimide–glutarimide junction cannot be alkylated without abolishing both the GLU377 and bridging-water contacts.

---

### 2O98

| Subsite | Near residues | Vector from centroid | Interpretation |
|---------|--------------|---------------------|----------------|
| **S1** | 14-3-3 VAL53 / ATPase HIS930 | (–0.06, +0.03, –1.00) | Directly between FSC and HIS930; points toward ATPase; currently bridged by HOH A1012 only |
| **S2** | 14-3-3 ASN49 | (+0.79, +0.20, +0.57) | Extension of the hydrophilic groove along the ASN49 face; toward a shallow solvent-exposed recess |
| **S3** | 14-3-3 LEU225 / ATPase HIS930 | (–0.95, –0.28, –0.16) | Second vector toward HIS930, from the LEU225 side; partially occupied by HOH A1023 |
| S4 | 14-3-3 ILE226 / ASP222 | (–0.49, –0.41, +0.77) | Between ILE226 and the ASP222 region; deep in the groove floor |
| S5 | ATPase HIS930 | (–0.36, +0.19, –0.91) | Third HIS930-proximal void; sub-cluster of S1 |
| S6 | 14-3-3 ASP222 | (–0.45, +0.23, +0.86) | Adjacent to ASP222; room for a small substituent near the sugar anchor |

The most striking finding is that **three of six unoccupied subsites converge on ATPase HIS930** (S1, S3, S5). The ATPase contact is currently so thin (O37 only, bridged by HOH A1012) that there is substantial unfilled space around HIS930. This is the primary opportunity to strengthen ATPase engagement.

**Cannot grow vectors:** Elaboration pointing toward 14-3-3 ARG67 (S1/S3 interior portion) would clash with the ordered water network A1042/A1041/A1023 (burial > 0.98 in all cases). Extending the acetyl group at C2 toward GLU19 would encounter HOH A1016 (displaceable, B=116 Å²) — this is actually a possible target. The glucose C-6 OH position (distal end pointing toward LYS129 NZ) cannot be grown into without leaving the LYS129 H-bond orbit.

---

## Part 6 — Ranked Design Vectors

### 6H0F — Pomalidomide / CRBN–IKZF1 molecular glue

| Rank | Vector | Site | Interaction gained | Risk |
|------|--------|------|--------------------|------|
| **1** | **C5-position substituent on phthalimide ring** (short aliphatic or halogen) | Subsite S3 — ASN351/PRO352 | New van der Waals/polar with ASN351-ND2 and PRO352-Cδ; closes a ~5 Å³ void without reaching any conserved water | Low: C5 points away from the HIS353/TRP386 contacts and from IKZF1 GLQ146; a single F or Me unlikely to lose existing bonds |
| **2** | **C6-position fluorine on phthalimide** | Rim between TRP386 NE1 and HIS353 NE2 | Halogen bond from C6–F to HIS353-NE2 (currently C–H contact at 3.10 Å); potential +0.5 to 1.0 kcal/mol gain | Low–moderate: risk of steric clash with TRP386-CE2 if too large; F only |
| **3** | **Small substituent at phthalimide C4-NH₂: replace NH₂ with NHCH₂OH or NHCO(small)** | Subsite S1 — TRP386/CYS150 boundary | Extend current 4-amino group toward the CRBN/IKZF1 rim; could gain a contact with CYS150 backbone O or TRP386-Nε1 | Moderate: 4-amino is already engaging CRBN; N-methylation disrupts the existing NH donor contacts with ASN351; linker length must be ≤2 bonds |
| **4** | **Glutarimide C3α-methyl (S-stereochemistry toward SER379)** | Subsite S6 — SER379 alt-loc region | Fills the void below N16/O20 near SER379-Oγ; could fix the SER379 alt-loc ensemble into one conformation, entropic gain | Moderate: HIS378 alt-loc B occupies adjacent space; S-methyl is known from CC-220 series and is tolerated; R-methyl clashes with TRP380 |
| **5** | **Replace glutarimide NH (N16) with O (succinimide bioisostere)** | Direct CRBN TRP380/TRP386 contacts | Removes N16-to-TRP380 H-bond donor; simplifies H-bond network but may improve metabolic stability | High: N16 is an H-bond donor to TRP380-NE1 (3.36 Å); loss likely reduces CRBN affinity by >10-fold unless compensated |

---

### 2O98 — Fusicoccin / 14-3-3–H⁺-ATPase native PPI stabiliser

| Rank | Vector | Site | Interaction gained | Risk |
|------|--------|------|--------------------|------|
| **1** | **Extend O37 with a short amino-ethyl or propanoic acid arm toward HIS930** | Subsite S1 — ATPase HIS930 | Direct H-bond to HIS930-NE2 (currently 3.28 Å, water-bridged via HOH A1012); an NH→NE2 or COOH→Nε contact would be more direct; potential displacement of HOH A1012 | Moderate: HOH A1012 is classified CONSERVED (burial 0.93, B=43.5); direct displacement requires that the extended group recapitulates the 3-body geometry; an amino group is preferred as it makes a donor H-bond to both NE2 and ND1 of HIS930 simultaneously |
| **2** | **Displace HOH A1016 (B=116, burial=0.50) near GLU19** | Subsite near GLU19 rim | Replace the water with a 1,2-diol or hydroxymethyl on the terpenoid C1-OH arm; gain a direct bond to GLU19-OE1 | Low: the water is clearly displaceable (B=116 is extreme); GLU19 makes only 1×polar contact currently; this is a peripheral site that adds selectivity rather than potency |
| **3** | **Replace acetyl at C2 with carboxymethyl** | ASP222 / LYS129 groove | The carboxylate would extend toward LYS129-NZ (currently O32→NZ 3.14 Å) and could add a second ionic anchor; simultaneously displaces HOH A1034 (B=65.9 Å², displaceable) | Moderate: carboxylate at C2 changes pKa of adjacent OH; conformational freedom must be constrained; existing OAc is hydrophobic-compatible — polar swap at C2 may affect how PHE126 packs against the acetyl methyl |
| **4** | **Replace glucose with a rigidified mimic (e.g. glucuronic acid or mono-deoxy variant)** | Sugar-binding groove of 14-3-3 | Maintain ASP222 and LYS129 H-bonds; reduce molecular weight by ~162 Da (glucose: 180 Da); improve cell permeability | Low (binding risk) / High (synthesis risk): the sugar contacts are straightforward but rigidification requires knowing the exact bioactive sugar ring conformation from NMR or crystal of the analogue |
| **5** | **Add small hydrophobic group to C17/C18 bridging position** | Subsite S4 — ILE226/ASP222 | C17 and C18 are in the bridging atom set (contact both partners); a gem-dimethyl or spirocycle here could improve hydrophobic contact with ILE226/LEU225 floor | Low: the vector points toward a hydrophobic pocket between ILE226 and LEU225 that is currently underexploited; no conserved water in the path; risk is steric clash with ASP222 beyond C17 |

---

## Summary

**6H0F quality and design confidence.** 3.25 Å with R-free 0.234 and four independent NCS copies — adequate for identifying the binding mode and hotspots, but the 0.46 Å DPI means exact side-chain geometry should not be over-trusted. The 99%-buried pomalidomide is anchored principally by the tri-Trp CRBN cage and has zero IKZF1-exclusive contacts, confirming that CRBN pre-organises the glue and IKZF1 simply docks onto the exposed phthalimide face. The two bridging waters HOH C301/C302 are well-supported by four NCS copies and are likely conserved in all CRBN/IKZF1 crystal forms; do not attempt to displace them. The best design space is at phthalimide C5 (S3 subsite, toward ASN351, low risk) and C6-F for HIS353 halogen bond (low-moderate risk).

**2O98 quality and design confidence.** 2.7 Å, R-free 0.263, ESU 0.35 Å — the better structure for design. Fusicoccin is 74% buried with uniform full occupancy. The remarkable asymmetry of the contact map (16 14-3-3 residues vs. 3 ATPase residues; O37 is the sole ATPase-exclusive contact) means that the natural product exploits the 14-3-3 amphipathic groove almost entirely and barely reaches the ATPase. The five highly buried bridging waters (A1042, A1041, A1012, A1007, A1023) mediate most of the ATPase stabilisation and should be treated as part of the pharmacophore network. The highest-priority design vector is an O37-extension toward HIS930 (S1 subsite) to strengthen the one direct ATPase H-bond; a carboxymethyl or aminoethyl arm of ≤4 bonds should achieve a direct 2.8–3.2 Å contact with HIS930-NE2 while potentially co-opting the HOH A1012 position or retaining it as a bridging water.
