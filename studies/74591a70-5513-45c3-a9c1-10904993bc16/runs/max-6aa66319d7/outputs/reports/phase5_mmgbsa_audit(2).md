
## Status: In Progress

Topologies built locally; MD running on LUMI (job 21779205); MMPBSA.py analysis pending.

---

## Protocol

**Force field:** ff14SB (protein) + GAFF2 (ligand) + igb=5 GB implicit solvent  
**Charge method:** Gasteiger (`antechamber -c gas`) — AM1-BCC rejected 16/32 ligands because gnina SDF files carry implicit C-H bonds; sqm counts only explicit atoms and finds an odd electron total. Gasteiger bypasses sqm consistently for all 32.  
**ZN handling:** Single ZN at residue B1428 (20.5 Å from pocket, zero contacts) removed from receptor; tleap cannot type an isolated ZN without coordinating residues.

**MD settings:** 500-step minimisation → 10 000-step NVT MD (20 ps, dt=0.002), cut=12 Å, rgbmax=12 Å (reduces GB Born-radii cost ~2×), SHAKE on H-bonds, Langevin thermostat, 50 frames saved.

**MMPBSA.py:** igb=5, saltcon=0.10, startframe=1, endframe=50. No entropy term (congeneric series). Tested on 2-frame trajectory for EDEL-CRBN-0001: DELTA TOTAL = −42.0 ± 1.8 kcal/mol.

---

## Execution steps

| Step | Status |
|------|--------|
| antechamber -c gas (32 ligands) | **32/32 OK** |
| tleap topologies (ff14SB + GAFF2, no ZN) | **32/32 OK** (~2.65 MB complex.prmtop each) |
| Sander min + MD on LUMI (32 parallel CPUs) | **Running** — job 21779205 |
| MMPBSA.py analysis (32 compounds) | Pending |
| Combined docking + MM-GBSA ranking table | Pending |

---

## Issues and fixes

| Issue | Fix |
|-------|-----|
| sqm odd electrons for 16/32 ligands | Gasteiger charges (`-c gas`) bypass sqm |
| tleap fatal on isolated ZN | Remove ZN from receptor PDB |
| sander 585 ms/step | `rgbmax=12.0` reduces to 315 ms/step |
| MMPBSA.py `AMBERHOME` TypeError | Set `AMBERHOME` in subprocess env |
| MMPBSA.py `Unknown variable intdiel` | Remove intdiel/extdiel from `&gb` namelist |
| MMPBSA.py `Could not open complex_prmtop` | Use `-cp` flag + absolute paths; clean `_MMPBSA_*` temp files |

---

## Key files

- `mmgbsa/receptor_nozn.pdb` — ZN-stripped receptor
- `mmgbsa/{name}_ent/complex.prmtop` — 32 ff14SB+GAFF2 topologies
- `mmgbsa/run_mmpbsa.py` — validated MMPBSA.py analysis script
- `mmgbsa/collate_results.py` — final ranking table (runs after MMPBSA.py)

---

## Caveats

Gasteiger charges are less accurate than AM1-BCC for polar groups; systematic error expected to cancel within this neutral glutarimide series. MD length (20 ps) adequate for relative ranking; not converged for absolute affinities. No entropy correction. rgbmax=12 Å slightly reduces Born-radii accuracy for buried atoms.
