# Audit: Submit CDK2-CCNE MD Pilot to Isambard

**Audited files**

- `md_prep/inputs/run_md.sh`
- `md_prep/inputs/create_ndx.py`
- `md_prep/inputs/em.mdp`, `nvt.mdp`, `npt.mdp`, `md.mdp`
- `md_prep/inputs/EDS00495858_topol.top`
- `md_prep/inputs/protein_Protein_chain_A.itp` (first 30 lines + atom count)
- `md_prep/inputs/protein_Protein_chain_B.itp` (atom count)

**Reference document for this phase:** NONE. No phase specification document exists.
This is itself a finding — see below.

---

## Finding 0: No Phase Document

**Severity: prerequisite missing — this finding cannot be classified as CRITICAL/MAJOR because there is nothing to check claims against.**

There is no specification document for the phase "Submit CDK2-CCNE MD pilot to Isambard". The hardcoded atom counts in `create_ndx.py` (CHAIN_A_ATOMS, CHAIN_B_ATOMS), the compound selection, the box size, ion concentration, and the timestep choice are all implementation decisions that have no recorded source of truth. The single most consequential consequence of this gap is documented as Finding 1 below: the atom counts were derived from an undocumented observation on a structure that does not match the files actually being submitted.

---

## CRITICAL Findings

### Finding 1: CHAIN_A_ATOMS and CHAIN_B_ATOMS are wrong — all chain-based index groups corrupted

**File:** `md_prep/inputs/create_ndx.py`, lines 19–20

```python
CHAIN_A_ATOMS = 4859   # atoms in chain A from pdb2gmx
CHAIN_B_ATOMS = 4375   # atoms in chain B from pdb2gmx
```

**Actual counts measured from the ITP files in this submission:**

| Constant | Hardcoded | Actual (from ITP) | Error |
|---|---|---|---|
| CHAIN_A_ATOMS | 4859 | 4605 | +254 |
| CHAIN_B_ATOMS | 4375 | 4112 | +263 |

Verified by counting `[ atoms ]` section entries in:
- `protein_Protein_chain_A.itp`: **4605 atoms**
- `protein_Protein_chain_B.itp`: **4112 atoms**

The script assigns index groups by arithmetic on these constants:

```python
chain_a  = list(range(1, CHAIN_A_ATOMS + 1))                                # → atoms 1..4859  (wrong; should be 1..4605)
chain_b  = list(range(CHAIN_A_ATOMS + 1, CHAIN_A_ATOMS + CHAIN_B_ATOMS + 1))# → atoms 4860..9234 (wrong; should be 4606..8717)
```

Consequences:
- `ChainA_CDK2` contains 254 atoms that actually belong to chain B.
- `ChainB_CyclinE` starts 254 positions late, skipping the first 254 atoms of the real chain B, and extends 263 positions beyond the end of chain B into ligand/solvent atoms.
- `Protein_LIG` (prot_idx + lig_idx) is also corrupted because prot_idx derives from the wrong chain lists.
- All downstream analysis using these groups produces wrong results: inter-chain minimum distance (`mindist_chains.xvg`), per-chain SASA (`sasa_A.xvg`, `sasa_B.xvg`), and BSA.

This matches the "rule derived from a single data point" pattern: the constants were measured once from an observation on a protein structure that was not the one used in this run.

**Failure scenario:** All 18 systems complete MD without error. The CSV columns `mindist_mean_nm`, `mindist_std_nm`, and `bsa_mean_nm2` are computed from corrupted index groups and reflect neither chain A–chain B distance nor the correct buried surface area.

---

### Finding 2: `stats_xvg` silently converts any analysis failure into zeros

**File:** `md_prep/inputs/run_md.sh`, lines 135–139

```bash
stats_xvg() {
    awk '!/^[@#]/{s+=$2; s2+=$2*$2; n++} END{
        if(n>0){m=s/n; v=s2/n-m*m; printf "%.5f %.5f %d\n", m, (v>0?sqrt(v):0), n}
        else{print "0 0 0"}
    }' "$1" 2>/dev/null || echo "0 0 0"
}
```

There are three silent-zero paths:
1. `2>/dev/null` — hides the "No such file or directory" warning when the xvg file was never created.
2. `|| echo "0 0 0"` — if awk exits non-zero for any reason (file missing, permission error), emits zeros.
3. `else{print "0 0 0"}` — if the file exists but contains no data rows (only `#`/`@` header lines), emits zeros.

