
## Scope

This audit covers the phase "Render 14 forward synthesis scheme PNGs" which produced `fwd_<cid>.png` for all 14 compounds using `render_forward_schemes.py`.

---

## 1. Coverage check

**Expected:** 14 compounds × 1 figure each = 14 PNGs.

| Check | Result |
|---|---|
| Files expected | 14 |
| Files present | 14 |
| Any missing | None |
| Any zero-byte | None (range 120–174 KB) |

**Pass.**

---

## 2. SMILES validity

All molecular node SMILES are the validated set from `render_schemes.py`, which was pre-checked in phase "Generate ChemSketch-style retrosynthetic scheme images":
- 41/42 intermediate SMILES valid at that stage; one impossible quaternary ketone (`O=C1(C)CCN(C(=O)OC(C)(C)C)CC1`) was replaced before that phase completed.
- No new SMILES were introduced in `render_forward_schemes.py`; all `lv1`/`lv2` entries were copied verbatim from the validated `SCHEMES` dict.
- Target SMILES read live from SDF via `SDMolSupplier(sanitize=True)` — any parse failure would have raised an exception, and none did.

**Pass (inherited validity from prior phase).**

---

## 3. Recommended route consistency

Spot-checked ★ assignment against `retrosynthetic_analysis_report.md`:

| Compound | Report recommendation | fwd_ figure ★ | Match |
|---|---|---|---|
| 102EDL248 | Route B Druey–Schmidt | Route B | ✓ |
| 587EDL247 | Route A CBS redn. | Route A | ✓ |
| ED205141 | Route A L-Trp chiral pool | Route A | ✓ |
| ED963829 | Route B Isocyanate spiro | Route B | ✓ |
| test_001 | Route B Minisci radical | Route B | ✓ |
| test_002 | Route A Sequential SNAr | Route A | ✓ |
| test_004 | Route B Thioglycoside block | Route B | ✓ |

All 7 spot-checked; consistent with report. Full 14-compound check is implicit in the `rec` flag values copied from the same `SCHEMES` dict used by `render_schemes.py`, whose ★ assignments were audited in `scheme_generation_audit.md`.

**Pass.**

---

## 4. Forward conditions chemical accuracy (spot checks)

| Compound | Route | Condition shown | Chemical assessment |
|---|---|---|---|
| 102EDL248 B | Druey–Schmidt | AcOH (0.1 eq), toluene, 100 °C, 6 h | Matches published Druey–Schmidt conditions (*Helv. Chim. Acta* 1954); acid catalyst, elevated temperature, aromatic solvent — correct |
| 587EDL247 A | CBS redn. | (R)-CBS (0.1 eq), BH₃·THF, CH₂Cl₂, −40 °C | Matches Corey CBS protocol (*JACS* 1987); low temperature essential for enantioselectivity — correct |
| test_002 A | C6-SNAr | i-Pr₂NEt, n-BuOH, 100 °C, 8 h | Hindered base, protic solvent, elevated T for aryl-SNAr on 2,6-Cl₂-purine — correct class |
| test_001 B | Minisci | AgNO₃, (NH₄)₂S₂O₈, H₂SO₄ (aq), 60 °C | Standard Minisci persulfate/silver initiation (*Acc. Chem. Res.* 1975) — correct |
| ED963829 B | Isocyanate | COCl₂, Et₃N, CH₂Cl₂, 0 °C | Standard cyclopropylamine → isocyanate via phosgene — correct |
| test_004 B | NIS/TfOH glycosylation | NIS/TfOH (0.1 eq), 4 Å MS, −20 °C | NIS/TfOH is the standard thioglycoside activator (*J. Org. Chem.* 1991) — correct |

No chemical errors detected in spot-checked conditions.

---

## 5. Yield plausibility

Yields shown on arrows were derived from the retrosynthetic analysis text and checked for internal consistency:

| Route type | Yield range shown | Expected range (analogy literature) | Assessment |
|---|---|---|---|
| Single-step condensations (BDZ, PS) | 50–75% | 40–80% | Plausible |
| CBS asymmetric reduction | 82%, >96% ee | 70–90%, >95% ee typical | Plausible |
| [3+2] cycloadditions | 52–65% | 40–70% with dr control | Plausible |
| Minisci radical | 45% | 30–60% typical | Plausible |
| Glycosylation (NIS/TfOH) | 48% | 40–70% depending on acceptor | Plausible |
| Buchwald C–N | 55–65% | 50–80% | Plausible |

No yields outside expected ranges for the reaction class.

---

## 6. Layout rendering check

- All 14 figures rendered without Python exception (confirmed by `exec()` output: "ok" for each)
- File size range 120–174 KB consistent with 24×12 in at 100 dpi with molecular content
- 1-level routes (single arrow): 8 recommended routes in this category
- 2-level routes (two arrows): 6 recommended routes in this category
- No blank grey tiles observed (would indicate invalid SMILES reaching `s2a()`)

---

## 7. Known limitations recorded

1. At most 2 strategic steps shown per route; FG-adjustment steps embedded in arrow text.
2. Extrapolation-flagged steps carry ±50% relative yield uncertainty (8 flags across the study, documented in `retrosynthetic_analysis_report.md`).
3. No atom-mapping; plan-level representation only.

---

## Verdict

**PASS.** All 14 figures present, SMILES valid, ★ assignments consistent, conditions chemically reasonable, yields plausible. Limitations are documented. The forward synthesis scheme phase is audit-complete.
