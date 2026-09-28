
from fpdf import FPDF
import textwrap, unicodedata

OUT = "/home/ubuntu/rayca-sessions/a26cc075-95a4-4e76-8438-9c117af1a9de-26995afd3529/HTE_screen_chat_log.pdf"

def clean(text):
    # Replace common unicode that Latin-1 can't handle
    replacements = {
        '’': "'", '‘': "'", '“': '"', '”': '"',
        '–': '-', '—': '-', '…': '...', '•': '*',
        '²': '2', '³': '3', 'α': 'alpha', 'β': 'beta',
        '°': 'deg', '→': '->', 'é': 'e', 'à': 'a',
        'è': 'e', '−': '-', '±': '+/-',
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text.encode('latin-1', errors='replace').decode('latin-1')

class ChatPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 9)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, 'HTE Screen Analysis - Chat Log  |  929EDL2056', align='C')
        self.ln(2)
        self.set_draw_color(200, 200, 200)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-12)
        self.set_font('Helvetica', '', 8)
        self.set_text_color(160, 160, 160)
        self.cell(0, 8, f'Page {self.page_no()}', align='C')

pdf = ChatPDF()
pdf.set_auto_page_break(auto=True, margin=18)
pdf.add_page()

# Title block
pdf.set_font('Helvetica', 'B', 16)
pdf.set_text_color(20, 20, 20)
pdf.cell(0, 10, 'HTE Screen Analysis - Chat Log', ln=True, align='C')
pdf.set_font('Helvetica', '', 10)
pdf.set_text_color(100, 100, 100)
pdf.cell(0, 6, 'Study: 929EDL2056  |  Cu-catalysed cross-coupling ligand screen  |  96-well HTE', ln=True, align='C')
pdf.ln(8)

W = 170  # usable width

for role, text in turns_pdf:
    text = clean(text)
    is_user = (role == 'user')

    # Role label
    if is_user:
        pdf.set_fill_color(230, 242, 255)
        pdf.set_text_color(0, 60, 130)
        label = 'USER'
    else:
        pdf.set_fill_color(245, 245, 245)
        pdf.set_text_color(40, 40, 40)
        label = 'ASSISTANT'

    pdf.set_font('Helvetica', 'B', 8)
    pdf.cell(W, 5, f'  {label}', fill=True, ln=True)

    # Body
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(30, 30, 30)
    pdf.set_x(14)

    # Wrap long lines manually
    for para in text.split('\n'):
        para = para.strip()
        if not para:
            pdf.ln(2)
            continue
        # multi_cell handles line wrapping
        pdf.set_x(14)
        pdf.multi_cell(W - 4, 4.5, para)

    pdf.ln(4)

pdf.output(OUT)
print(f"PDF saved: {OUT}  ({os.path.getsize(OUT)//1024} KB)")