In all three cases the caller reads "0 0 0", assigns `R_MEAN=0`, `R_STD=0`, etc., and writes a row like:

```
EDS00495858,1,0.00000,0.00000,0.00000,0.00000,0.00000,0.00000,0.00000
```

into `md_results.csv`, which is indistinguishable from a compound whose ligand has 0 nm RMSD and 0 H-bonds. Any ranking or active-vs-inactive comparison that uses these columns treats a silently failed analysis as a perfect false positive.

**Failure scenario:** `gmx rms` fails for one active compound (e.g., due to the wrong LIG group index from Finding 1). `stats_xvg rmsd_lig.xvg` returns "0 0 0". The compound is recorded as RMSD=0.00000 nm, causing it to rank top in any RMSD-based stability metric.

---

## MAJOR Findings

### Finding 3: `gmx hbond` and `gmx sasa` use a new selection interface in GROMACS 2026; stdin pipe of bare group names is undocumented

**File:** `md_prep/inputs/run_md.sh`, lines 158–160, 168–173

The script uses the old-style stdin pipe:

```bash
echo -e "Protein\nLIG" | $GMX hbond -f md.xtc -s md.tpr -n analysis.ndx -num hbond_prot_lig.xvg ...
echo "ChainA_CDK2"     | $GMX sasa   -f md.xtc -s md.tpr -n analysis.ndx -o sasa_A.xvg ...
```

Confirmed by checking the locally installed GROMACS 2026.3 binary (`/home/ubuntu/rayca-runtime/.mamba/envs/rayca/bin.AVX2_256/gmx`):

- `gmx hbond` now uses a selection-language interface: `-r <selection>` (reference) and `-t <selection>` (target) are required named flags, not stdin group-number prompts.
- `gmx sasa` now requires `-surface <selection>`; `-output <selection>` is optional.

The old interface (pipe group numbers or names) was the GROMACS 4/5 convention. In GROMACS 2026, these tools are selection-based.

Whether the pipe approach works depends on whether:
1. GROMACS 2026.1 (the cluster binary) prompts interactively for required selections when `-r`/`-t`/`-surface` are omitted from the command line, and
2. Bare names like `LIG` and `ChainA_CDK2` are accepted as valid GROMACS selection expressions (index group names without the `group "…"` prefix).

`LIG` and `ChainA_CDK2` are NOT built-in GROMACS selection keywords. They are index group names. If the selection parser does not fall back to index groups for bare unquoted names, both tools would fail silently (with output swallowed by `2>&1 | tail -3`), and `stats_xvg` would return zeros as per Finding 2.

The documented correct usage for this cluster (GROMACS 2026.1-mpi) is:
```bash
$GMX hbond -r "Protein" -t "LIG" -f md.xtc -s md.tpr -n analysis.ndx -num hbond_prot_lig.xvg
$GMX sasa -surface "Protein" -output "ChainA_CDK2" -f md.xtc -s md.tpr -n analysis.ndx -o sasa_A.xvg
```

**Failure scenario:** `gmx hbond` errors because "LIG" is not a recognized selection expression. No `hbond_prot_lig.xvg` is created. `stats_xvg` returns "0 0 0". All 18 rows in the CSV have `hbond_mean=0, hbond_std=0` with no warning.

Note: there is no `|| exit 1` guard on the hbond command in `analyse_system`, compounding the silent failure.

---

### Finding 4: Topology file has two `[ system ]` / `[ molecules ]` sections

**File:** `md_prep/inputs/EDS00495858_topol.top`, lines 660–683

The topology contains:
- Line 660: `[ system ]` / line 663: `[ molecules ]` → lists only `EDS00495858 1` (orphaned standalone ligand block)
- Line 677: `[ system ]` / line 680: `[ molecules ]` → lists `Protein_chain_A 1`, `Protein_chain_B 1`, `EDS00495858 1` (correct full topology)

This is the result of embedding the standalone acpype/antechamber ligand topology without removing its terminal `[ system ]`/`[ molecules ]` section. GROMACS topology format specifies one `[ molecules ]` block. In GROMACS 2026.1, grompp behavior with two `[ molecules ]` blocks is: the second block overrides the first (so the correct molecules list is used), but `gmx solvate` and `gmx genion` append to the last `[ molecules ]` block they find, which is the correct one at line 680. This has likely worked in practice, but the first orphaned block is a latent risk:
- Any future grompp version may error on duplicate sections.
- The orphaned `EDS00495858 1` in the first block is never matched by a coordinate section and could confuse topology parsers.

