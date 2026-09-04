# Phase 1 Retrosynthetic Analysis — Independent Audit Report

Auditor: Claude (independent check, no shared context with phase-1 writer)
Date: 2026-09-02
Source files read: `aizynthfinder-results.json`, `all_aiz_results.json`, `aiz_results_batch1.json`
SMILES parsed with: RDKit (run_python environment, results logged below)

---

## Preliminary finding — absence of a persistent document

**MAJOR**

The phase-1 output was delivered as inline chat text only. No standalone file (JSON, Markdown, PDF) was written that captures the analysis, route descriptions, numbered steps, or conclusions. This means:

- There is no file to diff against a prior version or a specification.
- Numbering errors cannot be caught automatically; they can only be discovered by re-reading the chat transcript.
- The analysis is not archivable or versioned. If the session is closed or the transcript scrolled past, the output is effectively lost.
- This audit itself (check 1, numbering) cannot be fully executed against a concrete document.

**Recommendation:** Require phase-1 agents to write a structured output file (e.g. `retrosynthesis_phase1.json` or `retrosynthesis_phase1.md`) before the phase closes.

---

## Check 1 — Index and numbering errors (1-based vs 0-based; step references)

**CANNOT FULLY VERIFY — no persistent document**

The analysis numbered routes 1/2/3 and steps 1/2/3/4/5 in inline chat text. Without a machine-readable file the only evidence available is the JSON data from AiZynthFinder runs. From `aizynthfinder-results.json`, routes are indexed `"rank": 1` through `"rank": 5` (1-based), consistent with what was reported. From `aizynthfinder-results-2.json` (A317), routes are ranked 1–3. No 0-based indexing was observed in the JSON outputs. However, the step numbering within manual route descriptions (B54, 8008, 7877, Mablink) cannot be verified from any file because those descriptions exist only in the chat transcript. This item remains **unresolved** pending a persistent document.

---

## Check 2 — Ring system nomenclature

### 2a. MCUF651: "4,6-difluorobenzothiazol-2-amine"

**VERDICT: VERIFIED CORRECT**

Leaf SMILES from `aizynthfinder-results.json` (all 5 routes share this precursor): `Nc1nc2c(F)cc(F)cc2s1`

RDKit ring analysis:
- Two rings detected: sizes [5, 6].
- 5-membered ring (atoms 1,2,3,10,11): symbols C, N, C, C, S — contains both S and N → benzothiazole confirmed.
- C2 (idx 1): bonded to N(amino), N(ring), S → position 2 (2-amino confirmed).
- 6-membered (benzo) ring traversal from C3a outward:
  - C3a (idx 3): F=False
  - C4  (idx 4): F=**True**
  - C5  (idx 6): F=False
  - C6  (idx 7): F=**True**
  - C7  (idx 9): F=False
  - C7a (idx 10): F=False

Fluorines are at C4 and C6. The name "4,6-difluorobenzothiazol-2-amine" is correct.

---

### 2b. A317: `c2ccccn2` — "pyridin-2-yl"

**VERDICT: VERIFIED CORRECT**

A317 SMILES: `O=C(Nc1nc([C@H]2CCCN2c2ccccn2)cs1)c1cccn1Cc1ccncc1`

RDKit analysis of the pyrrolidine N (idx 10) and its aromatic substituent:
- Pyrrolidine N (non-aromatic, in ring [7,6,10,9,8]) is bonded to aromatic C idx 11.
- Atom 11 belongs to pyridine ring [12,13,14,15,16,11] (symbols C,C,C,C,N,C).
- Pyridine N is at idx 16.
- Ring distance from attachment carbon (idx 11) to pyridine N (idx 16): **1 bond** (i.e., they are directly adjacent).

One bond from attachment carbon to pyridine N = **ortho** = pyridin-2-yl. The text is correct.

---

### 2c. 7977: "imidazo[4,5-c]pyridinone"

**VERDICT: VERIFIED CORRECT**

7977 SMILES: `Cc1cnc(-c2cc(Cl)ccc2F)cc1-n1c(=O)n(CC(N)=O)c2cnccc21`

RDKit ring analysis of the fused bicyclic fragment `-n1c(=O)n(CC(N)=O)c2cnccc21`:
- 5-membered ring: atoms (16,15,28,23,18), symbols C, N, C, C, N → two nitrogens, no oxygen, no sulfur.
- 6-membered ring: atoms (24,25,26,27,28,23), symbols C, N, C, C, C, C → one pyridine N.
- Junction atoms: 28 (C) and 23 (C) — **both carbons**, confirming imidazo[4,5-x] family (not imidazo[1,2-x] or [1,5-x] which would have N at a junction).
- Carbonyl (C=O) confirmed at atom 16 within the 5-membered ring.
- Pyridine N (idx 25) distances: 2 bonds from junction 23, 3 bonds from junction 28.

