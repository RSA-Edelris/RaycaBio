
from rdkit import Chem
raw_smiles = "OC=1C=C2C([C@H]([C@H](CC2)C3=CC=CC=C3)C4=CC=C(C=C4)N5CCC(CN6CCN(CC6)C=7C=C8C(=CC7)C(=O)N(C8)[C@@H]9C(=O)NC(=O)CC9)CC5)=CC1"
canonical = Chem.MolToSmiles(Chem.MolFromSmiles(raw_smiles))

eralpha_full = "SIKRSKKNSLALSLTADQMVSALLDAEPPILYSEYDPTRPFSEASMMGLLTNLADRELVHMINWAKRVPGFVDLTLHDQVHLLECAWLEILMIGLVWRSMEHPGKLLFAPNLLLDRNQGKCVEGMVEIFDMLLATSSRFRMMNLQGEEFVCLKSIILLNSGVYTFLSSTLKSLEEKDHIHRVLDKITDTLIHLMAKAGLTLQQQHQRLAQLLLILSHIRHMSNKGMEHLYSMKCKNVVPLSDLLLEMLDAHRLHAPTS"
crbn_stub = "GSMEAGRPRPVLRSVNSREPSQVIFCNRSP"  # 30 aa from sanity

# Test 1: ERalpha first 256 aa (just below 256-token pad boundary)
eral_256 = eralpha_full[:256]
print(f"ERalpha 256-truncated (last 5 aa: {eral_256[-5:]}), total={len(eral_256)}")

r_256 = run_aidd_tool('protacfold', {
    "name": "ARV471_eral256_crbn30",
    "sequences": [
        {"protein": {"id": "A", "sequence": eral_256}},
        {"protein": {"id": "B", "sequence": crbn_stub}},
        {"ligand":  {"id": "C", "smiles": canonical}}
    ],
    "modelSeeds": [42], "seed": 42,
    "diffusion_samples": 1,
    "sampling_steps": 10, "recycling_steps": 1,
    "output_format": "pdb", "use_msa_server": False,
    "dialect": "alphafold3", "version": 1
}, gpu=True)

print(f"\n256-token ERalpha + 30-aa CRBN: rc={r_256.get('rc')}")
