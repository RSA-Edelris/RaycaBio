
from rdkit.Chem.Draw import rdMolDraw2D
from PIL import Image, ImageDraw, ImageFont
import io, os

def mol_to_pil(mol, w=280, h=200):
    d = rdMolDraw2D.MolDraw2DCairo(w, h)
    d.drawOptions().addStereoAnnotation = False
    d.drawOptions().padding = 0.15
    d.DrawMolecule(mol)
    d.FinishDrawing()
    return Image.open(io.BytesIO(d.GetDrawingText()))

def make_label(text, w, h=28, fontsize=13):
    img = Image.new("RGB", (w, h), "white")
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", fontsize)
    except:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) // 2, 4), text, fill="black", font=font)
    return img

def make_arrow(w=60, h=200, label="", sublabel=""):
    img = Image.new("RGB", (w, h), "white")
    draw = ImageDraw.Draw(img)
    try:
        f10 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
        f9  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 9)
    except:
        f10 = f9 = ImageFont.load_default()
    mid = h // 2
    # Arrow line
    draw.line([(8, mid), (w-8, mid)], fill="black", width=2)
    draw.polygon([(w-8, mid-5), (w-8, mid+5), (w-2, mid)], fill="black")
    # Label above
    if label:
        for i, ln in enumerate(label.split("\n")):
            draw.text((4, mid - 14 - i*11), ln, fill="#1a1aaa", font=f9)
    # Sublabel below
    if sublabel:
        for i, ln in enumerate(sublabel.split("\n")):
            draw.text((4, mid + 6 + i*10), ln, fill="#aa1a1a", font=f9)
    return img

def stack_vertical(imgs, gap=0):
    w = max(i.width for i in imgs)
    h = sum(i.height for i in imgs) + gap * (len(imgs)-1)
    out = Image.new("RGB", (w, h), "white")
    y = 0
    for im in imgs:
        out.paste(im, ((w - im.width)//2, y))
        y += im.height + gap
    return out

def join_horizontal(imgs, gap=0):
    h = max(i.height for i in imgs)
    w = sum(i.width for i in imgs) + gap*(len(imgs)-1)
    out = Image.new("RGB", (w, h), "white")
    x = 0
    for im in imgs:
        out.paste(im, (x, (h - im.height)//2))
        x += im.width + gap
    return out

MW, MH = 260, 185  # mol cell size
AW = 65            # arrow width

# ── STARTING MATERIALS PANEL ──────────────────────────────────────────────
sm_keys = ["SM-1 2-nitropiperonal","SM-2 CpCH2NH2","SM-4 N-Boc-bAla",
           "SM-6 2-aminopiperonal","SM-7 2-bromopiperonal","Piperonal SM-1star"]
sm_labels = ["SM-1\n2-Nitropiperonal\n(Combi-Blocks; stock)",
             "SM-2\nCpCH₂NH₂\n(Sigma 106836; stock)",
             "SM-4\nN-Boc-β-Ala\n(Sigma 857629; stock)",
             "SM-6\n2-Aminopiperonal\n(Enamine; 2wk lead)",
             "SM-7\n2-Bromopiperonal\n(Sigma 195030; stock)",
             "Piperonal\n(Sigma W248606; bulk)"]

sm_cells = []
for k, lbl in zip(sm_keys, sm_labels):
    m = mol_to_pil(mols[k], MW, MH)
    lines = lbl.split("\n")
    lbls = [make_label(l, MW, 18, 11) for l in lines]
    sm_cells.append(stack_vertical([m] + lbls, gap=1))

# 3 per row
row1 = join_horizontal(sm_cells[:3], gap=6)
row2 = join_horizontal(sm_cells[3:], gap=6)
title_sm = make_label("STARTING MATERIALS", row1.width, 32, 16)
sm_panel = stack_vertical([title_sm, row1, row2], gap=6)
sm_panel.save("panel_SM.png")
print("SM panel:", sm_panel.size)
