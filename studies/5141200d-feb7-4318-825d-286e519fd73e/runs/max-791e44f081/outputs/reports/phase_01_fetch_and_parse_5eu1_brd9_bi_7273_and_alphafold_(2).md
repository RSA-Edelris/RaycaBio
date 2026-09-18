
## Inputs

| Resource | URL / source | Status |
|---|---|---|
| 5EU1 PDB | `https://files.rcsb.org/download/5EU1.pdb` | Downloaded, 4,589 lines |
| DCAF16 AlphaFold | API query `https://alphafold.ebi.ac.uk/api/prediction/Q9NXF7` → v6 URL | Downloaded, 1,765 lines |

Note: the hard-coded v4 URL (`AF-Q9NXF7-F1-model_v4.pdb`) returns HTTP 404. The API must be queried first to resolve the current version; at time of this run that is **v6**.

## 5EU1 contents

- Two chains: A and B, both BRD9 bromodomain fragment (UniProt residues 14–134, 113 Cα per chain)
- Ligand: residue name **5SW** (BI-7273), 26 heavy atoms, at sequence position 201 in each chain
- No other non-solvent ligands
- Experiment: X-ray diffraction

Chain A was selected for all downstream geometry calculations.

## DCAF16 AlphaFold v6 summary

- Sequence: 216 residues
- pLDDT very high (>90): 0 residues (0%)
- pLDDT confident (70–90): 0 residues (0%)
- pLDDT low (50–70): 13 residues (6%)
- pLDDT very low (<50): 203 residues (94%)
- Mean pLDDT: 38.2; only confident stretch: residues 206–210 (5 res, avg 53.5)

**Interpretation:** AlphaFold is not failing; it is correctly reflecting that DCAF16 in isolation is intrinsically disordered. DCAF16 is a substrate receptor that requires DDB1 assembly to adopt a stable fold. All downstream coordinates carry this low-confidence caveat.

## Files produced

| File | Content |
|---|---|
| `5EU1.pdb` | Full 5EU1 asymmetric unit |
| `DCAF16_AF.pdb` | AlphaFold v6 model for Q9NXF7 |
| `DCAF16_pae.json` | Predicted aligned error matrix (v6) |
| `001_1_download_5eu1.py` | Download script |
| `002_scan_5eu1_already_memory_pdb_text_intact.py` | Chain/ligand inventory |
| `003_query_alphafold_api_q9nxf7_get_correct_download_url.py` | AF API query to resolve v6 URL |
