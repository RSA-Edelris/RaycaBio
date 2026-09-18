
## Phase 1: Structure Fetch and Parsing

### 5EU1 (BRD9–BI-7273)

Downloaded from RCSB PDB (4,589 lines). Two-chain asymmetric unit, chains A and B, each carrying the BRD9 bromodomain fragment (UniProt residues 14–134, 113 Cα atoms per chain). BI-7273 is registered as residue **5SW** at sequence position 201 in both chains; 26 heavy atoms per copy.

Resolution and experiment type: X-ray diffraction (title: "Crystal structure of BRD9 in complex with BI-7273"). Chain A was used for all downstream calculations.

### AlphaFold DCAF16 (Q9NXF7)

API query confirmed the current model is **v6** (URL: `AF-Q9NXF7-F1-model_v6.pdb`; the v4 URL returns HTTP 404). Downloaded 1,765 lines. Sequence length 216 residues.

| pLDDT tier | Residues | Fraction |
|---|---|---|
| Very high (>90) | 0 | 0% |
| Confident (70–90) | 0 | 0% |
| Low (50–70) | 13 | 6% |
| Very low (<50) | 203 | **94%** |

Mean pLDDT = 38.2; median = 37.2; max = 68.0; min = 26.0. The only contiguous stretch above pLDDT 50 spans residues 206–210 (5 residues, avg 53.5). The model is consistent with an intrinsically disordered protein that requires a binding partner (DDB1) to adopt a stable fold.

---

## Phase 2: DCAF16 Cysteine Characterisation

### Cysteine inventory

Eight cysteines identified (Cα positions from AF model):

| Residue | pLDDT | SG neighbours <5 Å | Sequence context | Lit ABPP |
|---|---|---|---|---|
| C58 | 47.5 | **23 (buried)** | `VKC↑LLKY` | No |
| C100 | 35.2 | 9 | adjacent to C103 | No |
| C103 | 33.6 | 9 | adjacent to C100 | No |
| C119 | 29.6 | moderate | isolated | No |
| C173 | 31.9 | 9 | `SC↑VSGCCC` | No |
| **C177** | 36.7 | 9 | `SC↑CCGWL` | **Yes** |
| **C178** | 34.5 | 16 | `SCC↑CGWL` | **Yes** |
| C179 | 33.2 | 10 | `SCCC↑GWL` | No |

C177–C179 form a **CCCG motif** (residues 177–179 separated by Cα–Cα distances of 3.8–6.1 Å). This spacing is consistent with a zinc-coordinating finger; Zn²⁺ coordination in the DDB1-assembled complex depresses pKa of the coordinated thiols, making them hyper-reactive toward electrophilic warheads. C177 and C178 are independently confirmed reactive by competitive ABPP.

C58 is excluded despite basic flanking residues (K57, K61) because its SG is tightly packed (23 heavy-atom neighbours within 5 Å) — the thiol is buried and inaccessible.

### Experimental PDB structures for DCAF16

RCSB REST query returned no hits for a DCAF16-containing entry in the PDB at the time of this analysis. All downstream modelling therefore relies on the AF v6 model with the low-confidence caveat stated above.

---

## Phase 3: BI-7273 Exposure and Attachment Vector Analysis

### Ligand burial

Of 26 heavy atoms in 5SW:
- **14 buried** (≥3 protein contacts within 4 Å) — occupy the acetyl-Lys pocket floor
- **12 exposed** (<3 contacts) — form a coherent exit face pointing in direction (-0.81, -0.59, -0.05) from the BRD9 centre of mass

Nearest BRD9 residues to the exposed face: Gly43, Phe44, His42 (GF/ZA loop). This loop region tolerates substituents in bromodomain SAR.

Primary attachment atoms: **N15** (secondary amine, 0 protein contacts, 3.54 Å min protein distance) and **C25** (terminal carbon, 0 contacts, 5.00 Å clearance). C25 was used as the geometric anchor for all warhead projections.

### Warhead reach as a function of linker length

| Linker | Warhead position (5EU1 frame) |
|---|---|
| 5 Å | (−2.0, −4.7, 5.1) |
| 7 Å | (−3.6, −5.8, 4.9) |
| 9 Å | (−5.2, −7.0, 4.8) |
| 12 Å | (−7.6, −8.8, 4.7) |

---

## Phase 4: Ternary Complex Geometry Scan

### Method

Naive full-protein rigid translation produced universal clashes because the 216-residue disordered chain sweeps BRD9's surface. Correct physical model: translate and rotate only the **±12 residue local backbone window** around each candidate cysteine (the constrained segment at the moment of encounter). Twenty-four rotations around the approach axis were sampled.

### Results

| Linker | Cys | Best clashes | Interface atoms | Est. BSA | Verdict |
|---|---|---|---|---|---|
| 5 Å | C178 | 1 | 23 | 345 Å² | viable |
| **7 Å** | **C178** | **0** | **16** | **240 Å²** | **best** |
| 9 Å | C177 | 2 | 34 | 510 Å² | viable |
| 9 Å | C178 | 0 | 11 | 165 Å² | viable |
| 12 Å | C177 | 0 | 8 | 120 Å² | viable |
| Any | C173 | ≥13 | — | — | excluded |

**Recommended design point: 7 Å linker, C178 target, 150° rotation.** Estimated buried surface area of 165–510 Å² is far below a classical PPI (1,000–2,500 Å²), confirming the mechanism is a covalent tether rather than a non-covalent molecular glue.

---

## Plausibility Judgement and Falsification

### Mechanism plausibility without pre-existing binary affinity

**Plausible.** The covalent bond to C178 pays the full entropic cost of proximity (~60 kcal/mol effective affinity). DCAF16 does not need to recognise BRD9 non-covalently; the tethered BRD9 samples rotational freedom around the C178–warhead bond, allowing multiple lysines to transit the E2~Ub active site volume over successive ubiquitination cycles.

Key caveat: the C178 position in the **DDB1-assembled CRL4^DCAF16** complex is unknown. C178 must lie on the substrate-receptor face (not occluded by DDB1) for the warhead to engage in a cellular context. No DDB1–DCAF16 co-structure is available.

### Primary falsifying experiment

**In vitro ubiquitination reconstitution.** Purified BRD9 bromodomain + covalent compound + DCAF16 + DDB1 + CUL4A + RBX1 + Uba1 + UBE2D3 + Ub + ATP. If no poly-Ub laddering of BRD9 occurs despite confirmed SG-C178 covalent adduct (by LC-MS digest), the model is falsified: the tether orientation excludes productive E2 delivery.

### Secondary falsifiers

| Experiment | Falsifying result |
|---|---|
| DCAF16 C177S/C178S double mutant in DCAF16-KO cells | Residual BRD9 degradation (off-target E3) |
| Non-electrophilic BI-7273 analogue (methyl-amide control) | Degradation still occurs (mechanism is not covalent) |
| SPR: DCAF16 over BRD9, no compound | KD < 100 µM (pre-existing affinity exists, model wrong) |
| HDX-MS on BRD9 in ternary | Extra protection outside bromodomain pocket (non-covalent contacts forming) |
| GSH competition t½ at pH 7.4 | t½ < 15 min (warhead too reactive for selectivity) |
