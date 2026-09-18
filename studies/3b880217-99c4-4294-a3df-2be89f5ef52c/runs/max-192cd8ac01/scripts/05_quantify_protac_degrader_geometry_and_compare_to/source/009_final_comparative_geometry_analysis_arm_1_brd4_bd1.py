
import numpy as np

# ═══════════════════════════════════════════════════════════════════════════════
# FINAL COMPARATIVE GEOMETRY ANALYSIS
# Arm 1: BRD4 BD1 reads a BCL6-BTB acetyl-Lys (bromodomain insertion mode)
# Arm 2: CRBN/E3 ubiquitinates BRD4-BD1 surface Lys (PROTAC degrader mode)
# ═══════════════════════════════════════════════════════════════════════════════

sep = "═"*70

# ── A. BRD4 BD1 POCKET: measured parameters ──────────────────────────────────
# From 3P5O analysis
pocket_depth_asn140  = 4.47   # Å: Kac Nz → Asn140 ND2 (H-bond chain anchor)
pocket_entrance_span = 15.4   # Å: Tyr97 OH – Trp81 NE1
brd4_entrance_d      = 5.37   # Å: nearest BRD4 entrance-side atom (Leu94 CD1) to Kac-Nz
# Half-angle of acceptable approach: ≈ atan(pocket_entrance_span/2 / pocket_depth_asn140)
half_angle_bd = np.degrees(np.arctan(pocket_entrance_span/2 / pocket_depth_asn140))

# ── B. PROTAC: measured from 6BOY ─────────────────────────────────────────────
protac_lys_dist = [8.6, 9.0, 5.9, 10.1, 11.2, 4.9, 8.7]   # productive Lys → E3 surface
protac_angles   = [87, 144, 64, 39, 62, 104, 90]            # approach angles (°)
n_productive_protac = 7

# ── C. BCL6 BTB candidate Lys summary ─────────────────────────────────────────
bcl6_lys = [
    dict(rn=66,  sasa=93,  protrusion=2.24, deficit=3.14, bfac_nz=101.0, verdict="BLOCKED"),
    dict(rn=123, sasa=123, protrusion=0.11, deficit=5.26, bfac_nz=105.3, verdict="BLOCKED"),
    dict(rn=126, sasa=176, protrusion=5.33, deficit=0.05, bfac_nz=126.3,
         verdict="BORDERLINE (flexible C-term tail)"),
]

print(sep)
print("GEOMETRY COMPARISON: BRD4 BD1 bromodomain reading  vs.  PROTAC ubiquitination")
print(sep)

print("\n── 1. BCL6-BTB surface Lys candidates ──")
print(f"{'Lys':>5}  {'SASA(Å²)':>8}  {'protrusion':>10}  {'deficit':>8}  {'B-Nz':>6}  verdict")
for l in bcl6_lys:
    print(f"  K{l['rn']:<3}  {l['sasa']:>7.0f}   {l['protrusion']:>8.2f} Å   {l['deficit']:>6.2f} Å  {l['bfac_nz']:>5.1f}  {l['verdict']}")

