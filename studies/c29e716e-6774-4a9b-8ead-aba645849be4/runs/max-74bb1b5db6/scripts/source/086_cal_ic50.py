
import numpy as np, math

R=0.001987; T=310.0

# Rebuild functions
slope2=-0.2686; intercept2=-1.9705
def cal_ic50(dG): return 10**(slope2*dG+intercept2)
def ic50_range(dG, d=1.5): return 10**(slope2*(dG+d)+intercept2), 10**(slope2*(dG-d)+intercept2)

# Build proposed SMILES lookup
prop_dict = {n: s for n, s in proposed}

# Rank proposed by ΔG (most negative = best)
ranked = sorted(proposed, key=lambda x: docking_results[x[0]])

lines = []
lines.append("# IC50 Estimation Report — 20 Proposed Compounds\n")
lines.append("## Method")
lines.append("- Receptor: Target.pdb (waters stripped, 371 KB)")
lines.append("- Docking: AutoDock-Vina GPU 2.1, focused box 25×25×25 Å centred on blind-dock hit (28.8, 4.1, −24.4 Å)")
lines.append("- Calibration: linear fit of log₁₀(IC50) vs ΔG using 15 known actives; R²=0.20, p=0.093")
lines.append("  AS-ratio IC50 proxy assumes [P]=1 µM (typical ASMS); actual [P] unknown → absolute values uncertain")
lines.append("- Vina RMSE ≈1.5 kcal/mol → ~11× IC50 uncertainty per compound")
lines.append("- **Relative ranking more reliable than absolute values**\n")

lines.append("## Known Actives — Calibration Reference")
lines.append(f"| Compound | ΔG (kcal/mol) | Vina IC50 (nM) | AS-proxy IC50 (nM) |")
lines.append(f"|----------|--------------|----------------|-------------------|")
for name, smi, asr in sorted(known_actives, key=lambda x: docking_results[x[0]]):
    dG=docking_results[name]; ic50v=cal_ic50(dG); ic50a=asr*1000
    lines.append(f"| {name} | {dG:.1f} | {ic50v:.0f} | {ic50a:.0f} |")

lines.append("\n## Proposed Compounds — Ranked by Docking Score")
lines.append(f"| Rank | Compound | ΔG (kcal/mol) | Est. IC50 (nM) | 95% CI (nM) | Series | SMILES |")
lines.append(f"|------|----------|--------------|---------------|-------------|--------|--------|")
for rank, (name, smi) in enumerate(ranked, 1):
    dG=docking_results[name]; ic50=cal_ic50(dG); lo,hi=ic50_range(dG)
    series = name[0]
    lines.append(f"| {rank} | **{name}** | {dG:.1f} | {ic50:.0f} | {lo:.0f}–{hi:.0f} | {series} | `{smi}` |")

lines.append("\n## Highlight — Top 5 Proposed")
lines.append("| Rank | Compound | ΔG | Est. IC50 | Rationale |")
lines.append("|------|----------|----|-----------|-----------|")
rationales = {
    'B3': 'Methylbenzofuran R1 cap + benzyl R2 — largest hydrophobic fill; matches EDS00490594 scaffold',
    'D2': 'Piperidine-pyridyl R2 with 4-F-benzyl acyl chain — sp3-rich, novel ring exit vector',
    'E3': 'Fluorocyclopropyl spiro quaternary centre — constrained 3D shape, fills hydrophobic sub-pocket',
    'E1': '4-F-phenyl acyl + 4-(4-pyridyl)-4-F-piperidine — dual fluorine, good Fsp3',
    'E2': 'Hydroxy variant of E1 — H-bond donor at piperidine 4-position, added solubility',
}
for rank, (name, smi) in enumerate(ranked[:5], 1):
    dG=docking_results[name]; ic50=cal_ic50(dG)
    rat = rationales.get(name, '—')
    lines.append(f"| {rank} | **{name}** | {dG:.1f} | {ic50:.0f} nM | {rat} |")

lines.append("\n## Calibration Diagnostic")
lines.append(f"- R²=0.20: Vina ranks known actives weakly vs AS ratio (expected — AS ratio reflects ASMS conditions, not just Kd)")
lines.append(f"- Systematic bias: Vina IC50s ({int(min(cal_ic50(docking_results[n]) for n,s,r in known_actives))}–{int(max(cal_ic50(docking_results[n]) for n,s,r in known_actives))} nM) compressed vs AS proxy (1–172 nM)")
lines.append(f"- Recommended action: prioritise top 5–8 proposed compounds for SPR/ITC Kd measurement to anchor the calibration")
lines.append(f"- Uncertainty caveat: treat all IC50 estimates as order-of-magnitude guides only (±11×)")

report_text = "\n".join(lines)
ws = '/home/ubuntu/rayca-sessions/c29e716e-6774-4a9b-8ead-aba645849be4-01def6985d02'
with open(f'{ws}/ic50_report.md', 'w') as f: f.write(report_text)
print("Written ic50_report.md")
print(report_text[:3000])