In imidazo[4,5-c]pyridine the pyridine N is at position 5, which is 2 bonds from the C3a junction and 3 from C7a. This matches exactly. "imidazo[4,5-c]pyridinone" is correct.

For completeness: imidazo[4,5-b]pyridine would show N 1 bond from one junction; that does not match.

---

### 2d. 7877: "oxazolo[4,5-c]pyridine"

**VERDICT: CRITICAL ERROR**

7877 SMILES: `Cc1cccc(-c2cnc3occ(-c4ccc(C(=O)O)c(C5CCCC5)c4)c3c2)c1`

RDKit ring analysis of the fused fragment `c2cnc3occ(...)c3c2`:
- 5-membered ring: atoms (10,9,27,12,11), symbols **O, C, C, C, C** — one oxygen, four carbons, **zero nitrogens**.
- 6-membered ring: atoms (7,8,9,27,28,6), symbols C, N, C, C, C, C — one pyridine N (idx 8).
- Junction atoms: 9 (C) and 27 (C).

**The 5-membered ring contains O but no N. It is a furan ring, not an oxazole.** An oxazole requires both O and N in the 5-membered ring. The text's label "oxazolo[4,5-c]pyridine" is wrong at the most fundamental level: the 5-membered ring lacks nitrogen entirely.

The correct ring-system family is **furopyridine** (furo[x,y-z]pyridine).

Determining the specific isomer from the RDKit distances:
- O (idx 10) to junction 9: **1 bond** in 5-ring → O is adjacent to junction 9 → junction 9 = C2 of furan (O1 is adjacent to C2 in furan O1-C2-C3-C4-C5).
- O (idx 10) to junction 27: 2 bonds → junction 27 = C3 of furan.
- Junction 9 (=C2 of furan) to pyridine N (idx 8): **1 bond** in 6-ring → junction 9 is adjacent to pyridine N → this is the [b] face of pyridine (bond between N1 and C2 in pyridine numbering = bond "a"; fusion at C2-C3 = bond "b").

Correct name: **furo[2,3-b]pyridine** (not oxazolo[4,5-c]pyridine). This is a two-component error:
1. Wrong ring type (furan stated as oxazole).
2. Wrong regiochemistry designation ([4,5-c] stated instead of [2,3-b]).

---

## Check 3 — AiZynthFinder JSON verification for MCUF651

**VERDICT: VERIFIED CORRECT**

Source file: `aizynthfinder-results.json`

| Claim | JSON value | Match? |
|-------|-----------|--------|
| `is_solved=True` | `"is_solved": true` (line 4) | YES |
| `top_score=0.994` | `"top_score": 0.994039853898894` (rounds to 0.994) | YES |
| `n_routes=5` | `"n_routes": 5` (line 6) | YES |
| Building block: 2-amino-4,6-difluorobenzothiazole | Leaf SMILES `Nc1nc2c(F)cc(F)cc2s1` in_stock=true, all 5 routes | YES |
| Building block: (R)-nipecotic acid | Leaf SMILES `O=C(O)[C@H]1CCCNC1` in_stock=true | YES |
| Building block: 2-bromo-N,N-dimethylethylamine | Leaf SMILES `CN(C)CCBr` in_stock=true | YES |

Statistics field also confirms: `"precursors_in_stock": "CN(C)CCBr, Nc1nc2c(F)cc(F)cc2s1, O=C(O)[C@H]1CCCNC1"`.

One minor note: the text names this building block "2-bromo-N,N-dimethylethylamine" whereas the IUPAC-preferred name would be "2-bromo-N,N-dimethylethan-1-amine" or colloquially "dimethylaminoethyl bromide." The SMILES `CN(C)CCBr` unambiguously supports the compound the text intended, so this is not a substantive error.

---

## Check 4 — B54: rc=None characterised as "timed out on two independent attempts"

**VERDICT: CRITICAL ERROR — mischaracterised failure mode**

Source files: `all_aiz_results.json` (B54 key) and `aiz_results_batch1.json` (B54 key, same data).

Exact B54 record from `all_aiz_results.json`:

