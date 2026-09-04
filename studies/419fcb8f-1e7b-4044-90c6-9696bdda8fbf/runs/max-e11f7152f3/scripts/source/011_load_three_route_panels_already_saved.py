
import sys; sys.path.insert(0, ".")
from draw_helpers import *

# Load the three route panels already saved
pa = Image.open("panel_SM.png")
ra = Image.open("route_A.png")
rb = Image.open("route_B.png")
rc = Image.open("route_C.png")

# Normalise all to same width (widest wins), with white padding
W = max(pa.width, ra.width, rb.width, rc.width)

def pad_to_width(img, w):
    if img.width == w:
        return img
    out = Image.new("RGB", (w, img.height), "white")
    out.paste(img, ((w - img.width)//2, 0))
    return out

panels = [pad_to_width(p, W) for p in [pa, ra, rb, rc]]

# Divider line
def divider(w, h=6):
    img = Image.new("RGB", (w, h), "#cccccc")
    return img

# Header
def header_img(w):
    img = Image.new("RGB", (w, 42), "#003366")
    dr  = ImageDraw.Draw(img)
    try:
        f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
    except:
        f = ImageFont.load_default()
    txt = "RETROSYNTHETIC ANALYSIS — Compound A  (C₁₅H₁₈N₂O₃, MW 274.32, 8-membered benzo[1,5]diazocin-2-one)"
    bb = dr.textbbox((0,0), txt, font=f)
    dr.text(((w-(bb[2]-bb[0]))//2, (42-(bb[3]-bb[1]))//2), txt, fill="white", font=f)
    return img

# Score table as image
score_rows = [
    "ROUTE COMPARISON",
    "                         Route A               Route B               Route C ★",
    "Steps (total)            6                     5                     6",
    "Longest linear seq.      6                     5                     6",
    "Overall yield (est.)     10–13%                19–24%                25–30%",
    "Ring-closing yield       25–35%  (amide HATU)  35–45%  (reduct. am.) 40–55%  (Buchwald)",
    "Ring-closing bond        N1–C(=O)              N1–CH₂–Ar            C5a–N5(H)",
    "SM commercial status     SM-1: stock           SM-6: 2wk lead        All: genuine stock",
    "PG burden                2× Boc                1× acetal             1× Boc",
    "Worst step               A6: 0.5 mM syringe    B5: 5 mM, 48 h        C6: Pd removal",
    "Scale ceiling            ~50 mmol (dilution)   ~100 mmol             ~50 mmol (Pd cost)",
    "Stereochemical risk      None                  None                  None",
    "AiZynthFinder basis      Yes (SM-1+SM-2 SMs)   Partial (SM-6)        Expert (new)",
]

def score_table(rows, w):
    h = len(rows)*16 + 14
    img = Image.new("RGB", (w, h), "#f5f5f0")
    dr  = ImageDraw.Draw(img)
    try:
        fh = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 11)
        fr = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuMono.ttf", 10)
    except:
        fh = fr = ImageFont.load_default()
    for i, row in enumerate(rows):
        f = fh if i == 0 else fr
        c = "#003366" if i == 0 else ("black" if "Route C" not in row else "#005500")
        dr.text((12, 7+i*16), row, fill=c, font=f)
    return img

header = header_img(W)
table  = score_table(score_rows, W)
sep    = divider(W)

all_panels = [
    header, sep,
    panels[0], sep,        # SM panel
    panels[1], sep,        # Route A
    panels[2], sep,        # Route B
    panels[3], sep,        # Route C
    table,
]

total_h = sum(p.height for p in all_panels) + 4*(len(all_panels)-1)
combined = Image.new("RGB", (W, total_h), "white")
y = 0
for p in all_panels:
    combined.paste(p, (0, y))
    y += p.height + 4

combined.save("retrosynthesis_compound_A.png", dpi=(150,150))
print(f"Final image: {combined.size}  →  retrosynthesis_compound_A.png")
