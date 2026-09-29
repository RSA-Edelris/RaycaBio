
# ── Interface analysis and linker cooperativity model ──

def read_ca_chain(path, chain_id):
    c=[]; seen=set()
    with open(path) as f:
        for line in f:
            if line[:4]=="ATOM" and line[21]==chain_id and line[12:16].strip()=="CA":
                rn=int(line[22:26])
                if rn not in seen:
                    seen.add(rn)
                    x,y,z=float(line[30:38]),float(line[38:46]),float(line[46:54])
                    c.append(np.array([x,y,z]))
    return np.array(c)

def apply_transform(c,R,t): return c@R.T+t

# ── 1. BD2–VHL interface contacts from 5T35 (crystal reference) ──
bd2_ca = read_ca_chain(pdb5,'A')  # BRD4 BD2
vhl_ca = read_ca_chain(pdb5,'D')  # VHL
elcb_ca = read_ca_chain(pdb5,'B') # ElonginB
elcc_ca = read_ca_chain(pdb5,'C') # ElonginC

def count_interface_contacts(ca1, ca2, cutoff=12.0):
    n_contacts = 0
    for a in ca1:
        dists = np.linalg.norm(ca2 - a, axis=1)
        n_contacts += (dists < cutoff).sum()
    return n_contacts

bd2_vhl_contacts   = count_interface_contacts(bd2_ca, vhl_ca)
bd2_elcb_contacts  = count_interface_contacts(bd2_ca, elcb_ca)
bd2_elcc_contacts  = count_interface_contacts(bd2_ca, elcc_ca)
print(f"Crystal (5T35) interface contacts (<12Å Cα-Cα):")
print(f"  BD2–VHL:     {bd2_vhl_contacts}")
print(f"  BD2–ElonginB:{bd2_elcb_contacts}")
print(f"  BD2–ElonginC:{bd2_elcc_contacts}")
total_crystal = bd2_vhl_contacts + bd2_elcb_contacts + bd2_elcc_contacts
print(f"  Total:        {total_crystal}")

# ── 2. BD1 (superposed) interface contacts with VHL complex ──
bd1_ca_orig = read_ca_chain(pdb3,'A')
bd1_ca_tf   = apply_transform(bd1_ca_orig, Rf, tf)

bd1_vhl_contacts   = count_interface_contacts(bd1_ca_tf, vhl_ca)
bd1_elcb_contacts  = count_interface_contacts(bd1_ca_tf, elcb_ca)
bd1_elcc_contacts  = count_interface_contacts(bd1_ca_tf, elcc_ca)
print(f"\nModel (BD1 superposed) interface contacts (<12Å Cα-Cα):")
print(f"  BD1–VHL:     {bd1_vhl_contacts}")
print(f"  BD1–ElonginB:{bd1_elcb_contacts}")
print(f"  BD1–ElonginC:{bd1_elcc_contacts}")
total_model = bd1_vhl_contacts + bd1_elcb_contacts + bd1_elcc_contacts
print(f"  Total:        {total_model}")
print(f"  Fraction of crystal reference: {total_model/total_crystal:.2f}")
