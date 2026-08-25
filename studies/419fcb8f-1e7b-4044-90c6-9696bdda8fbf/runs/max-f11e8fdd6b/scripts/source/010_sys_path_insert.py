
import sys; sys.path.insert(0, ".")
from draw_helpers import *

def build_row(route_steps, mw=240, mh=175):
    cells = []
    for item in route_steps:
        if isinstance(item, tuple) and item[0] == "arrow":
            _, top, bot = item
            cells.append(arrow_block(top, bot, w=88, total_h=mh+30))
        else:
            mol_obj, lines = item
            cells.append(mol_cell(mol_obj, lines, mw, mh))
    return hstack(cells, gap=2)

# ── ROUTE B ───────────────────────────────────────────────────────────────
route_b = [
    (mols["SM-6 2-aminopiperonal"],  ["SM-6","2-Aminopiperonal","(Enamine; 2wk lead)"]),
    ("arrow", ["HOCH₂CH₂OH","p-TsOH,toluene","110°C DS"], ["88%","B1"]),
    (mols["Int-B1 acetal"],          ["Int-B1","1,3-Dioxolane acetal",""]),
    ("arrow", ["CH₂=CHCO Cl","Et₃N,DCM,0°C"], ["80%","B2"]),
    (mols["Int-B2 acrylamide"],      ["Int-B2","Acrylamide",""]),
    ("arrow", ["SM-2 CpCH₂NH₂","MeOH,RT,24h"], ["75%","B3  aza-Michael"]),
    (mols["Int-B3 aza-Michael"],     ["Int-B3","Aza-Michael adduct",""]),
    ("arrow", ["HCl(aq)/acetone","RT,2h"], ["92%","B4  acetal off"]),
    (mols["Int-B4 aldehyde-free"],   ["Int-B4","ArCHO + chain-NH",""]),
    ("arrow", ["NaBH₃CN,AcOH","MeOH/DMF 5mM","40°C,48h"], ["38-45%","B5  ring close"]),
    (mols["Target"],                 ["TARGET","C₁₅H₁₈N₂O₃ MW 274","8-membered ring"]),
]

row_b = build_row(route_b)
title_b = route_title("ROUTE B — Intramolecular reductive amination  |  5 steps, LLS 5, ~19-24% overall", row_b.width)
sub_b   = text_img("Key disconnection: N1–CH₂(C9a) benzylic C–N bond opened → ArCHO tethered precursor → intramolecular RA closes ring",
                   row_b.width, 20, 10, "#444444")
panel_b = vstack([title_b, sub_b, row_b], gap=3)
panel_b.save("route_B.png")
print("Route B:", panel_b.size)

# ── ROUTE C ───────────────────────────────────────────────────────────────
route_c = [
    (mols["SM-7 2-bromopiperonal"],  ["SM-7","2-Bromopiperonal","(Sigma 195030; stock)"]),
    ("arrow", ["NaBH₄","MeOH,0°C"], ["96%","C1"]),
    (mols["Int-C1 BnOH"],           ["Int-C1","Benzyl alcohol",""]),
    ("arrow", ["SOCl₂","DCM,0°C"], ["90%","C2"]),
    (mols["Int-C2 BnCl"],           ["Int-C2","Benzyl chloride",""]),
    ("arrow", ["SM-2,K₂CO₃","MeCN,60°C"], ["75%","C3"]),
    (mols["Int-C3 2nd-amine"],      ["Int-C3","2°-Amine (Ar-Br intact)",""]),
    ("arrow", ["SM-4,HATU","DIPEA,DMF"], ["82%","C4"]),
    (mols["Int-C4 Boc-amide"],      ["Int-C4","Boc-amide",""]),
    ("arrow", ["TFA/DCM","1:1,RT"], ["quant","C5"]),
    (mols["Int-C5 BH-precursor"],   ["Int-C5","BH precursor (ArBr+NH₂)",""]),
    ("arrow", ["Pd₂dba₃ 3mol%","BINAP,Cs₂CO₃","toluene 100°C"], ["40-55%","C6  BH ring close"]),
    (mols["Target"],                ["TARGET","C₁₅H₁₈N₂O₃ MW 274","★ RECOMMENDED"]),
]

row_c = build_row(route_c)
title_c = route_title("ROUTE C — Buchwald–Hartwig N-arylation  |  6 steps, LLS 6, ~25-30% overall  ★ RECOMMENDED", row_c.width)
sub_c   = text_img("Key disconnection: C5a–N5 aryl–NH bond (Pd C–N coupling); all SMs genuine commercial stock; no extreme dilution required",
                   row_c.width, 20, 10, "#444444")
panel_c = vstack([title_c, sub_c, row_c], gap=3)
panel_c.save("route_C.png")
print("Route C:", panel_c.size)
