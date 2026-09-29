
# ── Build ternary complex PDB ──
# Chain A: BD1 ATOM + JQ1 HETATM  (3MXF chain A, transformed by Rf/tf)
# Chain B: VHL ATOM + MZ1 HETATM  (5T35 chain D)
# Chain C: ElonginC ATOM           (5T35 chain C)
# Chain D: ElonginB ATOM           (5T35 chain B)

def transform_xyz(x, y, z, R, t):
    v = np.array([x, y, z])
    w = v @ R.T + t
    return float(w[0]), float(w[1]), float(w[2])

def rechain_line(line, new_chain, serial_offset=0):
    """Return a PDB ATOM/HETATM line with updated chain and serial."""
    serial = int(line[6:11]) + serial_offset
    new_line = f"{line[:6]}{serial:5d}{line[11:21]}{new_chain}{line[22:]}"
    return new_line

def transform_line(line, R, t):
    """Apply rotation+translation to x,y,z of a PDB line."""
    x, y, z = float(line[30:38]), float(line[38:46]), float(line[46:54])
    nx, ny, nz = transform_xyz(x, y, z, R, t)
    return f"{line[:30]}{nx:8.3f}{ny:8.3f}{nz:8.3f}{line[54:]}"

output_lines = []
serial = 0

def write_chain(src_path, src_chain, out_chain, record_types,
                do_transform=False, R=None, t=None,
                hetatm_resname=None, serial_start=0):
    lines_out = []
    s = serial_start
    with open(src_path) as f:
        for line in f:
            rt = line[:6].strip()
            if rt not in record_types: continue
            if line[21] != src_chain: continue
            if hetatm_resname and rt == "HETATM":
                if line[17:20].strip() != hetatm_resname: continue
            if rt in ("HETATM",) and hetatm_resname is None and not do_transform:
                continue   # skip HETATM unless requested
            # skip waters
            rn = line[17:20].strip()
            if rn in ("HOH", "WAT", "DMS", "EDO", "IOD"): continue
            if do_transform:
                line = transform_line(line, R, t)
            s += 1
            new = f"{line[:6]}{s:5d}{line[11:21]}{out_chain}{line[22:76].rstrip()}\n"
            lines_out.append(new)
    return lines_out, s

# Chain A: BD1 ATOM records (transformed)
lines_A_atom, s = write_chain(pdb3, 'A', 'A', {'ATOM'}, do_transform=True, R=Rf, t=tf, serial_start=0)
# Chain A: JQ1 HETATM (transformed)
lines_A_het, s = write_chain(pdb3, 'A', 'A', {'HETATM'}, do_transform=True, R=Rf, t=tf,
                              hetatm_resname='JQ1', serial_start=s)

# Chain B: VHL ATOM records (from 5T35 chain D, no transform)
lines_B_atom, s = write_chain(pdb5, 'D', 'B', {'ATOM'}, serial_start=s)
# Chain B: MZ1 HETATM (VHL warhead, 5T35 chain D, resname 759)
lines_B_het, s = write_chain(pdb5, 'D', 'B', {'HETATM'}, hetatm_resname='759', serial_start=s)

# Chain C: ElonginC ATOM (5T35 chain C)
lines_C, s = write_chain(pdb5, 'C', 'C', {'ATOM'}, serial_start=s)

# Chain D: ElonginB ATOM (5T35 chain B)
lines_D, s = write_chain(pdb5, 'B', 'D', {'ATOM'}, serial_start=s)

# Assemble with TER records
all_lines = (["REMARK  BRD4-BD1 / VHL:ElonginCB ternary complex model\n",
              "REMARK  BD1+JQ1 from 3MXF (Kabsch-superposed onto 5T35 BD2 position)\n",
              "REMARK  VHL+MZ1+ElonginCB from 5T35 (chains D,C,B)\n",
              "REMARK  BD1 Kabsch RMSD vs BD2 = 0.53 A (73 core residues)\n",
              "REMARK  Chains: A=BD1+JQ1  B=VHL+MZ1-warhead  C=ElonginC  D=ElonginB\n"]
             + lines_A_atom + ["TER\n"]
             + lines_A_het
             + lines_B_atom + ["TER\n"]
             + lines_B_het
             + lines_C + ["TER\n"]
             + lines_D + ["TER\n", "END\n"])

out_pdb = work_dir / "BRD4BD1_VHL_ternary_model.pdb"
with open(out_pdb, 'w') as f:
    f.writelines(all_lines)

n_atoms = sum(1 for l in all_lines if l[:4] in ("ATOM", "HETA"))
print(f"Written: {out_pdb}")
print(f"Total ATOM+HETATM records: {n_atoms}")
print(f"Total lines: {len(all_lines)}")
print(f"Chains: A(BD1+JQ1)={len(lines_A_atom)+len(lines_A_het)}  "
      f"B(VHL+MZ1)={len(lines_B_atom)+len(lines_B_het)}  "
      f"C(ElonginC)={len(lines_C)}  D(ElonginB)={len(lines_D)}")
