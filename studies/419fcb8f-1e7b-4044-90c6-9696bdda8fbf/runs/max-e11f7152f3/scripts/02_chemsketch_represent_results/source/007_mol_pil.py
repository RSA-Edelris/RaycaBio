
from rdkit.Chem.Draw import rdMolDraw2D

def mol_to_pil(mol, w=260, h=185):
    d = rdMolDraw2D.MolDraw2DCairo(w, h)
    d.drawOptions().padding = 0.15
    d.DrawMolecule(mol)
    d.FinishDrawing()
    return Image.open(io.BytesIO(d.GetDrawingText()))

def lbl(text, w, h=20, fs=10):
    img = Image.new("RGB", (w, h), "white")
    dr = ImageDraw.Draw(img)
    try: font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", fs)
    except: font = ImageFont.load_default()
    bb = dr.textbbox((0,0), text, font=font)
    dr.text(((w-(bb[2]-bb[0]))//2, 2), text, fill="black", font=font)
    return img

def bold_lbl(text, w, h=22, fs=11):
    img = Image.new("RGB", (w, h), "white")
    dr = ImageDraw.Draw(img)
    try: font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", fs)
    except: font = ImageFont.load_default()
    bb = dr.textbbox((0,0), text, font=font)
    dr.text(((w-(bb[2]-bb[0]))//2, 2), text, fill="#1a1a7a", font=font)
    return img

def arrow_block(top_lines, bot_lines, w=80, total_h=185):
    img = Image.new("RGB", (w, total_h), "white")
    dr = ImageDraw.Draw(img)
    try:
        ft = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 9)
        fb = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 9)
    except:
        ft = fb = ImageFont.load_default()
    mid = total_h // 2
    dr.line([(6, mid),(w-6, mid)], fill="black", width=2)
    dr.polygon([(w-6,mid-5),(w-6,mid+5),(w-1,mid)], fill="black")
    for i, t in enumerate(top_lines):
        dr.text((3, mid-14-(len(top_lines)-1-i)*11), t, fill="#1a1aaa", font=ft)
    for i, t in enumerate(bot_lines):
        dr.text((3, mid+5+i*11), t, fill="#8b0000", font=fb)
    return img

def vstack(imgs, gap=2):
    w = max(i.width for i in imgs)
    h = sum(i.height for i in imgs) + gap*(len(imgs)-1)
    out = Image.new("RGB",(w,h),"white")
    y=0
    for im in imgs:
        out.paste(im,((w-im.width)//2,y)); y+=im.height+gap
    return out

def hstack(imgs, gap=4):
    h = max(i.height for i in imgs)
    w = sum(i.width for i in imgs)+gap*(len(imgs)-1)
    out = Image.new("RGB",(w,h),"white")
    x=0
    for im in imgs:
        out.paste(im,(x,(h-im.height)//2)); x+=im.width+gap
    return out

def mol_cell(key, name_lines):
    m = mol_to_pil(mols[key])
    cells = [m] + [lbl(t, m.width, 18, 10) for t in name_lines]
    return vstack(cells, gap=1)

print("helpers defined")
