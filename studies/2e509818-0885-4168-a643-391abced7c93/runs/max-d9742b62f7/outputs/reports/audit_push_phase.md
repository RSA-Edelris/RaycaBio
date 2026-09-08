# Audit Report: Push Results to GitHub RSA-Edelris/RaycaBio

**Auditor:** Independent review agent  
**Date:** 2026-09-08  
**Files read:** `adme_models.py`, `results.sdf` (first 200 lines), `adme_scoring_report.md`, `source/004_write_all_adme_functions_module_file_they_persist.py`, `source/005_re_import_adme_models_persisted_disk.py`, `source/006_mpo_desirability_functions_rationale_weights_ppi.py`, `source/007_sdwriter.py`, `source/003_adme_descriptor_model_functions.py`, `reports/phase_01_push_results_to_github_rsa_edelris_raycabio.md`  
**RDKit version verified:** 2026.03.4

---

## CRITICAL — Invalidates results (wrong answers silently produced)

### C1. `n_basic_n` counts amide nitrogens as basic nitrogens

**File:** `adme_models.py`, lines 24–26 (also `source/004`, lines 26–28)  
**Code:**
```python
n_basic_n  = sum(1 for a in mol.GetAtoms()
                 if a.GetAtomicNum()==7 and not a.GetIsAromatic()
                 and not any(b.GetBondTypeAsDouble()==2 for b in a.GetBonds()))
```
**Finding:** The check `not any(b.GetBondTypeAsDouble()==2 for b in a.GetBonds())` only tests whether the nitrogen atom itself has a double bond. It does NOT test whether the nitrogen is adjacent to a carbonyl (i.e., whether it is an amide). In RDKit's representation, an amide nitrogen (N–C(=O)–) has a single bond to the carbonyl carbon — `GetBondTypeAsDouble()` returns 1.0 for that bond, so the check passes and the amide N is counted.

**Evidence:** Running the first compound from `results.sdf` (`CCOCC(=O)N1CCc2ccc(C(=O)NCc3ccccc3)nc2C1`) confirms `n_basic_n = 2`, counting N atom idx=6 and N atom idx=15. Both are confirmed amide nitrogens (each is bonded to a carbon that has a C=O to oxygen). `HERG_BASIC.HasSubstructMatch()` returns `False` for the same molecule, showing the SMARTS guard correctly rejects amide N — the fallback `d["n_basic_n"]>0` overrides the SMARTS.

**Propagation into results:**

1. **hERG risk** (`pred_herg`, lines 127–135): `bas = (HERG_BASIC and mol.HasSubstructMatch(HERG_BASIC)) or d["n_basic_n"]>0`. Because `HERG_BASIC.HasSubstructMatch()` is False (correct) but `d["n_basic_n"]>0` is True (incorrect), `bas=True` for every amide product in this series. Consequence: every compound with cLogP > 2.0 receives `herg_risk = "Medium"` regardless of whether it actually contains a basic nitrogen. The desirability score for "Medium" hERG is 0.5 vs 1.0 for "Low" (weight 2.0, the highest weight in the MPO). For all compounds where the true basic nitrogen count is zero, the MPO score is suppressed by up to (2.0 × 0.5)/10.0 = 0.10 units — a systematic 10-point downgrade in the highest-weighted endpoint.

2. **Metabolic clearance route** (`pred_met_stability`, line 72–77): `elif d["n_basic_n"]>=1 and d["n_ar_rings"]>=1: route = "CYP2D6/3A4 (basic-N + Ar)"`. Because `n_basic_n >= 1` from the amide N, and `n_ar_rings >= 1` from the scaffold pyridine ring, this branch fires for every product. The clearance route string "CYP2D6/3A4 (basic-N + Ar)" is written to every SDF record, attributing CYP2D6/3A4 oxidation to a motif (amide N near Ar) that is not a CYP2D6/3A4 substrate feature.

**Compounds affected:** All 353 products (all carry the ring amide nitrogen from the scaffold after amide-bond formation).

---

## MAJOR — May affect accuracy or reproducibility

### M1. Phase document exists but records no procedure