print(f"""
── 2. BRD4 BD1 bromodomain insertion (BCL6-Kac → BD1 pocket) ──
   a) DISTANCE: Kac-Nz must sit {pocket_depth_asn140:.1f} Å from Asn140-ND2 (at H-bond reach of acetyl C=O)
                BRD4 entrance-side atoms (Leu94/Pro82) are {brd4_entrance_d:.1f} Å from the Kac-Nz anchor
                → BCL6 Lys-Nz must protrude ≥{brd4_entrance_d:.1f} Å axially above the BCL6 surface
   b) ORIENTATION: must enter within ≈{half_angle_bd:.0f}° of the pocket axis (pocket span/depth constraint)
   c) PREREQUISITE: Lys must be acetylated before reading is possible
   d) DESIGN CONFLICT: if the heterobifunctional molecule uses BD1 as BRD4 recruitment handle,
                       the BD1 pocket is BLOCKED by the JQ1-arm → reading and recruitment
                       cannot coexist on the same domain; BD2 or a non-BD surface must be used
   e) BCL6 VERDICT per Lys:
       K66 (SASA=93):  protrusion 2.24 Å, need 5.37 Å → clash deficit 3.14 Å → BLOCKED
       K123 (SASA=123): protrusion 0.11 Å, need 5.37 Å → clash deficit 5.26 Å → BLOCKED
       K126 (SASA=176): protrusion 5.33 Å, need 5.37 Å → clash deficit 0.05 Å → BORDERLINE
           ↳ K126 B-factor(Cα/Nz)=72/126 → likely disordered C-terminal tail →
             conformational sampling may clear the 0.05 Å deficit, but only for this residue
""")

print(f"""── 3. PROTAC ubiquitination (CRBN-based, measured from 6BOY) ──
   a) DISTANCE: productive Lys Nz range = {min(protac_lys_dist):.1f}–{max(protac_lys_dist):.1f} Å from E3 substrate-receptor surface
                ({n_productive_protac} of 11 surface Lys qualify at ≤15 Å threshold)
   b) ORIENTATION: approach angles observed = {min(protac_angles)}°–{max(protac_angles)}°  (mean {np.mean(protac_angles):.0f}°)
                   No preference for a specific direction — E2~Ub swings freely on the RING
   c) PREREQUISITE: none — native unmodified Lys sufficient
   d) DESIGN CONFLICT: none — PROTAC recruits E3 to target via a separate binding site;
                        the Lys ubiquitination machinery is entirely on the E3/E2 side
""")

print(sep)
print("WHICH CONSTRAINT IS HARDER?")
print(sep)
print(f"""
Metric                           BRD4 BD reading           PROTAC ubiquitination
─────────────────────────────────────────────────────────────────────────────────
Productive Lys on BCL6 BTB      1* (K126, borderline)      3 (K66, K123, K126)
Required protrusion above surf  ≥ 5.37 Å (axial)          ~0 Å (any SASA>0)
Distance tolerance              ~0 Å slack (0.05 Å margin) 5–15 Å wide window
Approach cone half-angle        ≤ {half_angle_bd:.0f}° (narrow pocket)     39–144° (unconstrained)
Prerequisite modification        Acetylation                None
Recruitment handle conflict      YES (BD1 = drug site)      No
Transfer depth into active site  4.5 Å insertion (Kac→Asn) ~5 Å (Lys Nz→E2 Cys)
─────────────────────────────────────────────────────────────────────────────────
* K126 only, requires C-terminal disorder and a dedicated acetylation step

VERDICT: BRD4 bromodomain insertion is the harder constraint — by a large margin.

The fundamental asymmetry is geometric, not chemical:
  • Ubiquitination needs PROXIMITY (Lys Nz within 5–15 Å of E3, any orientation).
  • Bromodomain reading needs INSERTION: the Kac must physically thread ≥4.5 Å inside
    the pocket through a 15.4 Å entrance, requiring the Lys to protrude ≥5.37 Å above
    the BCL6 surface along the pocket axis — a clearance that only the disordered C-
    terminal K126 approaches (and even then only within 0.05 Å of the steric limit).
  Rigid BCL6 BTB residues K66 and K123 fall short by 3.1–5.3 Å; no linker chemistry
  resolves a protein-body steric clash of that magnitude.

Additional compounding factors for the bromodomain mode (none apply to PROTAC):
  1. Acetylation prerequisite (adds a separate enzymatic step)
  2. Recruitment-handle conflict (BD1 used for both drug binding AND reading)
  3. Transfer depth is comparable (4.5 Å vs ~5 Å) yet the approach geometry is far
     narrower (±{half_angle_bd:.0f}° cone vs essentially 4π steradians for PROTAC)
""")
