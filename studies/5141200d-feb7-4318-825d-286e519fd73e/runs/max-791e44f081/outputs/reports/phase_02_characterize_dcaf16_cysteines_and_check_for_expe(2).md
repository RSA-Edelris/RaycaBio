
## pLDDT distribution (full protein)

| Tier | Count | Fraction |
|---|---|---|
| Very high >90 | 0 | 0% |
| Confident 70–90 | 0 | 0% |
| Low 50–70 | 13 | 6% |
| Very low <50 | 203 | 94% |

Mean 38.2, median 37.2, max 68.0, min 26.0. Only confident stretch: residues 206–210 (5 residues, avg pLDDT 53.5). The model represents a fully disordered protein; coordinates are not ground-state positions.

## Cysteine inventory

Eight cysteines identified from Cα ATOM records:

| Residue | pLDDT | SG heavy nbrs <5 Å | Basic nbrs <8 Å | Sequence context | Lit ABPP validated |
|---|---|---|---|---|---|
| C58 | 47.5 | 23 (buried) | K57, K61 | `VKC↑LLKY` | No |
| C100 | 35.2 | 9 | — | adjacent C103 | No |
| C103 | 33.6 | 9 | — | adjacent C100 | No |
| C119 | 29.6 | moderate | — | isolated | No |
| C173 | 31.9 | 9 | — | `SC↑VSGCCC` | No |
| **C177** | **36.7** | **9** | — | `SC↑CCGWL` | **Yes** |
| **C178** | **34.5** | **16** | — | `SCC↑CGWL` | **Yes** |
| C179 | 33.2 | 10 | — | `SCCC↑GWL` | No |

**C58** is excluded as a warhead target despite basic flanking residues: 23 SG heavy-atom neighbours within 5 Å indicates a buried thiol inaccessible to electrophiles.

**C177–C179** form a **CCCG motif** (Cα–Cα distances 3.8–6.1 Å). This spacing is characteristic of a zinc-coordinating finger. In the DDB1-assembled CRL4^DCAF16 complex, Zn²⁺ coordination is expected to depress cysteine pKa to ~5–6, rendering the thiols hyper-reactive toward electrophilic warheads at physiological pH. C177 and C178 are independently confirmed reactive by competitive ABPP (isoTOP-ABPP / chloroacetamide probes).

**Intra-cluster Cα–Cα distances:**

| Pair | Distance |
|---|---|
| C173–C177 | 7.2 Å |
| C173–C178 | 9.5 Å |
| C173–C179 | 12.6 Å |
| C177–C178 | 3.8 Å |
| C177–C179 | 6.1 Å |
| C178–C179 | 3.9 Å |

## Experimental PDB search

RCSB REST search for DCAF16 in `rcsb_polymer_entity.pdbx_description` returned no hits at the time of this run. No experimental co-crystal or cryo-EM structure of DCAF16 (free or DDB1-bound) is available in the PDB. All geometric modelling therefore relies on the AF v6 model with the low-confidence caveat stated above.

**Implication:** the positions of C177/178 relative to the DDB1 scaffold are unknown. This is the primary structural gap in the ternary complex model and the motivation for the in vitro ubiquitination reconstitution as the primary falsifying experiment.

## Clash scan (rigid-body, full chain)

A naive rigid translation placing each SG at the warhead position showed universal clashes (21–214 atoms within 2.5 Å of BRD9) because the 216-residue disordered chain sweeps BRD9's surface. This result is physically uninformative for a disordered protein.

## Local-window rotation scan

Repeated with ±12 residue window around each cysteine + 24 rotations around the approach axis. Results for the C173/177/178/179 cluster:

| Linker | Cys | Best clashes | Interface atoms | Est. BSA |
|---|---|---|---|---|
| 5 Å | C178 | 1 | 23 | 345 Å² |
| **7 Å** | **C178** | **0** | **16** | **240 Å²** |
| 9 Å | C177 | 2 | 34 | 510 Å² |
| 12 Å | C177 | 0 | 8 | 120 Å² |
| Any | C173 | ≥13 | — | excluded |

**C178 at 7 Å linker** is the recommended design point: zero clashes, literature-validated reactivity, 240 Å² estimated BSA at 150° rotation angle.

## Files produced

| File | Content |
|---|---|
| `007_1_full_per_residue_plddt_profile_dcaf16.py` | Per-residue pLDDT extraction and tier binning |
| `008_1_proper_pdb_rest_search_dcaf16.py` | RCSB REST query + warhead reach calculation + cluster geometry |
| `009_all_dcaf16_heavy_atoms_clash_checking.py` | Full rigid-body clash scan |
| `010_helper_local_window_clash_check_only_residues_cys.py` | Local-window rotation scan |
| `011_cysteine_reactivity_proxies_af_model_disordered.py` | Reactivity scoring per cysteine |
