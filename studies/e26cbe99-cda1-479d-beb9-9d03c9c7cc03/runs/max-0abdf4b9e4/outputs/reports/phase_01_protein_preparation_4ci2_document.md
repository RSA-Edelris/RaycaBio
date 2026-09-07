
## Objective

Download PDB 4CI2 (DDB1–CRBN–lenalidomide E3 ligase ternary complex), repair missing residues, assign protonation states at pH 7.4, identify the ligandable pocket, and produce a trimmed receptor ready for GPU docking.

---

## Methods

### 1.1 Structure download and inspection

PDB 4CI2 was downloaded from the RCSB PDB (resolution 3.0 Å). The raw file is `PB-20260903-4CI2_raw.pdb` (1.83 MB). The structure contains two protein chains (A: DDB1, B: CRBN thalidomide-binding domain) and the co-crystal ligand lenalidomide (LVY) in chain B.

REMARK 465 parsing revealed missing residues restricted to terminal His-tag and linker segments (negative sequence numbers or positions at chain ends). No internal loop gaps were present in the DDB1 or CRBN thalidomide-binding domains.

### 1.2 Receptor preparation (PDBFixer v1.12.0)

Preparation was performed as a Python library call (not a container dispatch) to preserve workspace file access:

```
fixer.findMissingResidues()
# Exclude terminal tag residues (seqno ≤ 0 or ≥ chain length)
fixer.findNonstandardResidues() → replaceNonstandardResidues()
fixer.removeHeterogens(keepWater=False)
fixer.findMissingAtoms() → addMissingAtoms()
fixer.addMissingHydrogens(7.4)
```

Output: `PB-20260903-4CI2_receptor.pdb` — 1 520 residues, 23 970 atoms, full DDB1–CRBN assembly, protonated at pH 7.4.

### 1.3 Pocket identification

fpocket was not available as a PyPI or system package. Instead, the CRBN IMiD binding site was identified directly from the co-crystal ligand LVY (lenalidomide). The geometric centre of all LVY heavy atoms was computed as the pocket centroid:

| Coordinate | Value (Å) |
| :--- | ---: |
| x | 84.80 |
| y | 154.94 |
| z | 13.24 |

The canonical tri-tryptophan basket (TRP382, TRP388, TRP402 in CRBN chain B) and the ASN351 H-bond anchor were confirmed as the key pharmacophoric residues of this site, consistent with the published lenalidomide binding mode.

### 1.4 Receptor trimming for docking

A 20 Å sphere centred on the pocket centroid was used to select 142 residues from chain B. The trimmed receptor was H-stripped for gnina docking input:

| File | Residues | Atoms | Use |
| :--- | ---: | ---: | :--- |
| `PB-20260903-4CI2_receptor_trimmed.pdb` | 142 | 2 262 | With H (MM-GBSA) |
| `PB-20260903-4CI2_receptor_trimmed_noH.pdb` | 142 | 1 140 | H-stripped (gnina input) |

An orphan TER record for chain A (which had no atoms in the trimmed file) was present in both files; this was corrected before any downstream energy calculation by filtering TER records with no preceding ATOM records on the same chain.

For MM-GBSA preparation, terminal capping was applied to the truncated chain using PDBFixer (`findMissingAtoms` + `addMissingHydrogens(7.4)`), producing `PB-20260903-4CI2_receptor_trimmed_capped.pdb` (142 residues, 2 265 atoms) with proper OXT on the C-terminal LEU and H1/H2/H3 on the N-terminal PHE.

---

## Results

| Output | Description |
| :--- | :--- |
| `PB-20260903-4CI2_raw.pdb` | Original RCSB download |
| `PB-20260903-4CI2_receptor.pdb` | Full assembly, PDBFixer-repaired, pH 7.4 |
| `PB-20260903-4CI2_receptor_noH.pdb` | Full assembly, H-stripped |
| `PB-20260903-4CI2_receptor_trimmed.pdb` | 20 Å pocket sphere, with H |
| `PB-20260903-4CI2_receptor_trimmed_noH.pdb` | 20 Å pocket sphere, H-stripped |
| `PB-20260903-4CI2_receptor_trimmed_capped.pdb` | Pocket sphere, terminal caps added |
| Pocket centre | x=84.80, y=154.94, z=13.24 Å (LVY centroid) |
| Key pocket residues | TRP382, TRP388, TRP402 (tri-Trp basket); ASN351 (H-bond anchor) |

---

## Limitations

- fpocket was unavailable; pocket definition relies on crystal ligand position, which is appropriate for a known IMiD binder but should be complemented by unbiased pocket detection for novel target exploration.
- Protonation states at the pocket histidines (HIS354, HIS378, HIS397) were assigned empirically by PDBFixer at pH 7.4; explicit pKa prediction (PROPKA) was not run.
- The trimmed receptor omits DDB1 chain A; long-range electrostatic effects from the full assembly are not captured in the docking calculation.
