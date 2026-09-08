
import matplotlib, matplotlib.pyplot as plt, matplotlib.patches as mpatches
import numpy as np, pandas as pd
matplotlib.use("Agg")
WS = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777"

# ── Data ─────────────────────────────────────────────────────────────────────
targets = ["JAK3","BMX","IRAK4","IKKε","BTK","ITK","AurA ★","TBK1","LRRK2","STK17A","MARK4 ★"]
compounds = ["BX912","EL2003A","EL2003A-\nA2U1","EL2003A-\nA4U1","EL5001A","EL5003A"]
data_raw = [
    [8.05, 8.05, np.nan, np.nan, np.nan, np.nan],
    [np.nan, 8.35, np.nan, np.nan, np.nan, np.nan],
    [np.nan, 8.30, np.nan, np.nan, np.nan, np.nan],
    [7.57, 7.57, np.nan, np.nan, np.nan, np.nan],
    [7.57, 7.56, 6.84, np.nan, np.nan, np.nan],
    [np.nan, 7.36, np.nan, np.nan, np.nan, np.nan],
    [7.86, 7.86, 7.86, 7.86, 7.86, 7.86],
    [6.99, 7.05, 5.63, 5.63, 6.71, 6.03],
    [np.nan, 7.32, 7.32, np.nan, np.nan, np.nan],
    [6.91, 6.98, np.nan, np.nan, 7.20, 7.22],
    [6.40, 6.61, 6.47, 6.47, 6.74, 6.75],
]
mat = np.array(data_raw, dtype=float)

fig, ax = plt.subplots(figsize=(9, 6.5))
fig.patch.set_facecolor("#1a1a2e")
ax.set_facecolor("#1a1a2e")

cmap = plt.cm.RdYlGn
cmap.set_bad(color="#2d2d4e")
masked = np.ma.masked_invalid(mat)
vmin, vmax = 5.4, 8.5
im = ax.imshow(masked, cmap=cmap, vmin=vmin, vmax=vmax, aspect="auto")

# Cell labels
for i in range(mat.shape[0]):
    for j in range(mat.shape[1]):
        v = mat[i, j]
        if not np.isnan(v):
            col = "white" if (v < 6.2 or v > 7.9) else "#1a1a1a"
            ax.text(j, i, f"{v:.2f}", ha="center", va="center",
                    fontsize=8.5, fontweight="bold", color=col)

# Axes
compound_labels = ["BX912","EL2003A","EL2003A-\nA2U1","EL2003A-\nA4U1","EL5001A","EL5003A"]
ax.set_xticks(range(6)); ax.set_xticklabels(compound_labels, color="white", fontsize=9)
ax.set_yticks(range(len(targets))); ax.set_yticklabels(targets, color="white", fontsize=9)
ax.tick_params(colors="white", length=0)
for spine in ax.spines.values():
    spine.set_visible(False)

# Colorbar
cb = plt.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
cb.ax.yaxis.set_tick_params(color="white")
cb.ax.tick_params(labelcolor="white", labelsize=8)
cb.set_label("Inferred pIC50", color="white", fontsize=9)

ax.set_title("Similarity-Based Cross-Target Kinase Inference\n"
             "6 PDK1 Ligands  |  Tc ≥ 0.40  |  ★ = experimentally confirmed",
             color="white", fontsize=11, pad=12)

# Annotation band for confirmed targets
for i, t in enumerate(targets):
    if "★" in t:
        ax.add_patch(mpatches.FancyBboxPatch((-0.5, i-0.45), 5.97, 0.9,
            linewidth=1.2, edgecolor="#f0c040", facecolor="none",
            boxstyle="round,pad=0.02"))

plt.tight_layout()
fig.savefig(f"{WS}/similarity_inference_heatmap.png", dpi=160, bbox_inches="tight",
            facecolor=fig.get_facecolor())
plt.close()
print("Heatmap saved.")

# ── BX912 three-way comparison bar chart ─────────────────────────────────────
fig2, ax2 = plt.subplots(figsize=(8, 4))
fig2.patch.set_facecolor("#1a1a2e")
ax2.set_facecolor("#1a1a2e")

kinases_bar = ["PDK1","AurA","BTK","MARK4","TBK1","MARK3"]
dock_vals   = [6.893, 7.403, 7.053, np.nan, np.nan, np.nan]
inf_vals    = [7.161, 7.860, 7.569, 6.403, 6.987, 5.962]
exp_vals    = [np.nan, 7.860, np.nan, 6.471, 5.633, 5.477]

x = np.arange(len(kinases_bar))
w = 0.26
b1 = ax2.bar(x - w, dock_vals, w, label="KD2 Docking", color="#4e9af1", zorder=3)
b2 = ax2.bar(x,     inf_vals,  w, label="Tc-Weighted Inference", color="#f1a44e", zorder=3)
b3 = ax2.bar(x + w, exp_vals,  w, label="Experimental (ChEMBL)", color="#6ecf70", zorder=3)

ax2.set_xticks(x); ax2.set_xticklabels(kinases_bar, color="white", fontsize=10)
ax2.set_ylabel("pIC50", color="white", fontsize=10)
ax2.set_ylim(4.5, 9.0)
ax2.set_title("BX912: Docking vs. Similarity Inference vs. Experimental", color="white", fontsize=11)
ax2.tick_params(colors="white"); ax2.yaxis.set_tick_params(labelcolor="white")
for spine in ax2.spines.values(): spine.set_color("#444466")
ax2.set_facecolor("#1a1a2e")
ax2.grid(axis="y", color="#333355", zorder=0)
ax2.legend(fontsize=8.5, facecolor="#2a2a4a", labelcolor="white", edgecolor="#555577")

plt.tight_layout()
fig2.savefig(f"{WS}/bx912_docking_vs_inference_vs_exp.png", dpi=160, bbox_inches="tight",
             facecolor=fig2.get_facecolor())
plt.close()
print("Bar chart saved.")
