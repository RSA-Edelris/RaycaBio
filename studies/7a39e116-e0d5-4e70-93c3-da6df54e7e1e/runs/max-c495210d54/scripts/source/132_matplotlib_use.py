
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# ── Clinical annotation for each kinase ─────────────────────────────────────
FAMILY = {
    "AurA":"Other","FLT3":"TK","JAK2-b":"TK","FGFR1":"TK","MET":"TK",
    "CDK4":"CMGC","BRAF":"TKL","EGFR":"TK","ROCK2":"AGC","p38a":"CMGC",
    "ROCK1":"AGC","BTK":"TK","SRC":"TK","CDC2":"CMGC","KDR":"TK",
    "CDK2":"CMGC","ABL1":"TK","PKN1":"AGC","PKACa":"AGC","CHK1":"CAMK",
    "MAP2K1":"STE","Erk2":"CMGC","CDK6":"CMGC","PKCt":"AGC","MRCKb":"AGC",
    "CHK2":"CAMK","PKCi":"AGC","AKT1":"AGC","RSK2":"AGC","p70S6K":"AGC",
    "YANK1":"AGC","PKG1":"AGC","JNK1":"CMGC","GPRK5":"AGC","NDR1":"AGC",
    "GSK3B":"CMGC","PKCh":"AGC","PLK1":"Other","AKT2":"AGC","BARK1":"AGC",
    "CK1d":"CK1","Erk1":"CMGC","PDK1":"AGC",
}
FAMILY_COLOR = {
    "AGC":"#4a9eff","CMGC":"#f97316","TK":"#22c55e","TKL":"#a855f7",
    "CAMK":"#ec4899","STE":"#eab308","CK1":"#06b6d4","Other":"#ef4444",
}

# Sort kinases: PDK1 first, then by mean pIC50 descending
sorted_kins = ["PDK1"] + list(summary.index)  # summary already sorted by mean
mat = pivot[sorted_kins].copy()

# ── Heatmap ──────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(20, 5), facecolor="#0d1117")
ax.set_facecolor("#0d1117")

cmap = plt.cm.RdYlGn
norm = mcolors.Normalize(vmin=6.4, vmax=7.5)

im = ax.imshow(mat.values, aspect="auto", cmap=cmap, norm=norm, interpolation="nearest")

# Axes
ax.set_xticks(range(len(sorted_kins)))
ax.set_xticklabels(sorted_kins, rotation=45, ha="right", fontsize=7.5, color="white")
ax.set_yticks(range(len(compounds)))
ax.set_yticklabels(compounds, fontsize=9, color="white")

# Colour xtick labels by family
for i, kin in enumerate(sorted_kins):
    col = FAMILY_COLOR.get(FAMILY.get(kin,"Other"), "#aaa")
    ax.get_xticklabels()[i].set_color(col)

# Annotate cells
for r in range(len(compounds)):
    for c, kin in enumerate(sorted_kins):
        v = mat.iloc[r, c]
        if np.isnan(v): continue
        ax.text(c, r, f"{v:.2f}", ha="center", va="center",
                fontsize=5.5, color="black" if 6.65<v<7.3 else "white",
                fontweight="bold" if v >= 7.1 else "normal")

# Colour bar
cb = plt.colorbar(im, ax=ax, pad=0.01, fraction=0.015)
cb.set_label("pIC50 (DNN)", color="white", fontsize=9)
cb.ax.yaxis.set_tick_params(color="white")
plt.setp(cb.ax.yaxis.get_ticklabels(), color="white", fontsize=8)

# Family legend
handles = [matplotlib.patches.Patch(color=v, label=k) for k,v in FAMILY_COLOR.items()]
ax.legend(handles=handles, loc="upper right", bbox_to_anchor=(1.0, -0.55),
          ncol=4, fontsize=7.5, facecolor="#111", edgecolor="#333",
          labelcolor="white", title="Kinase family",
          title_fontsize=8)

ax.set_title("Kinome selectivity profile — 6 PDK1 ligands\n"
             "(sorted by mean pIC50 across all compounds; PDK1 = reference)",
             color="white", fontsize=11, pad=10)

plt.tight_layout(rect=[0, 0.10, 1, 1])
out_hm = f"{WS}/kinome_heatmap.png"
plt.savefig(out_hm, dpi=160, bbox_inches="tight", facecolor="#0d1117")
plt.close()
print("Saved:", out_hm)
import os; print(f"  {os.path.getsize(out_hm)/1024:.0f} KB")
