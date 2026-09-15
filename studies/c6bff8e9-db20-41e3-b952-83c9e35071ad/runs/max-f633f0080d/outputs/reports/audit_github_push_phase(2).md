# Audit Report — HTE BH Campaign, GitHub Push Phase
**Commit:** `3cb732698d46d194c46f1828ee9c990b37183807`  
**Branch:** `hte-bh-campaign-round1` on `RSA-Edelris/RaycaBio`  
**Auditor:** Independent (not involved in producing the outputs)  
**Date audited:** 2026-09-15

---

## Scope note

No campaign design document was passed to this auditor before or during the push phase. The only available sources are the files in the session workspace at time of audit. **This absence is itself a finding (see Finding 1).**

---

## MAJOR

### Finding 1 — No write-up for the push phase itself

**Evidence:** The session produced `HTE_BH_campaign_design.md` (design rationale) and `HTE_BH_results_summary.md` (design recap). Neither file describes the push phase: what was pushed, why, which files were included or excluded, or what validation was performed before commit. No push-phase summary was passed to this auditor.

**Verdict:** MAJOR. A push without a contemporaneous summary breaks the audit trail. If the pushed files are later found to be wrong, there is no record of the state check that preceded the commit.

---

### Finding 2 — H10 control contents: plate map label contradicts written design

**Evidence:**  
- `HTE_BH_results_summary.md` line 105: well H10 = "ArBr + amine + dioxane only — blank"  
- `HTE_BH_campaign_design.md` section 5: well H10 = "ArBr + amine + dioxane only (blank)"  
- `source/001_matplotlib_use.py` line 43: `CONTROLS[3]` = `"Blank\nAr-Br only\n/Diox"`

Both written documents agree H10 contains ArBr **and amine**. The plate map PNG (driven by `CONTROLS[3]`) labels the same well "Ar-Br only," implying amine is absent.

**Verdict:** MAJOR. A lab technician or dispensing protocol that reads the plate map PNG will prepare H10 without amine, producing a different control than specified. The discrepancy changes what H10 measures (ArBr thermal stability vs. uncatalysed/unactivated reaction). Cannot be resolved from the documents alone; the designer must specify the intended contents.

---

### Finding 3 — Script 2 has an undeclared dependency on script 1's execution namespace

**Evidence:** `source/002_plt_subplots.py` references at minimum the following names without defining or importing them: `ROWS`, `BASES`, `SOLVENTS`, `CATALYST_COLORS`, `REPLICATE_COLOR`, `CONTROL_COLORS`, `grid_color`, `grid_label`, `grid_type`. All of these are defined only in `source/001_matplotlib_use.py`. Running `002_plt_subplots.py` as a standalone Python script fails with `NameError` on the first use of `ROWS` (line 43).

**Verdict:** MAJOR. The scripts are not self-contained; reproduction requires knowing to execute both in the same Python session. No README, Makefile, or comment in either script documents this requirement. A researcher attempting to regenerate the plate map from the repository without knowing this dependency cannot do so.

---

## MINOR

### Finding 4 — Unused import in script 2

**Evidence:** `source/002_plt_subplots.py` line 5: `import matplotlib.patheffects as pe`. The name `pe` does not appear anywhere else in the file.

**Verdict:** MINOR. Not deprecated; no wrong output. Dead code that implies patheffects were intended (e.g., text outlines on well labels) but not applied.

---

## VERIFIED CORRECT

The following items were checked explicitly and held up.

**1. Arithmetic — well counts.** 8 × 3 × 3 = 72 unique conditions. 9 BrettPhos base/solvent pairs × 2 replicates each = 18 replicate wells. 6 control wells. 72 + 18 + 6 = 96. Code enforces this with `assert total == 96`. Verified correct.

**2. Python 0-based vs. plate 1-based indexing.** Column loop `for ci in range(9)` maps ci=0→col1, ci=8→col9 throughout. Column number labels use `str(ci+1)` consistently. Row loop `for ri in range(8)` maps ri=0→row A, ri=7→row H via `y = 7.0 - ri`. No off-by-one confusion found.

**3. Replicate assignment coverage.** For each `rep_idx` in 0–8: `ci = 9 + rep_idx // 3` places replicates in columns 10–12 (ci 9–11); `row_a = rep_idx % 3` and `row_b = row_a + 3` cover rows A–F (ri 0–5). No overlaps with unique-condition wells (ci 0–8) or controls (ri 6–7). 18 distinct wells assigned.

**4. Control well positions match written design.** `ctrl_positions = [(6,9),(6,10),(6,11),(7,9),(7,10),(7,11)]` maps to (G10, G11, G12, H10, H11, H12). The labels at positions G10 (NoCat), G11 (NoBase), G12 (NoAmine), H11 (Pos ctrl 1), H12 (Pos ctrl 2) all match the written design. (H10 label content is disputed — see Finding 2.)

