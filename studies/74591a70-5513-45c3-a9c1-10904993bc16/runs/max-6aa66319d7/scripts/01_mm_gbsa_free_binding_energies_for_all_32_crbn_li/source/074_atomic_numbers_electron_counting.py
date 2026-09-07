
import re
from pathlib import Path

# Atomic numbers for electron counting
Z = {'H':1,'C':6,'N':7,'O':8,'F':9,'S':16,'Cl':17,'Br':35,'I':53,'P':15}

# V2000 atom charge codes → formal charge
atom_chg_code = {0:0, 1:3, 2:2, 3:1, 4:0, 5:-1, 6:-2, 7:-3}  # 4 = radical

def analyse_sdf(sdf_path):
    lines = Path(sdf_path).read_text().split("\n")
    # Find counts line (line 4, 0-indexed line 3)
    for i, line in enumerate(lines):
        if 'V2000' in line:
            counts_line = line
            atom_count = int(counts_line[0:3])
            # Atom block starts at next line
            atom_start = i + 1
            break
    else:
        return None  # not V2000

    # Parse atom block
    elems = []
    formal_charges = []
    for j in range(atom_count):
        aline = lines[atom_start + j]
        if len(aline) < 34:
            continue
        elem = aline[31:34].strip()
        elems.append(elem)
        # Charge code at columns 37-39 (0-indexed 36-38)
        if len(aline) >= 39:
            try:
                chg_code = int(aline[36:39].strip() or '0')
                formal_charges.append(atom_chg_code.get(chg_code, 0))
            except ValueError:
                formal_charges.append(0)
        else:
            formal_charges.append(0)

    # M  CHG lines override atom-block charges
    m_chg = {}
    for line in lines:
        if line.startswith("M  CHG"):
            parts = line.split()
            n = int(parts[2])
            for k in range(n):
                atom_idx = int(parts[3 + k*2]) - 1  # 1-indexed
                charge   = int(parts[4 + k*2])
                m_chg[atom_idx] = charge

    # Apply M CHG overrides
    for idx, chg in m_chg.items():
        if idx < len(formal_charges):
            formal_charges[idx] = chg

    net_charge = sum(formal_charges)
    total_Z = sum(Z.get(e, 0) for e in elems)
    n_electrons = total_Z - net_charge

    elem_str = ""
    for e in sorted(set(elems)):
        elem_str += f"{e}{elems.count(e)}"

    return {
        "formula": elem_str,
        "nc": net_charge,
        "n_electrons": n_electrons,
        "odd": n_electrons % 2 != 0,
        "n_atoms": atom_count
    }

# Analyse all 32
print(f"{'Ligand':<26} {'Formula':<22} {'nc':>3} {'e-':>5} {'odd':>5}")
print("-"*65)
for name in names:
    sdf = f"{WORK}/best_poses/{name}_pose1.sdf"
    res = analyse_sdf(sdf)
    if res:
        flag = " *** ODD ***" if res["odd"] else ""
        print(f"{name:<26} {res['formula']:<22} {res['nc']:>3} {res['n_electrons']:>5} {flag}")