**File:** `reports/phase_01_push_results_to_github_rsa_edelris_raycabio.md`  
The document is present (contradicting the audit brief's premise). However, it states: "No method records were captured for this phase, so the procedure cannot be stated. This is a gap in the record, not a phase that did no work." and "No tool call is on record for this phase." The document lists 15 artifact hashes (including `results.sdf`, `adme_models.py`, `adme_scoring_report.md`) but contains no account of what commands were run, which repository branch was targeted, what git commit was made, whether the push succeeded, or what remote URL was used. The push cannot be verified or reproduced from this document alone.

---

### M2. Scaffold SMILES in the scoring report contains a boron atom

**File:** `adme_scoring_report.md`, line 10  
**Quoted line:** `**Scaffold amine SMILES:** \`O=C(NCc1cccbc1)c1ccc2c(n1)CNCC2\``

The fragment `c1cccbc1` contains 'b' (lowercase boron in SMILES notation), giving a six-membered ring with one boron atom. RDKit parses this as valid but canonicalises it to `c1cbccc1` — a boracyclic ring, not benzene. The correct benzene ring is `c1ccccc1`. The actual product SMILES in `results.sdf` (line 70) is `CCOCC(=O)N1CCc2ccc(C(=O)NCc3ccccc3)nc2C1`, confirming `c3ccccc3` (pure benzene) in the product. The erroneous scaffold SMILES in the report would confuse any reader attempting to reproduce the enumeration from the document.

---

### M3. hERG model citation "Redfern-2003 anchor" is incorrect for the thresholds used

**File:** `adme_models.py`, line 135  
**Quoted line:** `herg_model="Structural-alert + cLogP (Redfern-2003 anchor; ±1 class)"`  
(Same string appears in `source/004`, line 137.)

Redfern et al. 2003 (Cardiovasc Res 58:32–45) classifies 100 marketed drugs into five clinical TdP risk categories based on observed cardiac adverse events. The paper does not define SMARTS patterns or cLogP thresholds. The specific rules — cyclic tertiary non-amide N AND cLogP > 3.5 AND ≥1 Ar ring → High; any non-amide non-aromatic N AND cLogP > 2.0 → Medium — are heuristics from general hERG SAR knowledge with no stated training set or derivation. The citation implies those numerical thresholds originated in Redfern 2003; they did not. A reader attempting to retrieve and replicate the rule from that reference will find no cLogP cutoffs.

---

### M4. `except Exception` in row-building loop silently drops failing compounds

**File:** `source/005_re_import_adme_models_persisted_disk.py`, lines 14–33  
**Code:**
```python
try:
    d = adme.compute_base_descriptors(mol)
    ...
    rows.append(row)
except Exception as e:
    print(f"ERROR {p['cr_id']}: {e}")
```
Any compound that raises an exception during descriptor calculation or prediction is excluded from `rows` without raising a failure. The only record is a line printed to stdout; there is no structured error count, no assertion that `len(rows) == len(products)`, and no downstream check. If silent drops occurred in this run, the reported count of 353 scored compounds is lower than the 353 enumerated, but no warning appears in the SDF or report. (In this run, 353 passed, consistent with no exceptions — but the missing safeguard would not surface failures in a future rerun.)

---

### M5. `adme_models.py` is missing the Ar-CF3 labile pattern present in the development script

**File:** `adme_models.py` vs `source/003_adme_descriptor_model_functions.py`, line 75  
**Development version (003) line 75:**
```python
('c1cccc(C(F)(F)F)c1',  'Ar-CF3: generally stable but metabolite risk'),
```
The final module (`adme_models.py` / `source/004`) has only 5 LABILE_PATS and omits this pattern. Compounds bearing an Ar-CF3 group are not flagged in `met_flags`. The omission is undocumented.

---

## VERIFIED CORRECT

**V1. Phase document existence.** The audit brief states "No document exists for this phase." A document does exist: `reports/phase_01_push_results_to_github_rsa_edelris_raycabio.md`. The brief's premise is incorrect. What is missing is substantive content within that document (see M1).

**V2. SDF Rank field is 1-based.** `results.sdf` line 60–61 shows the first compound has `Rank = 1`. `source/007_sdwriter.py` line 9 uses `for rank, row in enumerate(top96, 1)`, explicitly starting at 1. No 0-based/1-based confusion.

**V3. Double-prefix key names are internally consistent (not a bug).** `source/005` prefixes each prediction dict's keys with the model name: `{f"sol_{k}": v for k,v in sol.items()}`, producing `sol_logS`, `sol_sol_ad`, `sol_sol_model`. Keys that already carried a prefix in the model function (e.g., `sol_ad`, `met_score`, `cyp_risk`, `pampa_cat`, `ppb_pct`, `herg_risk`) become doubled: `sol_sol_ad`, `met_met_score`, `cyp_cyp_risk`, `pampa_pampa_cat`, `ppb_ppb_pct`, `herg_herg_risk`. All three call sites (`005`, `006`, `007`) use these exact doubled names consistently. Confusing naming, but no mismatch.

**V4. All five rdMolDescriptors functions confirmed present in RDKit 2026.03.4.** `CalcNumHBD`, `CalcNumHBA`, `CalcNumRotatableBonds`, `CalcFractionCSP3`, `CalcNumAromaticRings` all appear in `dir(rdMolDescriptors)`. No function-not-found risk.

**V5. No bare `except:` in `adme_models.py`.** The SMARTS guard pattern `if pat and mol.HasSubstructMatch(pat)` is used consistently for all LABILE_PATS entries (line 61) and CYP_PATS entries (lines 101–102). No bare `except:` or `except Exception` swallowing errors inside the model functions themselves.

**V6. `linear_des` and `trapezoid_des` positional arguments are in the correct order at every call site.** Four call sites checked:
- `des_sol`: `linear_des(logs, -5.5, -3.0)` — lo_bad=−5.5 < hi_good=−3.0. Correct: lower logS is worse.
- `des_perm`: `linear_des(logpapp, -7.0, -5.5)` — lo_bad=−7.0 < hi_good=−5.5. Correct: lower logPapp is worse.
- `des_logp`: `trapezoid_des(clogp, 0.0, 2.0, 4.0, 5.5)` — 0.0 < 2.0 < 4.0 < 5.5. Strictly ascending.
- `des_mw`: `trapezoid_des(mw, 200, 400, 650, 850)` — 200 < 400 < 650 < 850. Strictly ascending.

No argument reversal found.
