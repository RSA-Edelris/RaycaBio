
from rdkit.Chem.Draw import rdMolDraw2D
from PIL import Image, ImageDraw, ImageFont
import io

FONT_REG  = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def get_font(path, size):
    try: return ImageFont.truetype(path, size)
    except: return ImageFont.load_default()

def mol_to_pil(mol, w=260, h=185):
    d = rdMolDraw2D.MolDraw2DCairo(w, h)
    d.drawOptions().padding = 0.15
    d.DrawMolecule(mol)
    d.FinishDrawing()
    return Image.open(io.BytesIO(d.GetDrawingText()))

def text_img(text, w, h=20, fs=10, color="black", bold=False):
    img = Image.new("RGB", (w, h), "white")
    dr  = ImageDraw.Draw(img)
    f   = get_font(FONT_BOLD if bold else FONT_REG, fs)
    bb  = dr.textbbox((0,0), text, font=f)
    dr.text(((w-(bb[2]-bb[0]))//2, (h-(bb[3]-bb[1]))//2), text, fill=color, font=f)
    return img

def arrow_block(top_lines, bot_lines, w=82, total_h=185):
    img = Image.new("RGB", (w, total_h), "white")
    dr  = ImageDraw.Draw(img)
    ft  = get_font(FONT_REG, 9)
    mid = total_h // 2
    dr.line([(5, mid),(w-6, mid)], fill="black", width=2)
    dr.polygon([(w-6,mid-5),(w-6,mid+5),(w-1,mid)], fill="black")
    for i, t in enumerate(reversed(top_lines)):
        dr.text((3, mid-13-i*11), t, fill="#1a1aaa", font=ft)
    for i, t in enumerate(bot_lines):
        dr.text((3, mid+5+i*11), t, fill="#8b0000", font=ft)
    return img

def vstack(imgs, gap=2):
    w = max(i.width for i in imgs)
    h = sum(i.height for i in imgs)+gap*(len(imgs)-1)
    out = Image.new("RGB",(w,h),"white"); y=0
    for im in imgs:
        out.paste(im,((w-im.width)//2,y)); y+=im.height+gap
    return out

def hstack(imgs, gap=4):
    h = max(i.height for i in imgs)
    w = sum(i.width for i in imgs)+gap*(len(imgs)-1)
    out = Image.new("RGB",(w,h),"white"); x=0
    for im in imgs:
        out.paste(im,(x,(h-im.height)//2)); x+=im.width+gap
    return out

def mol_cell(mol, lines, mw=260, mh=185):
    cells = [mol_to_pil(mol, mw, mh)] + [text_img(t, mw, 18, 10) for t in lines]
    return vstack(cells, gap=1)

def route_title(text, w):
    return text_img(text, w, 34, 15, color="#003366", bold=True)
