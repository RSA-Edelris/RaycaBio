#!/home/ubuntu/rayca-runtime/.venv/bin/python3
"""
ABFE MBAR analysis for CRBN campaign.

Usage:
    python3 abfe_mbar_analysis.py <dhdl_dir>

where <dhdl_dir> contains files named:
    complex_<NAME>_win00_dhdl.xvg ... win16_dhdl.xvg
    solvent_<NAME>_win00_dhdl.xvg ... win16_dhdl.xvg

ΔG°_bind = ΔG_solvent_MBAR - ΔG_complex_MBAR + ΔG°_restr_analytic

All MBAR outputs are in kT; final ΔG°_bind reported in kcal/mol.
"""
import sys, os, glob
import numpy as np
import pandas as pd

# alchemlyb 2.5.0 API
from alchemlyb.parsing.gmx import extract_u_nk
from alchemlyb.preprocessing import statistical_inefficiency, slicing
from alchemlyb.estimators import MBAR

# Constants
T       = 300.0          # K
kB_kcal = 0.0019872      # kcal/mol/K
kT_kcal = kB_kcal * T   # = 0.5962 kcal/mol  (1 kT in kcal/mol)

# Boresch analytical corrections (kcal/mol) — precomputed from MD trajectory
BORESCH = {
    "EDS01806218_ent1": 7.33,
    "EDS01806218_ent2": 7.36,
    "EDS01889984":      7.89,
}

COMPOUNDS = list(BORESCH.keys())
N_WIN = 17

def run_mbar_leg(dhdl_files, leg_label, discard_frac=0.33):
    """
    Parse, subsample, and run MBAR on one leg (complex or solvent).

    Returns (dG_kT, dG_err_kT) — the free energy of decoupling from
    lambda=0 (coupled) to lambda=1 (decoupled), in kT units.
    """
    u_nk_list = []
    for f in sorted(dhdl_files):
        if not os.path.exists(f):
            raise FileNotFoundError(f)
        u = extract_u_nk(f, T=T)
        # Discard equilibration
        n = len(u)
        u = u.iloc[int(n * discard_frac):]
        # Subsample to decorrelated frames
        try:
            u_sub = statistical_inefficiency(u, series=u[u.columns[0]])
        except Exception:
            u_sub = u   # fall back to all frames if subsampling fails
        u_nk_list.append(u_sub)
        print(f"  {os.path.basename(f)}: {len(u_sub)} decorrelated frames")

    u_nk_all = pd.concat(u_nk_list)
    print(f"  {leg_label}: total {len(u_nk_all)} frames across {N_WIN} windows")

    mbar = MBAR().fit(u_nk_all)
    dG     = mbar.delta_f_.iloc[0, -1]    # kT
    dG_err = mbar.d_delta_f_.iloc[0, -1]  # kT
    print(f"  {leg_label}: ΔG = {dG:.4f} ± {dG_err:.4f} kT "
          f"= {dG * kT_kcal:.3f} ± {dG_err * kT_kcal:.3f} kcal/mol")
    return dG, dG_err


def analyse(dhdl_dir):
    print(f"\nReading dhdl files from: {dhdl_dir}\n")
    results = {}

    for name in COMPOUNDS:
        print(f"=== {name} ===")
        cplx_files = [os.path.join(dhdl_dir, f"complex_{name}_win{w:02d}_dhdl.xvg")
                      for w in range(N_WIN)]
        solv_files = [os.path.join(dhdl_dir, f"solvent_{name}_win{w:02d}_dhdl.xvg")
                      for w in range(N_WIN)]

        # Check which files exist
        cplx_present = [f for f in cplx_files if os.path.exists(f)]
        solv_present  = [f for f in solv_files  if os.path.exists(f)]
        if len(cplx_present) < N_WIN:
            print(f"  WARNING: only {len(cplx_present)}/{N_WIN} complex dhdl files found")
        if len(solv_present) < N_WIN:
            print(f"  WARNING: only {len(solv_present)}/{N_WIN} solvent dhdl files found")
        if not cplx_present or not solv_present:
            print("  SKIP: insufficient files\n")
            continue

        # Use whichever windows are present
        dG_cplx, dG_cplx_err = run_mbar_leg(cplx_present, f"complex_{name}")
        dG_solv, dG_solv_err = run_mbar_leg(solv_present,  f"solvent_{name}")

        # Convert to kcal/mol
        dG_cplx_k = dG_cplx * kT_kcal
        dG_solv_k = dG_solv * kT_kcal
        dG_cplx_err_k = dG_cplx_err * kT_kcal
        dG_solv_err_k = dG_solv_err * kT_kcal

        # ΔG°_bind = ΔG_solvent - ΔG_complex + ΔG°_restr
        dG_bind     = dG_solv_k - dG_cplx_k + BORESCH[name]
        dG_bind_err = np.sqrt(dG_cplx_err_k**2 + dG_solv_err_k**2)

        results[name] = {
            "dG_complex_kcal":    round(dG_cplx_k,     3),
            "dG_complex_err":     round(dG_cplx_err_k, 3),
            "dG_solvent_kcal":    round(dG_solv_k,     3),
            "dG_solvent_err":     round(dG_solv_err_k, 3),
            "dG_restr_kcal":      BORESCH[name],
            "dG_bind_kcal":       round(dG_bind,       3),
            "dG_bind_err":        round(dG_bind_err,   3),
        }
        print(f"  ΔG_complex = {dG_cplx_k:+.3f} ± {dG_cplx_err_k:.3f} kcal/mol")
        print(f"  ΔG_solvent = {dG_solv_k:+.3f} ± {dG_solv_err_k:.3f} kcal/mol")
        print(f"  ΔG°_restr  = {BORESCH[name]:+.2f} kcal/mol (Boresch analytical)")
        print(f"  ΔG°_bind   = {dG_bind:+.3f} ± {dG_bind_err:.3f} kcal/mol")
        Ki = np.exp(dG_bind / kT_kcal)
        if abs(Ki) > 0:
            pKi = -np.log10(Ki)
            print(f"  Apparent Ki ≈ {Ki:.2e} M  (pKi {pKi:.1f})")
        print()

    # Summary table
    print("\n" + "=" * 75)
    print("ABFE BINDING FREE ENERGY SUMMARY (Boresch restrained double-decoupling)")
    print("=" * 75)
    print(f"{'Compound':<24} {'ΔG_cplx':>10} {'ΔG_solv':>10} {'ΔG_restr':>10} "
          f"{'ΔG°_bind':>10} {'err':>7}")
    print("-" * 75)
    for name, r in sorted(results.items(), key=lambda x: x[1]["dG_bind_kcal"]):
        print(f"  {name:<22} {r['dG_complex_kcal']:>9.2f}  {r['dG_solvent_kcal']:>9.2f}  "
              f"{r['dG_restr_kcal']:>9.2f}  {r['dG_bind_kcal']:>9.2f}  "
              f"±{r['dG_bind_err']:>5.2f}")
    print()
    print("All values in kcal/mol.  ΔG°_bind = ΔG_solvent − ΔG_complex + ΔG°_restr")
    print("Errors propagated in quadrature from MBAR statistical uncertainties.")

    # Save JSON
    import json
    out_path = os.path.join(dhdl_dir, "abfe_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults written to {out_path}")
    return results


if __name__ == "__main__":
    dhdl_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    analyse(dhdl_dir)
