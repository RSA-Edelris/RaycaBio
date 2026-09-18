
# ── Main pocket: residues within 4.5 Å of any LVY atom ──────────────────────
cutoff_main = 4.5

prot_xyz = np.array([[a['x'],a['y'],a['z']] for a in protein])

main_pocket_res = {}
for pa in protein:
    pa_xyz = np.array([pa['x'], pa['y'], pa['z']])
    for la in lvy:
        la_xyz = np.array([la['x'], la['y'], la['z']])
        dist = np.linalg.norm(pa_xyz - la_xyz)
        if dist <= cutoff_main:
            key = (pa['resseq'], pa['resname'])
            main_pocket_res[key] = main_pocket_res.get(key, 0) + 1
            break

print("=== MAIN POCKET (LVY-binding, ≤4.5 Å) ===")
for (rseq, rname), n in sorted(main_pocket_res.items()):
    print(f"  {rname:3s} {rseq:4d}  ({n} atoms)")

# ── ZN coordination shell: residues within 3.0 Å of ZN ──────────────────────
zn_pos = np.array([zn_atm[0]['x'], zn_atm[0]['y'], zn_atm[0]['z']])
zn_shell = {}
for pa in protein:
    d = np.linalg.norm(np.array([pa['x'],pa['y'],pa['z']]) - zn_pos)
    if d <= 3.0:
        key = (pa['resseq'], pa['resname'])
        zn_shell[key] = True

print("\n=== ZN COORDINATION SHELL (≤3.0 Å) ===")
for (rseq, rname) in sorted(zn_shell.keys()):
    print(f"  {rname:3s} {rseq:4d}")

# Extended ZN pocket: 5 Å sphere
zn_pocket_res = {}
for pa in protein:
    d = np.linalg.norm(np.array([pa['x'],pa['y'],pa['z']]) - zn_pos)
    if d <= 5.0:
        key = (pa['resseq'], pa['resname'])
        zn_pocket_res[key] = True

print("\n=== ZN POCKET SHELL (≤5.0 Å) ===")
for (rseq, rname) in sorted(zn_pocket_res.keys()):
    print(f"  {rname:3s} {rseq:4d}")