**Failure scenario:** A grompp version upgrade causes grompp to error with "duplicate `[ molecules ]` section" before any MD runs.

---

## VERIFIED CORRECT

The following items were explicitly checked and held up:

1. **SEEDS array indexing** (`run_md.sh` line 65): `${SEEDS[$((REP-1))]}` with REP=1,2,3 correctly accesses 0-based bash array positions 0,1,2, giving seeds 1001/2002/3003 for replicas 1/2/3.

2. **`combine_gro` argument order** (lines 48–59, called at line 82): positional order `prot_gro=$1 lig_gro=$2 out_gro=$3` matches all call sites (`combine_gro protein.gro ${CID}.gro complex.gro`).

3. **`combine_gro` box vector** (line 58): taken from `prot_gro` (last line of protein.gro) — correct, since the box was defined on the protein.

4. **`gmx rms` group order** (lines 153–155): `Backbone` (fit group) then `LIG` (RMSD group) — correct order for measuring ligand RMSD after fitting to backbone.

5. **NVT timing**: 50 000 steps × 0.002 ps = 100 ps — matches stated 100 ps NVT equilibration.

6. **NPT timing**: 250 000 steps × 0.002 ps = 500 ps — matches stated 500 ps NPT equilibration.

7. **Production MD timing**: 5 000 000 steps × 0.002 ps = 10 ns — matches stated 10 ns production.

8. **EM convergence criterion**: `emtol = 100.0` in `em.mdp` — matches stated Fmax ≤ 100 kJ/mol/nm.

9. **nvt.mdp seed substitution** (lines 78–79): `nvt.mdp` is correctly excluded from the `cp` line and generated per-replica by `sed "s/SEED/${SEED}/"`. No replica shares a seed.

10. **`gmx hbond` command name**: Verified against GROMACS 2026.3 local binary — the tool is named `gmx hbond` (not `gmx hbonds`). Confirmed present and functional.

11. **`gmx hbond -num` flag**: Confirmed present in GROMACS 2026.3 — `-num [<.xvg>]` writes H-bond count vs. time.

12. **`gmx sasa -ndots 24 -probe 0.14`**: Both flags confirmed in GROMACS 2026.3 (`-ndots <int>` default 24, `-probe <real>` default 0.14). No regression.

13. **Ligand residue name**: `create_ndx.py` searches for residue name `"MOL"` (line 34). The topology atoms section confirms residue name `MOL` for all ligand atoms. Consistent.

14. **Thermostat groups `Protein`/`non-Protein`**: These are default GROMACS groups generated by `gmx make_ndx`. They are present in `default.ndx`, which `create_ndx.py` copies verbatim into `analysis.ndx`. `nvt.mdp`, `npt.mdp`, and `md.mdp` reference these groups — they will be found.

15. **BSA formula**: `(SASA_A + SASA_B - SASA_AB) / 2` is the standard buried surface area formula. Arithmetic is correct.

16. **`gmx mindist -od` flag**: Confirmed present in GROMACS 2026.3 synopsis — `-od [<.xvg>]` writes minimum distance.

---

## Summary Table

| # | Severity | Location | Issue |
|---|---|---|---|
| 0 | Missing prerequisite | — | No phase specification document exists |
| 1 | CRITICAL | `create_ndx.py` lines 19–20 | CHAIN_A_ATOMS=4859 (actual 4605, +254) and CHAIN_B_ATOMS=4375 (actual 4112, +263); all chain-based index groups corrupted |
| 2 | CRITICAL | `run_md.sh` lines 135–139 | `stats_xvg` returns "0 0 0" on file-not-found or empty file; failed analyses write fabricated zeros to CSV |
| 3 | MAJOR | `run_md.sh` lines 158–160, 168–173 | `gmx hbond` and `gmx sasa` use new selection interface in GROMACS 2026; stdin pipe of bare group names is undocumented and may silently fail for custom group names (LIG, ChainA_CDK2, etc.) |
| 4 | MAJOR | `EDS00495858_topol.top` lines 660–683 | Two `[ system ]`/`[ molecules ]` blocks; first is an orphaned standalone ligand section that should have been removed |
