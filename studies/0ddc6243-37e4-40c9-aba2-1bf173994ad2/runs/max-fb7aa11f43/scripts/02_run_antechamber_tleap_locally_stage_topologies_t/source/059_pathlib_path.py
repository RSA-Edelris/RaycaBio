
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors
import pathlib

BASE    = pathlib.Path('/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b')
LIG_DIR = BASE / 'md' / 'ligands'

LIGS = ['REF_85C','CPD1','CPD4','CPD7','CPD8','CPD9','CPD10','CPD11','CPD12']

print(f"{'Lig':<12} {'HeavyAtoms':>10} {'AllAtoms':>9} {'HasH':>5} {'FormalQ':>8} {'Electrons':>10} {'OddElec':>8}")
print('-'*70)

for lig in LIGS:
    sdf = LIG_DIR / f'{lig}_top.sdf'
    mol = Chem.SDMolSupplier(str(sdf), removeHs=False, sanitize=True)[0]
    if mol is None:
        print(f"{lig:<12} PARSE ERROR")
        continue

    n_heavy = sum(1 for a in mol.GetAtoms() if a.GetAtomicNum() > 1)
    n_all   = mol.GetNumAtoms()
    n_H     = n_all - n_heavy
    fq      = Chem.GetFormalCharge(mol)

    # Total electrons = sum of atomic numbers - formal charge
    total_electrons = sum(a.GetAtomicNum() for a in mol.GetAtoms()) - fq
    odd = 'ODD' if total_electrons % 2 != 0 else 'even'

    print(f"{lig:<12} {n_heavy:>10} {n_all:>9} {n_H:>5} {fq:>8} {total_electrons:>10} {odd:>8}")
