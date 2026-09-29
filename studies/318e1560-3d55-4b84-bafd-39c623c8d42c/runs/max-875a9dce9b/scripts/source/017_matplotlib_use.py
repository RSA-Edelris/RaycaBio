
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

b = 1.5
d_bd1 = 5.6

def p_vec(d, n, b=1.5):
    sigma2 = n * b**2 / 3.0
    return (1/(2*np.pi*sigma2))**1.5 * np.exp(-d**2 / (2*sigma2))

alpha_mz1 = 31.0
p_mz1_ref = p_vec(5.0, 12)  # MZ1 reference

# Continuous sweep
ns = np.arange(1, 35, 0.5)
alphas = alpha_mz1 * np.array([p_vec(d_bd1, n) / p_mz1_ref for n in ns])

# Four linker points
ldata = [
    ("L1-short",   4,  1.52,  "#d62728"),
    ("L2-medium",  8,  16.92, "#ff7f0e"),
    ("L3-long",    12, 21.92, "#2ca02c"),
    ("L4-xlong",   18, 21.21, "#1f77b4"),
]

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

# ── Left: α_pred vs linker length ──
ax = axes[0]
ax.plot(ns, alphas, color='#555', lw=2, zorder=1, label='Gaussian-chain model')
ax.axvline(x=(d_bd1/b)**2, color='gray', ls='--', lw=1.2, label=f'n* = {(d_bd1/b)**2:.1f} (optimal)')
ax.axhline(y=alpha_mz1, color='purple', ls=':', lw=1.2, label=f'MZ1 α={alpha_mz1} (BD2 ref)')

for label, n, alpha, col in ldata:
    ax.scatter(n, alpha, color=col, s=130, zorder=5)
    ax.annotate(f'{label}\nα≈{alpha:.1f}', xy=(n, alpha),
                xytext=(n+0.8, alpha-3.5), fontsize=8.5, color=col,
                arrowprops=dict(arrowstyle='-', color=col, lw=0.8))

ax.set_xlabel('Linker heavy atoms (n)', fontsize=11)
ax.set_ylabel('Predicted α (relative to MZ1 BD2 baseline)', fontsize=10)
ax.set_title('BD1–VHL PROTAC: Cooperativity vs linker length\n(Gaussian chain, d=5.6 Å, calibrated to MZ1 α=31)', fontsize=9.5)
ax.set_xlim(0, 32); ax.set_ylim(0, 30)
ax.legend(fontsize=8.5, loc='upper right')
ax.grid(alpha=0.25)

# ── Right: strain ratio + α side-by-side ──
ax2 = axes[1]
labels   = [ld[0].replace('-', '\n') for ld in ldata]
alphas_v = [ld[2] for ld in ldata]
strains  = [d_bd1 / (ld[1]*b) for ld in ldata]
colors   = [ld[3] for ld in ldata]
x = np.arange(len(labels))
w = 0.35

bars1 = ax2.bar(x - w/2, alphas_v, w, color=colors, alpha=0.85, label='α_pred')
ax2b  = ax2.twinx()
bars2 = ax2b.bar(x + w/2, strains, w, color=colors, alpha=0.4, hatch='//', label='strain ratio')
ax2b.axhline(1.0, color='red', ls='--', lw=1.0, label='fully extended')
ax2b.set_ylabel('Strain ratio (d/max_ext)', fontsize=10)
ax2b.set_ylim(0, 1.4)
ax2.set_xticks(x); ax2.set_xticklabels(labels, fontsize=9)
ax2.set_ylabel('Predicted α', fontsize=10)
ax2.set_title('Linker ranking: cooperativity (bars) vs strain (hatched)', fontsize=9.5)
ax2.set_ylim(0, 30)
h1 = mpatches.Patch(color='gray', alpha=0.85, label='α_pred')
h2 = mpatches.Patch(color='gray', alpha=0.4, hatch='//', label='strain ratio')
h3 = mpatches.Patch(color='red', label='strain=1 (full ext.)')
ax2.legend(handles=[h1,h2,h3], fontsize=8.5, loc='upper left')
ax2.grid(alpha=0.2, axis='y')

plt.tight_layout()
fig_path = work_dir / "brd4bd1_vhl_linker_ranking.png"
plt.savefig(fig_path, dpi=150, bbox_inches='tight')
plt.close()
print(f"Figure saved: {fig_path}")
