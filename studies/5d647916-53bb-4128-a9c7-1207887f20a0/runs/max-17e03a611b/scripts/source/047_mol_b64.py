
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors
from rdkit.Chem.Draw import rdMolDraw2D
import base64, re

def mol_b64(smi, w=175, h=125):
    mol = Chem.MolFromSmiles(smi)
    if not mol: return None
    AllChem.Compute2DCoords(mol)
    d = rdMolDraw2D.MolDraw2DSVG(w, h)
    d.drawOptions().clearBackground = False
    d.drawOptions().addStereoAnnotation = True
    d.DrawMolecule(mol)
    d.FinishDrawing()
    return base64.b64encode(d.GetDrawingText().encode()).decode()

def mol_box(smi, label, role, mw_val):
    tag_map = {'sm':'SM', 'int':'INT', 'prod':'★ TARGET'}
    tag  = tag_map[role]
    cls  = f'mol-box mol-{role}'
    tcls = f'mol-role-tag tag-{role}'
    b64  = mol_b64(smi)
    return (f'<div class="{cls}">'
            f'<span class="{tcls}">{tag}</span>'
            f'<div class="mol-img-wrap"><img class="mol-img" src="data:image/svg+xml;base64,{b64}"'
            f' width="175" height="125" alt="{smi[:40]}"></div>'
            f'<div class="mol-name">{label}</div>'
            f'</div>')

def arrow_block(reagents_html, conditions, yield_str):
    return (f'<div class="arrow-block">'
            f'<div class="arrow-reagents">{reagents_html}</div>'
            f'<div class="arrow-shaft"><div class="arrow-line"></div><div class="arrow-head">&#9654;</div></div>'
            f'<div class="arrow-conditions">{conditions}</div>'
            f'<div class="arrow-yield">{yield_str}</div>'
            f'</div>')

def plus_sep():
    return '<div style="font-size:1.5rem;font-weight:700;color:#555;align-self:center;padding:0 4px">+</div>'

mw = lambda s: round(Descriptors.MolWt(Chem.MolFromSmiles(s)))

# Correct row for MCUF651 Route 1
new_row = '<div class="scheme-row">'

# Step 1: indole acid + pipe amine → amide int
new_row += mol_box(INDOLE_ACID, '4,6-Difluoroindole-2-carboxylic acid', 'sm', mw(INDOLE_ACID))
new_row += plus_sep()
new_row += mol_box(PIPE_AMINE,  '(R)-Piperidin-3-amine', 'sm', mw(PIPE_AMINE))
new_row += arrow_block(
    'HATU (1.1 eq), DIPEA (3 eq)',
    'DMF, 0 °C → RT, 12 h',
    '75–85%'
)
new_row += mol_box(AMIDE_INT, 'Amide intermediate\n(indole-C(=O)-NH-piperidine)', 'int', mw(AMIDE_INT))

# Step 2: N-alkylation
new_row += arrow_block(
    'K₂CO₃ (2 eq)<br>+ 2-Bromo-N,N-dimethylethylamine (1.1 eq)',
    'MeCN, 60 °C, 8 h',
    '65–80%'
)
new_row += mol_box(MCUF651, 'MCUF651', 'prod', mw(MCUF651))
new_row += '</div>\n'

print(f"New row length: {len(new_row):,} chars")
print("Preview (no base64):")
preview = re.sub(r'data:image/svg\+xml;base64,[A-Za-z0-9+/=]+', 'B64', new_row)
print(preview[:600])
