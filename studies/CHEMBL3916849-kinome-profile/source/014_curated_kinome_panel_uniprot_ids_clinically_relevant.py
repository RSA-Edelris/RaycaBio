
import requests, time

# Curated kinome panel — UniProt IDs for clinically relevant kinases
KINOME_PANEL = {
    'O14965': 'AURKA',   'Q96GD4': 'AURKB',   'Q9UQB9': 'AURKC',
    'P06493': 'CDK1',    'P24941': 'CDK2',    'P11802': 'CDK4',   'Q00534': 'CDK6',
    'P27448': 'MARK3',   'Q96L34': 'MARK4',   'Q9P0L2': 'MARK1',  'Q7KZI7': 'MARK2',
    'Q9UHD2': 'TBK1',    'Q14164': 'IKKE',
    'P00533': 'EGFR',    'Q9UM73': 'ALK',     'P07949': 'RET',
    'P36888': 'FLT3',    'P09619': 'PDGFRB',  'P10721': 'KIT',
    'P11362': 'FGFR1',   'P21802': 'FGFR2',   'P22607': 'FGFR3',
    'P53350': 'PLK1',    'P53350': 'PLK1',
    'Q8TF76': 'HASPIN',
    'O96017': 'DYRK2',   'Q13627': 'DYRK1A',
    'P15056': 'BRAF',    'Q02750': 'MAP2K1',
    'P31749': 'AKT1',    'P31751': 'AKT2',
    'P42336': 'PIK3CA',
    'P04049': 'RAF1',
    'P06239': 'LCK',     'P08631': 'HCK',
    'P00519': 'ABL1',
    'Q05655': 'PRKCD',
    'Q16659': 'MAPK6',   'P28482': 'MAPK1',
    'P45983': 'MAPK8',   'P54646': 'PRKAA2',
}

# Remove duplicate values (PLK1 duplicate)
KINOME_PANEL = dict(KINOME_PANEL)

UNIPROT_BASE = "https://rest.uniprot.org/uniprotkb"

seq_map = {}  # uniprot_acc -> sequence
for acc in list(KINOME_PANEL.keys()):
    try:
        r = requests.get(f"{UNIPROT_BASE}/{acc}.fasta", timeout=15)
        if r.status_code == 200:
            lines = r.text.strip().split('\n')
            seq = ''.join(lines[1:])
            seq_map[acc] = seq
        time.sleep(0.1)
    except:
        pass

print(f"Sequences fetched from UniProt: {len(seq_map)}/{len(KINOME_PANEL)}")
for acc, name in list(KINOME_PANEL.items())[:5]:
    if acc in seq_map:
        print(f"  {name} ({acc}): {len(seq_map[acc])} aa, starts {seq_map[acc][:20]}...")
