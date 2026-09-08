
## Objective

Select and validate the correct ChEMBL similarity search mechanism for retrieving structural analogs of the 6 PDK1 ligands as the data-collection step upstream of Tanimoto-weighted cross-target kinase inference.

---

## Container Tool Evaluation

The platform's `chembl` container tool (FPSim2, Morgan r=2 2048-bit, GPU-accelerated Tanimoto) was dispatched for all 6 compounds at threshold Tc ≥ 0.40.

| Compound | Hits returned |
|:---|:---:|
| BX912 | 0 |
| EL2003A | 0 |
| EL2003A-A2U1 | 0 |
| EL2003A-A4U1 | 0 |
| EL5001A | 0 |
| EL5003A | 0 |

Root cause identified from `chembl-results.json`: the tool's summary field reads *"0 hit(s) of 0 above threshold in a **38-compound** ChEMBL subset."* The baked image contains only 38 molecules — insufficient for any meaningful similarity search over novel pharmaceutical compounds.

**Decision: container tool is not viable for this task. Switched to ChEMBL REST API.**

---

## ChEMBL REST API Validation

Endpoint: `GET https://www.ebi.ac.uk/chembl/api/data/similarity/{smiles_encoded}/{threshold}.json`

**Separator format discovery:** The `molecule_chembl_id__in` batch filter requires **comma-separated** values. Semicolons and pipe characters return 0 results.

| Separator tested | Result |
|:---|:---|
| Semicolon (`;`) | 0 activities |
| Pipe (`\|`) | 0 activities |
| Comma (`,`) | Correct results |

**Single-compound validation (CHEMBL3916849, BX912 exact match):**
- Direct query without `__in`: 10 activities returned ✓
- Comma-separated `__in` with two IDs: 27 activities returned ✓

---

## Similarity Search Results (REST API, Tc ≥ 0.40)

| Compound | Analogs found | Top hit | Top Tc | Top hit name |
|:---|:---:|:---|:---:|:---|
| BX912 | 51 | CHEMBL3916849 | 1.000 | (BX912 itself — exact match) |
| EL2003A | 59 | CHEMBL3916849 | 0.757 | BX912 — confirms shared scaffold |
| EL2003A-A2U1 | 23 | CHEMBL3581165 | 0.500 | — |
| EL2003A-A4U1 | 24 | CHEMBL3581165 | 0.481 | — |
| EL5001A | 19 | CHEMBL3916849 | 0.481 | — |
| EL5003A | 5 | CHEMBL5088930 | 0.440 | — |
| **Total unique IDs** | **105** | | | |

The EL5003A analog set (5 hits) is the shallowest because the rigid trans-4-aminocyclohexyl linker replacing the flexible piperidine creates a distinct 3D footprint at Tc = 0.40–0.44.

---

## Output Files

| File | Description |
|:---|:---|
| `chembl-results.json` through `chembl-results-5.json` | Container tool raw output (38-compound subset, 0 hits each) |
| `similarity_hits.pkl` | Per-compound analog lists with Tanimoto scores from REST API |
| `chembl_activities_raw.parquet` | 1,294 raw ChEMBL activities for the 105 analogs |

---

## Verification

| Claim | Check | Result |
|:---|:---|:---|
| Container tool baked subset = 38 compounds | `chembl-results.json` summary field | "38-compound ChEMBL subset" ✓ |
| BX912 = CHEMBL3916849 | REST API similarity at Tc=1.000 | Exact SMILES match ✓ |
| EL2003A top analog = BX912 | Tc(EL2003A, BX912) via REST API | 0.757 ✓ |
| Comma delimiter required | Tested `;`, `|`, `,` against single-compound ground truth | Comma only ✓ |
| 105 unique analog IDs | `len(set.union(*[{h["chembl_id"] for h in v} for v in all_hits.values()]))` | 105 ✓ |
