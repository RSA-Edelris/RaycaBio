
# Binary search: what is the max token count that works?
# Try 258 + 30 = 288 tokens (ERalpha full + tiny CRBN stub)
crbn_stub_30 = crbn_proper[-30:]   # last 30 residues of CRBN
print(f"CRBN stub (30 aa): {crbn_stub_30}")

r_288 = run_aidd_tool('protacfold', {
    "name": "ARV471_288tok_test",
    "sequences": [
        {"protein": {"id": "A", "sequence": "SIKRSKKNSLALSLTADQMVSALLDAEPPILYSEYDPTRPFSEASMMGLLTNLADRELVHMINWAKRVPGFVDLTLHDQVHLLECAWLEILMIGLVWRSMEHPGKLLFAPNLLLDRNQGKCVEGMVEIFDMLLATSSRFRMMNLQGEEFVCLKSIILLNSGVYTFLSSTLKSLEEKDHIHRVLDKITDTLIHLMAKAGLTLQQQHQRLAQLLLILSHIRHMSNKGMEHLYSMKCKNVVPLSDLLLEMLDAHRLHAPTS"}},
        {"protein": {"id": "B", "sequence": crbn_stub_30}},
        {"ligand":  {"id": "C", "smiles": canonical}}
    ],
    "modelSeeds": [42], "seed": 42,
    "diffusion_samples": 1,
    "sampling_steps": 10, "recycling_steps": 1,
    "output_format": "pdb", "use_msa_server": False,
    "dialect": "alphafold3", "version": 1
}, gpu=True)

print(f"\n288-token run: rc={r_288.get('rc')} — {r_288.get('summary')}")
