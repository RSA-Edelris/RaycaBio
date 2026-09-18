
import numpy as np
from Bio.PDB.SASA import ShrakeRupley

# ── Identify chains in 6BOY ───────────────────────────────────────────────────
m6 = s6[0]
print("6BOY chain COMPND titles:")
for line in pdb_6boy.split('\n'):
    if 'COMPND' in line or 'CHAIN' in line:
        print(' ', line.strip())
    if line.startswith('ATOM') and not any(line.startswith(k) for k in ('ATOM  ','ATOM   ','HETATM')):
        break

# chain C = BRD4-BD1 (confirmed); A+B = VHL complex
brd4_deg  = m6["C"]   # BRD4 BD1 being degraded
vhl_chain = m6["A"]   # VHL complex

# ── Run SASA on Chain C (BRD4 BD1 target) ────────────────────────────────────
sr = ShrakeRupley()
sr.compute(s6, level="R")

# ── Find VHL-complex surface (Chain A + B) as atom array ─────────────────────
vhl_atoms = np.array([
    a.coord for ch in [m6["A"], m6["B"]] for res in ch if res.id[0]==' '
    for a in res.get_atoms() if a.element not in ('H','')
])
print(f"\nVHL-complex heavy atoms: {len(vhl_atoms)}")

# PROTAC RN6 CoM already computed = [72.1, 38.7, 51.1]
rn6 = next((res for ch in m6 for res in ch if res.resname=="RN6"), None)
rn6_com = np.mean([a.coord for a in rn6.get_atoms()], axis=0) if rn6 else None
print(f"PROTAC (RN6) CoM: {rn6_com.round(2)}")

# ── Surface Lys on BRD4-BD1 (Chain C) ────────────────────────────────────────
print("\n=== BRD4 BD1 surface Lys in PROTAC ternary complex (6BOY, Chain C) ===")
print(f"{'Lys':>6}  {'SASA':>7}  {'Nz→VHL(Å)':>10}  {'Nz→PROTAC(Å)':>13}  {'in-window':>10}")
print("-"*60)

for res in sorted(brd4_deg.get_residues(), key=lambda r: r.id[1]):
    if res.id[0]!=' ' or res.resname!='LYS': continue
    sasa = res.sasa
    if sasa < 30: continue
    if 'NZ' not in res: continue
    nz = res['NZ'].coord
    d_vhl    = float(np.linalg.norm(vhl_atoms - nz, axis=1).min())
    d_protac = float(np.linalg.norm(nz - rn6_com)) if rn6_com is not None else float('nan')
    in_window = d_vhl <= 15.0   # ≤15 Å from E3 surface = in productive ubiquitination range
    print(f"  K{res.id[1]:>3}  {sasa:>7.1f}  {d_vhl:>10.1f}  {d_protac:>13.1f}  {'YES' if in_window else 'no':>10}")

# ── Key PROTAC geometry parameters ───────────────────────────────────────────
# Find the VHL-arm anchor of RN6 (closest RN6 atom to VHL chain A)
if rn6 is not None:
    rn6_atoms = np.array([a.coord for a in rn6.get_atoms()])
    # distance matrix RN6 atoms × VHL atoms (subsample VHL for speed)
    step = max(1,len(vhl_atoms)//200)
    d_rn6_vhl = np.linalg.norm(rn6_atoms[:,None] - vhl_atoms[::step][None,:], axis=2).min(axis=1)
    vhl_arm_idx  = int(np.argmin(d_rn6_vhl))
    vhl_arm_pos  = rn6_atoms[vhl_arm_idx]
    # BRD4 arm = furthest RN6 atom from VHL arm (approximation)
    brd4_arm_pos = rn6_atoms[np.argmax(np.linalg.norm(rn6_atoms - vhl_arm_pos, axis=1))]
    linker_span  = float(np.linalg.norm(brd4_arm_pos - vhl_arm_pos))
    print(f"\nPROTAC VHL-arm anchor:  {vhl_arm_pos.round(2)}")
    print(f"PROTAC BRD4-arm anchor: {brd4_arm_pos.round(2)}")
    print(f"PROTAC end-to-end span: {linker_span:.1f} Å")

# Orientation cone: for each productive Lys, measure approach angle
# (angle between Lys Cα→Nz and Nz→VHL-arm-anchor — a broad cone means tolerant orientation)
print("\n=== PROTAC approach-angle distribution for productive Lys ===")
for res in sorted(brd4_deg.get_residues(), key=lambda r: r.id[1]):
    if res.id[0]!=' ' or res.resname!='LYS': continue
    if res.sasa < 30 or 'NZ' not in res or 'CA' not in res: continue
    nz = res['NZ'].coord; ca = res['CA'].coord
    lys_ax = (nz-ca)/np.linalg.norm(nz-ca)
    if rn6_com is not None:
        d_vhl_min = float(np.linalg.norm(vhl_atoms - nz, axis=1).min())
        if d_vhl_min > 20: continue
        # angle between Lys axis and direction toward VHL interface
        nearest_vhl = vhl_atoms[np.argmin(np.linalg.norm(vhl_atoms - nz, axis=1))]
        nz_to_vhl   = (nearest_vhl - nz)/np.linalg.norm(nearest_vhl - nz)
        ang = float(np.degrees(np.arccos(np.clip(np.dot(lys_ax, nz_to_vhl),-1,1))))
        print(f"  K{res.id[1]:>3}  dist_VHL={d_vhl_min:.1f} Å  approach_angle={ang:.0f}° to nearest VHL atom")