```
rc:          null
error:       "input_file_not_staged"
duration_s:  0.0
image:       null
gpu:         false
summary:     "aizynthfinder was NOT dispatched: smiles='O=C(Nc1nc(/C=C/c2cn(C3CCCCC3)cn2)cs1)c1cccn1Cc1ccncc1'
              names a file that is not staged and does not exist, so the container would have failed to
              open it. No container was started and no time was spent."
unstaged:    [{"field": "smiles", "path": "O=C(Nc1nc(/C=C/c2cn(C3CCCCC3)cn2)cs1)c1cccn1Cc1ccncc1"}]
```

**What rc=None means here:** The dispatch wrapper sets rc=None when the container is *never started* — i.e., the pre-flight validation failed. The tool detected that the value passed as the `smiles` argument was being treated as a file path, and that file did not exist in the staged files list. The same record appears in both `aiz_results_batch1.json` and `all_aiz_results.json`, indicating a single failed attempt that was recorded twice in two aggregation files, not two independent runs.

**What the analysis claimed:** "B54 returned rc=None on two independent attempts" and concluded this indicated a timeout.

**Why this is wrong:**

1. `duration_s = 0.0` — zero seconds elapsed. A timeout would require the tool to run to completion of the timeout window (typically seconds to minutes) and exit with a signal-based rc (e.g., -9, 124) or a non-null rc. 0.0 s duration is physically incompatible with a timeout.
2. `image = null` — the container image was never pulled. AiZynthFinder was not invoked.
3. The error string explicitly says "No container was started and no time was spent."
4. The hint field explains the fix: pass the SMILES content via the `files` argument, not as a bare string that the tool would interpret as a filename.

**Consequence:** B54's synthesisability is completely unknown from the AiZ data. The phase-1 manual analysis for B54 was presented as a fallback after an AiZ failure, but the actual failure was a tool-invocation error that is trivially fixable. B54 should be re-submitted with the SMILES content properly staged.

---

## Check 5 — Hantzsch regiochemistry for A317 AiZ route

**VERDICT: CRITICAL ERROR in the analysis — the AiZ route is actually correct**

The analysis flagged "AiZ regiochemical error in A317," claiming that the AiZ-proposed haloketone `O=C(CBr)[C@H]1CCCN1c1ccccn1` would give a C5- not C4-substituted thiazole.

**Hantzsch 2-aminothiazole rule (well-established):**
In Hantzsch synthesis from alpha-haloketone R-C(=O)-CH2Br and thiourea:
- The **alpha-carbon bearing Br** (CH2Br) → becomes **C5** of the thiazole ring (sp2, unsubstituted if R2=H).
- The **carbonyl carbon** (bearing substituent R) → becomes **C4** of the thiazole ring (carries substituent R).

Reference example: phenacyl bromide (BrCH2-CO-Ph) + thiourea → 2-amino-4-**phenyl**thiazole (Ph at C4, not C5).

**Structural analysis of the AiZ haloketone** (RDKit, O=C(CBr)[C@H]1CCCN1c1ccccn1):

- Atom 1 (C): Carbonyl carbon — bonded to O(=O), CH2Br (idx 2), **and [C@H](pyrrolidinyl) (idx 4)**. This carbon bears the pyrrolidinyl substituent.
- Atom 2 (C): Alpha-carbon — bonded to carbonyl C (idx 1) and Br (idx 3), with 2 implicit H. **No pyrrolidinyl group here.**

Applying the Hantzsch rule:
- Alpha-C (idx 2, CH2Br, R=H) → C5 with H.
- Carbonyl C (idx 1, bearing pyrrolidinyl [C@H]) → C4 with pyrrolidinyl group.

**In the target A317** (`O=C(Nc1nc([C@H]2CCCN2c2ccccn2)cs1)...`), the thiazole ring is `nc([C@H]2...)cs` where the `c([C@H]2...)` is C4 and the `cs` part is C5-S. The pyrrolidinyl group is at **C4**. This is exactly what the AiZ haloketone would produce.

This conclusion is independently confirmed by the AiZ atom mapping in `all_aiz_results.json` (A317 Route 3): in the mapped reaction SMILES, `[C:6]` (the carbonyl carbon bearing `[C@H:7]1CCCN1...`) maps to `[c:6]` in the product, and `[c:6]` occupies the C4 position of the thiazole (adjacent to `[cH:18]` which is C5 and to `[n:5]` which is N3).

**The AiZ route does NOT have a regiochemical error.** The analysis incorrectly applied the Hantzsch rule — likely by confusing which carbon bears the Br (it confused the carbonyl C with the alpha-C, or applied the rule in reverse). The consequence is that a valid AiZ retrosynthetic route was incorrectly discarded.

---

## Check 6 — Stereocentre location in A317

**VERDICT: VERIFIED CORRECT**

