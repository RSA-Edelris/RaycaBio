
import matplotlib.patches as mpatches

# ── Figure 2: per-compound selectivity bars (top-8 off-targets per compound) ─
fig, axes = plt.subplots(2, 3, figsize=(18, 8), facecolor="#0d1117",
                         sharex=False, sharey=False)
axes = axes.flatten()

for ax, cpd in zip(axes, compounds):
    ax.set_facecolor("#0d1117")
    row   = pivot.loc[cpd].drop("PDK1").sort_values(ascending=False).head(8)
    pdk1  = pivot.loc[cpd, "PDK1"]
    colors = [FAMILY_COLOR.get(FAMILY.get(k,"Other"),"#aaa") for k in row.index]
    bars  = ax.barh(range(len(row)), row.values, color=colors, edgecolor="#333", height=0.65)
    ax.axvline(pdk1, color="white", linewidth=1.2, linestyle="--", label=f"PDK1={pdk1:.2f}")
    ax.set_yticks(range(len(row)))
    ax.set_yticklabels(row.index, fontsize=8, color="white")
    ax.set_xlabel("pIC50", color="#aaa", fontsize=8)
    ax.set_title(cpd, color="white", fontsize=10, fontweight="bold")
    ax.tick_params(colors="#888", labelsize=7)
    for spine in ax.spines.values(): spine.set_edgecolor("#333")
    ax.set_xlim(6.3, 7.6)
    ax.legend(fontsize=7, facecolor="#111", edgecolor="#333", labelcolor="white",
              loc="lower right")
    for i, (v, kin) in enumerate(zip(row.values, row.index)):
        ax.text(v + 0.01, i, f"{v:.2f}", va="center", fontsize=7, color="white")

# Shared family legend
handles = [mpatches.Patch(color=v, label=k) for k,v in FAMILY_COLOR.items()]
fig.legend(handles=handles, loc="lower center", ncol=8, fontsize=7.5,
           facecolor="#111", edgecolor="#333", labelcolor="white",
           title="Kinase family", title_fontsize=8, bbox_to_anchor=(0.5, -0.04))

fig.suptitle("Per-compound top-8 off-targets vs. PDK1 (dashed white)\n"
             "KinaseDocker2  |  Vina-GPU + DNN scorer  |  43 kinases profiled",
             color="white", fontsize=11, y=1.01)
plt.tight_layout()
out_bar = f"{WS}/kinome_per_compound.png"
plt.savefig(out_bar, dpi=150, bbox_inches="tight", facecolor="#0d1117")
plt.close()
import os; print(f"Saved {out_bar} ({os.path.getsize(out_bar)//1024} KB)")
