
import sys
sys.path.insert(0, '/home/ubuntu/rayca-sessions/9d335ae8-a19c-4b53-89e1-813dc8783c51-0e2dd53329c8')
from drug_utils import residue_descriptors

# ---- APO CDK2 resname lookup ----
apo_resname  = {(ch,rs): alist[0]['resn'] for (ch,rs), alist in apo_atoms_dict.items()}
holo_resname = {(ch,rs): alist[0]['resn'] for (ch,rs), alist in holo_atoms_dict.items()}

# ---- Pocket 1: CRBN main (thalidomide / LVY binding) ----
crbn_main_raw = [
    382,383,385,386,388,389,390,391,392,393,394,396,399,400,401,402,403,404,
    405,406,407,408,409,410,411,412,413,414,415,416,417,418,419,420,421,422
]
crbn_resname = {(ch,rs): alist[0]['resn'] for (ch,rs), alist in crbn_atoms_dict.items()}
crbn_main = [('B', r, crbn_resname.get(('B',r),'UNK')) for r in crbn_main_raw
             if ('B',r) in crbn_resname]

# ---- Pocket 2: CRBN allosteric / zinc shell ----
crbn_allo_raw = [325,328,329,330,331,332,333,334,335,336,393,394,395,396,397]
crbn_allo = [('B', r, crbn_resname.get(('B',r),'UNK')) for r in crbn_allo_raw
             if ('B',r) in crbn_resname]

# ---- Pocket 3: dpCDK2 ATP-binding (chain A) ----
atp_raw = [15,17,18,30,31,32,33,34,35,46,47,48,49,50,51,52,53,54,55,56,
           58,63,64,65,66,67,76,77,78,79,80,81,82,83,84,85,86,89,
           118,123,125,126,127,128,129,132,134,135,136,137,
           142,143,144,145,146,147,148,149,150,
           158,163,164,165,172,173,175,176,177,178,179,180,185,233,234]
atp_pocket = [('A', r, apo_resname.get(('A',r),'UNK')) for r in atp_raw
              if ('A',r) in apo_resname]

# ---- Pocket 4: dpCDK2 T-loop allosteric (chain A) ----
tloop_raw = [156,157,158,159,161,163,172,173,174,175,176,177,178,179,180,181]
tloop_pocket = [('A', r, apo_resname.get(('A',r),'UNK')) for r in tloop_raw
                if ('A',r) in apo_resname]

# ---- Pocket 5: CDK2-CyclinE1 interface (apo, both chains) ----
iface_a_raw = [116,119,120,121,122]
iface_b_raw = [90,95,96,97,98,99,100,101,102,103,104,105]
iface_pocket = ([('A', r, apo_resname.get(('A',r),'UNK')) for r in iface_a_raw if ('A',r) in apo_resname] +
                [('B', r, apo_resname.get(('B',r),'UNK')) for r in iface_b_raw if ('B',r) in apo_resname])

# ---- Pocket 6: CTX contact shell (holo, both chains) ----
ctx_a_raw  = [54,57,58,121,122,123,151,152,153]
ctx_b_raw  = [90,101,102,104,105,107,108,111,149,227,228,229,233,234,237]
ctx_pocket = ([('A', r, holo_resname.get(('A',r),'UNK')) for r in ctx_a_raw  if ('A',r) in holo_resname] +
              [('B', r, holo_resname.get(('B',r),'UNK')) for r in ctx_b_raw  if ('B',r) in holo_resname])

# ---- Compute descriptors ----
pockets = [
    ('CRBN',            'Main (thalidomide/IMiD)',       crbn_main,    crbn_atoms_dict),
    ('CRBN',            'Allosteric (zinc shell)',        crbn_allo,    crbn_atoms_dict),
    ('dpCDK2–CyclinE1', 'ATP-binding',                   atp_pocket,   apo_atoms_dict),
    ('dpCDK2–CyclinE1', 'T-loop allosteric',             tloop_pocket, apo_atoms_dict),
    ('dpCDK2–CyclinE1', 'CDK2–CyclinE1 interface (apo)', iface_pocket, apo_atoms_dict),
    ('CDK2–CCNE (holo)', 'CTX binding (interface)',       ctx_pocket,   holo_atoms_dict),
]

results = []
for target, name, res, adict in pockets:
    d = residue_descriptors(res, adict)
    d['target'] = target
    d['pocket'] = name
    results.append(d)
    print(f"{target:25s}  {name:35s}  n={d['n_res']:3d}  "
          f"vol={d['vol_hull']:7.0f} Å³  "
          f"hydro={d['f_hydro']:.2f}  arom={d['f_arom']:.2f}  "
          f"pos={d['f_pos']:.2f}  neg={d['f_neg']:.2f}  polar={d['f_polar']:.2f}")
