
## Summary

Fetched PDB structures 5MW2 (BCL6 BTB domain + BI-3802 / U52) and 3P5O (BRD4 BD1 + EAM inhibitor) from the RCSB via HTTP. Confirmed chain composition, residue ranges, ligand identities, heavy-atom counts, and centres of mass for both bound small molecules. Results defined the two anchor sites for the heterobifunctional molecule designed in this study.

**Script:** `source/001_warnings_filterwarnings.py`

---

## Procedure

1. Fetch 5MW2 and 3P5O PDB text via `requests.get` (30 s timeout, `raise_for_status`).
2. Parse both with `Bio.PDB.PDBParser(QUIET=True)`.
3. For each structure, iterate chains in model 0; separate ATOM (protein) from HETATM (ligand/ion) records by `residue.id[0]`.
4. For protein chains: record residue count and residue-number range.
5. For hetero residues (excluding waters `id[0]=='W'`): compute heavy-atom count (`element != 'H'`) and centre of mass as the mean of all atom coordinates.
6. Print TITLE record, chain summary, and per-ligand report.

---

## Results

### 5MW2 — BCL6 BTB domain + BI-3802

| Property | Value |
| :--- | :--- |
| Chain | A |
| Residues | 122 aa (A7–A128) |
| Ligand | U52 (BI-3802) |
| U52 heavy atoms | 34 |
| U52 centre of mass | [13.66, 17.40, 14.07] Å |

U52 occupies the lateral corepressor-binding groove of the BTB domain. Its CoM defines the BCL6-arm anchor for the heterobifunctional molecule (Arm 1).

### 3P5O — BRD4 BD1 + EAM inhibitor

| Property | Value |
| :--- | :--- |
| Chain | A |
| Residues | 127 aa (A42–A168, full-length BRD4 numbering) |
| Ligand | EAM (Kac-pocket inhibitor) |
| EAM heavy atoms | 30 |
| EAM centre of mass | [26.29, 50.72, −2.12] Å |
| Co-crystallised cryo-protectant | EDO × 4 (excluded from analysis) |

EAM occupies the acetyl-lysine reading pocket. Its CoM is 6.0 Å from Asn140 ND2 (the Kac H-bond acceptor) and served as the initial anchor estimate for Arm 2. Subsequent phases refined this to the Kac-Nζ position at 4.5 Å from Asn140 ND2, derived from the canonical Kac-peptide/BD1 H-bond geometry.

---

## Interpretation

The U52 and EAM CoMs define the two binding-site anchor points whose separation dictates the minimum linker length for the heterobifunctional molecule. U52 CoM lies within the BCL6 BTB lateral groove; EAM CoM lies within the BRD4 BD1 Kac pocket. The vector between these two anchors, when threaded through a linker, must bridge the gap without steric conflict — a constraint analysed in Phases 3–4.

---

## Environment

| Property | Value |
| :--- | :--- |
| Host | platform.europe-north1-a.c.project-s-496512.internal |
| Platform | Linux-6.17.0-1022-gcp-x86_64-with-glibc2.39 |
| Python | 3.12.3 |
| Key libraries | BioPython (PDBParser), requests, NumPy |

---

## References

- PDB 5MW2: Kerres, N. et al. (2017). Chemically induced degradation of the oncogenic transcription factor BCL6. *Cell Rep* 20, 2860–2875.
- PDB 3P5O: Filippakopoulos, P. et al. (2010). Selective inhibition of BET bromodomains. *Nature* 468, 1067–1073.