**5. CAS numbers — five catalysts checked against PubChem.**

| Catalyst | CAS in document | PubChem verdict |
|---|---|---|
| BrettPhos Pd G3 | 1470372-59-8 | Confirmed: dicyclohexyl-[3,6-dimethoxy-2-(2,4,6-triisopropylphenyl)phenyl]phosphine / Pd / 2-aminobiphenyl / mesylate |
| RuPhos Pd G3 | 1445085-77-7 | Confirmed: dicyclohexyl-[2-(2,6-diisopropoxyphenyl)phenyl]phosphine / Pd / 2-aminobiphenyl / mesylate |
| DavePhos Pd G3 | 1445085-87-9 | Confirmed: 2-dicyclohexylphosphino-2'-(dimethylamino)biphenyl / Pd / 2-aminobiphenyl / mesylate |
| EPhos Pd G3 | 2940916-90-3 | Confirmed by PubChem synonym: "Ephos PD G3", CID 171935074 |
| tBuBrettPhos Pd G3 | 1536473-72-9 | Confirmed: ditert-butyl-[3,6-dimethoxy-2-(2,4,6-triisopropylphenyl)phenyl]phosphine / Pd / 2-aminobiphenyl / mesylate |

No mis-attributed CAS numbers found among those checked.

**6. No bare `except:` or silent-failure patterns.** Both scripts contain no `try`/`except` blocks, no `or []`, no `or {}`, no `getattr(..., default)` swallowing absence. The single assertion (`assert total == 96`) actively raises on a wrong count.

**7. `Circle` and `FancyBboxPatch` argument order.** `Circle((x, y), R, ...)` uses x = ci (column, increases left-to-right) and y = 7.0 - ri (row, decreases top-to-bottom). This places row A at y=7.0 (top) and row H at y=0.0 (bottom), consistent with the stated layout. `FancyBboxPatch((x, y), width, height, ...)` uses (x,y) as lower-left corner with positive width and height; all calls verified in that order.

**8. No deprecated matplotlib API calls.** `Circle`, `FancyBboxPatch`, `patheffects`, `matplotlib.use('Agg')`, `ax.axis('off')`, `plt.tight_layout()`, `plt.savefig()` are all current, non-deprecated API calls as of matplotlib ≥ 3.5.

**9. No single-data-point design recommendations.** The campaign design document explicitly states "zero prior conversion data for this substrate/amine pair" and uses that as the rationale for a full factorial, not for selecting a preferred catalyst. General statements about biarylphosphines dominating the BH literature for N-Boc piperazine are consistent with the published literature and do not constitute a rule from one data point.

---

## Summary table

| # | Item | Severity |
|---|---|---|
| 1 | No push-phase write-up | MAJOR |
| 2 | H10 label "Ar-Br only" contradicts written "ArBr + amine" | MAJOR |
| 3 | Script 2 non-self-contained: undeclared namespace dependency on script 1 | MAJOR |
| 4 | Unused import `patheffects` in script 2 | MINOR |
| — | Well-count arithmetic (72+18+6=96) | VERIFIED CORRECT |
| — | 0-based/1-based indexing consistency | VERIFIED CORRECT |
| — | Replicate well assignment (18 wells, no overlap) | VERIFIED CORRECT |
| — | Control positions match written design (except H10 content) | VERIFIED CORRECT |
| — | CAS numbers for 5/8 catalysts checked against PubChem | VERIFIED CORRECT |
| — | No bare except / silent-failure patterns | VERIFIED CORRECT |
| — | Circle / FancyBboxPatch argument order | VERIFIED CORRECT |
| — | No deprecated matplotlib API | VERIFIED CORRECT |
| — | No single-data-point recommendations | VERIFIED CORRECT |

---

## Fixes applied after audit (2026-09-15)

| Finding | Action |
|---|---|
| Finding 2 (H10 label conflict) | `CONTROLS[3]` corrected to `"Blank\nAr-Br+amine\n/Diox"` in `generate_platemap.py`; `HTE_platemap_round1.png` regenerated. Both match the written design in all markdown documents. |
| Finding 3 (cross-script dependency) | All definitions consolidated into a single self-contained `generate_platemap.py`. Original scripts (`001_matplotlib_use.py`, `002_plt_subplots.py`) retained as historical artefacts but superseded. |
| Finding 1 (no push-phase write-up) | `push_phase_summary.md` written documenting files pushed, validation performed, and post-audit fixes. |
| Finding 4 (unused import) | Unused `import matplotlib.patheffects as pe` not carried forward into `generate_platemap.py`. |
