
# ── PART 1: helpers + scheme data ───────────────────────────────────────────
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import rdMolDraw2D
from PIL import Image
import io, os, numpy as np

workspace = "/home/ubuntu/rayca-sessions/9dea6793-337f-42cf-8e3e-908d9d53ed0e-dc0c221c42d4"
sdf_path  = "/home/ubuntu/rayca-artifacts/dc0c221c42d47c64e9717502/files/PoC Retrosynthetic analysis_Targets.sdf"

# ── read all target SMILES from SDF ─────────────────────────────────────────
suppl = Chem.SDMolSupplier(sdf_path, removeHs=False, sanitize=True)
targets = {}
for mol in suppl:
    if mol:
        targets[mol.GetProp('_Name')] = Chem.MolToSmiles(mol)

# ── rendering helpers ────────────────────────────────────────────────────────
def s2a(smi, w=300, h=220):
    """SMILES → numpy RGB array."""
    if not smi:
        return np.full((h, w, 3), 248, dtype=np.uint8)
    mol = Chem.MolFromSmiles(smi)
    if mol is None:
        arr = np.full((h, w, 3), 255, dtype=np.uint8)
        return arr
    AllChem.Compute2DCoords(mol)
    d = rdMolDraw2D.MolDraw2DCairo(w, h)
    d.drawOptions().addStereoAnnotation = True
    d.drawOptions().padding = 0.13
    d.DrawMolecule(mol); d.FinishDrawing()
    return np.array(Image.open(io.BytesIO(d.GetDrawingText())).convert('RGB'))

def render_scheme(cid, tgt_smi, routes, out):
    """
    3-route retrosynthetic scheme.  routes = list of 3 dicts:
      title, rec, lv1(list[smi]), lab1, lv2(list[smi]|None), lab2, src(list[str])
    """
    fig = plt.figure(figsize=(21, 16))
    fig.patch.set_facecolor('white')
    fig.text(0.5, 0.975, f'{cid}  —  Retrosynthetic Analysis  (Routes A / B / C)',
             ha='center', va='top', fontsize=14, fontweight='bold', color='#1a1a2e')

    # ── target (top-centre) ──────────────────────────────────────────────────
    ax_t = fig.add_axes([0.30, 0.74, 0.40, 0.21])
    ax_t.imshow(s2a(tgt_smi, 480, 250)); ax_t.axis('off')
    ax_t.set_title('TARGET  ▼', fontsize=9, color='#555', pad=3, style='italic')

    COLS = [0.02, 0.35, 0.68]   # left edge of each 0.30-wide column
    CW   = 0.30

    for ri, R in enumerate(routes):
        cx  = COLS[ri]
        mid = cx + CW/2
        rec = R.get('rec', False)
        hdr = '#1a5276' if rec else '#2c3e50'

        # route header
        star = '  ★ RECOMMENDED' if rec else ''
        fig.text(mid, 0.74, R['title'] + star,
                 ha='center', va='top', fontsize=8.5, fontweight='bold', color=hdr)

        # ── first retro-arrow  (0.72→0.57) ──────────────────────────────────
        axa = fig.add_axes([cx+0.01, 0.57, CW-0.02, 0.15])
        axa.set_xlim(0,1); axa.set_ylim(0,1); axa.axis('off')
        axa.annotate('', xy=(0.45,0.05), xytext=(0.45,0.95),
                     arrowprops=dict(arrowstyle='->', color='#111', lw=3,
                                    mutation_scale=20), zorder=5)
        axa.annotate('', xy=(0.50,0.05), xytext=(0.50,0.95),
                     arrowprops=dict(arrowstyle='->', color='#111', lw=1.8,
                                    mutation_scale=20), zorder=5)
        axa.text(0.53, 0.50, R.get('lab1',''), fontsize=7.5, color='#c0392b',
                 va='center', style='italic', wrap=True)

        # ── level-1 molecules ────────────────────────────────────────────────
        lv1 = R.get('lv1', [])
        n   = len(lv1)
        mw  = (CW - 0.01) / max(n, 1) - 0.005
        for mi, smi in enumerate(lv1):
            ax_m = fig.add_axes([cx + mi*(mw+0.005), 0.38, mw, 0.18])
            ax_m.imshow(s2a(smi, 200, 165)); ax_m.axis('off')
        for mi in range(n-1):
            fig.text(cx+(mi+1)*(mw+0.005)-0.008, 0.47,
                     '+', ha='center', va='center', fontsize=14, color='#111')

        # ── second retro-arrow (only if lv2 exists) ─────────────────────────
        lv2 = R.get('lv2')
        if lv2:
            axb = fig.add_axes([cx+0.01, 0.20, CW-0.02, 0.16])
            axb.set_xlim(0,1); axb.set_ylim(0,1); axb.axis('off')
            axb.annotate('', xy=(0.45,0.05), xytext=(0.45,0.95),
                         arrowprops=dict(arrowstyle='->', color='#111', lw=3,
                                        mutation_scale=20), zorder=5)
            axb.annotate('', xy=(0.50,0.05), xytext=(0.50,0.95),
                         arrowprops=dict(arrowstyle='->', color='#111', lw=1.8,
                                        mutation_scale=20), zorder=5)
            axb.text(0.53, 0.50, R.get('lab2',''), fontsize=7.5, color='#c0392b',
                     va='center', style='italic')

            n2 = len(lv2)
            mw2 = (CW-0.01)/max(n2,1) - 0.005
            for mi, smi in enumerate(lv2):
                ax_s = fig.add_axes([cx+mi*(mw2+0.005), 0.03, mw2, 0.16])
                ax_s.imshow(s2a(smi, 200, 155)); ax_s.axis('off')
            for mi in range(n2-1):
                fig.text(cx+(mi+1)*(mw2+0.005)-0.008, 0.11,
                         '+', ha='center', va='center', fontsize=14, color='#111')
            src_y = 0.02
        else:
            src_y = 0.35

        src = R.get('src', [])
        if src:
            fig.text(mid, src_y, '  |  '.join(src),
                     ha='center', va='top', fontsize=6.5, color='#555', style='italic')

    # column dividers
    for dx in [0.34, 0.67]:
        line = plt.Line2D([dx, dx], [0.02, 0.96],
                          transform=fig.transFigure, color='#ccc', lw=1.2)
        fig.add_artist(line)

    plt.savefig(out, dpi=100, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f'  ✓  scheme_{cid}.png')

print("Helpers defined. targets loaded:", list(targets.keys()))