A317 SMILES: `O=C(Nc1nc([C@H]2CCCN2c2ccccn2)cs1)c1cccn1Cc1ccncc1`

RDKit `FindMolChiralCenters`: one chiral centre, atom idx 6, configuration R.

- Atom 6 is in ring (7,6,10,9,8) with symbols C,C,N,C,C — a **pyrrolidine** ring (5-membered, one N, no S, no O). This is the pyrrolidine C2 position.
- Atom 6 is **not** in the thiazole ring (which has atoms 4,3,18,17,5 with symbols N,C,S,C,C — all aromatic, all sp2 hybridization).
- RDKit confirms every thiazole atom: `aromatic=True`, `hybridization=SP2`. An sp2 aromatic carbon cannot be a stereocentre.

The analysis statement "the stereocentre is on the pyrrolidine C2, not on the thiazole ring (which is aromatic/sp2 at C4)" is **correct**.

---

## Summary table

| # | Item | Verdict | Severity |
|---|------|---------|----------|
| 0 | No persistent document written for phase 1 | ERROR | MAJOR |
| 1 | Step/route numbering consistency | UNRESOLVABLE — no document | — |
| 2a | MCUF651: "4,6-difluorobenzothiazol-2-amine" | VERIFIED CORRECT | — |
| 2b | A317: `c2ccccn2` = pyridin-2-yl | VERIFIED CORRECT | — |
| 2c | 7977: "imidazo[4,5-c]pyridinone" | VERIFIED CORRECT | — |
| 2d | 7877: "oxazolo[4,5-c]pyridine" | **WRONG** — 5-membered ring is furan (no N), should be furo[2,3-b]pyridine | **CRITICAL** |
| 3 | AiZ JSON: is_solved, top_score, n_routes, building blocks | VERIFIED CORRECT | — |
| 4 | B54 rc=None = timeout | **WRONG** — rc=None means dispatch never started; error = input_file_not_staged; 0.0 s elapsed | **CRITICAL** |
| 5 | AiZ A317 "regiochemical error" | **WRONG** — AiZ route is correct; analysis misapplied Hantzsch rule | **CRITICAL** |
| 6 | Stereocentre on pyrrolidine C2, not thiazole C4 | VERIFIED CORRECT | — |

---

## Critical findings in detail

### CRITICAL-1: 7877 ring system misidentified (Check 2d)

The compound 7877 contains a **furo[2,3-b]pyridine** ring system. The phase-1 text called it "oxazolo[4,5-c]pyridine." This is wrong at two levels:

- **Level 1 (ring type):** Oxazole = 5-membered ring with one O and one N. RDKit finds the 5-membered ring has atoms (O,C,C,C,C) — one oxygen, four carbons, **zero nitrogen**. This is a furan ring.
- **Level 2 (regioisomer):** Even the regioisomer descriptor [4,5-c] does not match. The O is 1 bond from junction C2 and 2 bonds from junction C3 (furan [2,3] fusion), and the pyridine N is directly bonded to junction C2 (pyridine [b] face). Correct descriptor: furo[**2,3-b**]pyridine.

Any retrosynthetic strategy that builds an oxazolo ring (requiring C-N bond formation plus C-O bond formation in a 5-membered ring) would be entirely wrong for this substrate, which has no N in the fused 5-membered ring at all.

### CRITICAL-2: B54 AiZ failure mischaracterised as timeout (Check 4)

B54 was never submitted to AiZynthFinder. The SMILES string was passed directly to the tool dispatch but the tool framework interpreted it as a filename (because the field named `smiles` was expected to be a path to a file, not an inline string). The container was never pulled (`image: null`), never run (`duration_s: 0.0`), and the rc was null because the dispatch function returned before any subprocess was launched.

The analysis's conclusion ("AiZynthFinder cannot handle B54 within its timeout") is unsupported. The failure is a tool-calling error, not a computational limitation of AiZynthFinder. B54 should be resubmitted with SMILES staged as a file.

### CRITICAL-3: A317 AiZ regiochemical error flag is itself incorrect (Check 5)

The analysis flagged AiZ Route 1 for A317 as having "regiochemical error" and stated the proposed haloketone `O=C(CBr)[C@H]1CCCN1c1ccccn1` would give the wrong regioisomer. By Hantzsch rule (carbonyl C → C4; alpha-C bearing halogen → C5), the pyrrolidinyl group on the carbonyl C maps to C4 of the product thiazole, which is exactly where A317 requires it. The AiZ route is correct. The phase-1 analysis applied the Hantzsch rule in reverse and discarded a valid route.
