
# ── Correct prep: keep chain B (CRBN+LVY), remove chain A (DDB1) ──────────────

fixer2 = PDBFixer(filename=raw_pdb)

chain_list = [(i, c.id, sum(1 for _ in c.residues()))
              for i, c in enumerate(fixer2.topology.chains())]
print("Chain inventory:")
for idx, cid, nres in chain_list:
    print(f"  idx={idx}  id={cid}  residues={nres}")

# Remove chain A segments (DDB1); keep chain B (CRBN)
remove_idx = [idx for idx, cid, _ in chain_list if cid == 'A']
print(f"\nRemoving chain-A segments: indices {remove_idx}")
fixer2.removeChains(remove_idx)

remaining = [(i, c.id, sum(1 for _ in c.residues()))
             for i, c in enumerate(fixer2.topology.chains())]
print("Remaining chains after removal:")
for idx, cid, nres in remaining:
    print(f"  idx={idx}  id={cid}  residues={nres}")

# ── Fix missing residues (internal loops only) ────────────────────────────────
fixer2.findMissingResidues()
chains_topo = list(fixer2.topology.chains())
for key in list(fixer2.missingResidues.keys()):
    cidx, ridx = key
    nres = sum(1 for _ in chains_topo[cidx].residues())
    if ridx == 0 or ridx >= nres:
        del fixer2.missingResidues[key]

n_loop = sum(len(v) for v in fixer2.missingResidues.values())
print(f"\nInternal missing residues to model: {n_loop}")
print("Loop details:", {str(k): v for k, v in fixer2.missingResidues.items()})

fixer2.findNonstandardResidues()
fixer2.replaceNonstandardResidues()
fixer2.findMissingAtoms()
fixer2.addMissingAtoms()
fixer2.addMissingHydrogens(7.4)
print("Hydrogens added at pH 7.4 (His ε/δ, Asp/Glu/Lys/Arg protonation states assigned).")

# ── Write receptor WITH LVY (for box/pocket reference) ───────────────────────
full_path = f"{WORK}/4CI2_CRBN_full.pdb"
with open(full_path, 'w') as out:
    PDBFile.writeFile(fixer2.topology, fixer2.positions, out, keepIds=True)
print(f"Full CRBN PDB (with LVY + ZN + waters): {full_path}")
print(f"File size: {os.path.getsize(full_path):,} bytes")
