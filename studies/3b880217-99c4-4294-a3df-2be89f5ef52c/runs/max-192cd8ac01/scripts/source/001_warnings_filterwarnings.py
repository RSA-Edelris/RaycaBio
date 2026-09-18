
import requests, numpy as np, io, warnings
from Bio import PDB
from Bio.PDB.SASA import ShrakeRupley
warnings.filterwarnings('ignore')

def get_pdb(pid):
    r = requests.get(f"https://files.rcsb.org/download/{pid}.pdb", timeout=30)
    r.raise_for_status()
    return r.text

bcl6_txt = get_pdb("5MW2")
brd4_txt = get_pdb("3P5O")

p = PDB.PDBParser(QUIET=True)
bcl6 = p.get_structure("bcl6", io.StringIO(bcl6_txt))
brd4 = p.get_structure("brd4", io.StringIO(brd4_txt))

for label, s, txt in [("5MW2/BCL6-BTB", bcl6, bcl6_txt), ("3P5O/BRD4-BD1", brd4, brd4_txt)]:
    for line in txt.split('\n'):
        if line.startswith('TITLE'):
            print(f"{label}: {line.strip()}")
            break
    for chain in s[0]:
        prot = [r for r in chain if r.id[0]==' ']
        het  = [r for r in chain if r.id[0] not in (' ','W')]
        if prot:
            nums = [r.id[1] for r in prot]
            print(f"  Chain {chain.id}: {len(prot)} aa  ({min(nums)}-{max(nums)})")
        for h in het:
            com = np.mean([a.coord for a in h.get_atoms()], axis=0)
            nha = sum(1 for a in h.get_atoms() if a.element!='H')
            print(f"  Ligand {h.resname}  nHA={nha}  CoM={com.round(1)}")
    print()
