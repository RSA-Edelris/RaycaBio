
import gemmi, numpy as np, os

BASE = "/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b/job-6567207/ternary_out"

GSPT1_LEN = 199
CRBN_LEN  = 406

def parse_pdb(path):
    st = gemmi.read_structure(path)
    model = st[0]
    chains = {}
    for chain in model:
        coords, resnames, resnums, atomnames = [], [], [], []
        for res in chain:
            for atom in res:
                coords.append([atom.pos.x, atom.pos.y, atom.pos.z])
                resnames.append(res.name)
                resnums.append(res.seqid.num)
                atomnames.append(atom.name)
        chains[chain.name] = {
            'coords': np.array(coords),
            'resnames': resnames,
            'resnums': resnums,
            'atomnames': atomnames,
        }
    return chains

def ca_coords(chain_data):
    """Extract Cα coordinates."""
    ca = [(c, rn) for c, rn, an in zip(
        chain_data['coords'], chain_data['resnums'], chain_data['atomnames'])
          if an == 'CA']
    if not ca:
        return np.array([])
    return np.array([c for c, _ in ca])

def heavy_coords(chain_data):
    return chain_data['coords']

results = []
for i in range(3):
    path = f"{BASE}/gspt1_crbn_glue_{i}.pdb"
    chains = parse_pdb(path)
    chain_names = list(chains.keys())
    print(f"\nModel {i} chains: {chain_names}")
    for cn in chain_names:
        n_atoms = len(chains[cn]['coords'])
        unique_res = len(set(chains[cn]['resnums']))
        sample_res = set(chains[cn]['resnames'])
        print(f"  Chain {cn}: {n_atoms} atoms, {unique_res} residues, residue types (sample): {list(sample_res)[:5]}")
    results.append(chains)
