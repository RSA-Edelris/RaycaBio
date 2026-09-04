
import sys; sys.path.insert(0, ".")
from draw_helpers import *

# ── ROUTE A ───────────────────────────────────────────────────────────────
route_a = [
    (mols["SM-1 2-nitropiperonal"],   ["SM-1","2-Nitropiperonal","(Combi-Blocks stock)"]),
    ("arrow", ["NaBH₃CN","SM-2,AcOH","MeOH 0°C→RT"], ["78%","A1"]),
    (mols["Int-A1 reductive-am"],     ["Int-A1","2-Nitro BnNH-CpCH₂",""]),
    ("arrow", ["Boc₂O,Et₃N","DCM,RT"], ["92%","A2"]),
    (mols["Int-A2 N-Boc"],            ["Int-A2","N-Boc protected",""]),
    ("arrow", ["SnCl₂·2H₂O","EtOH 70°C"], ["82%","A3"]),
    (mols["Int-A3 aniline"],          ["Int-A3","Aniline (Boc on N1)",""]),
    ("arrow", ["SM-4,HATU","DIPEA,DMF"], ["75%","A4"]),
    (mols["Int-A4 amide"],            ["Int-A4","Bis-Boc amide",""]),
    ("arrow", ["TFA/DCM","1:1 RT"], ["quant","A5"]),
    (mols["Int-A5 open-chain"],       ["Int-A5","Open-chain δ-amino acid",""]),
    ("arrow", ["HATU,DIPEA","0.5 mM DCM","syringe pump"], ["30-35%","A6  ⚠ worst step"]),
    (mols["Target"],                  ["TARGET","C₁₅H₁₈N₂O₃ MW 274","8-membered lactam"]),
]

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

row_a = build_row(route_a)
title_a = route_title("ROUTE A — Linear / HATU lactamisation  |  6 steps, LLS 6, ~12% overall", row_a.width)
sub_a   = text_img("Key disconnection: N1–C(=O) amide bond opened → linear δ-amino acid → medium-ring closure (⚠ worst step: 8-membered HATU cyclisation at 0.5 mM)",
                   row_a.width, 20, 10, "#444444")
panel_a = vstack([title_a, sub_a, row_a], gap=3)
panel_a.save("route_A.png")
print("Route A:", panel_a.size)
