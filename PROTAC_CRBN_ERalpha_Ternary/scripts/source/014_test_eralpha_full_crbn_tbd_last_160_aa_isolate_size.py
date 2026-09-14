
# Test with ERalpha (full) + CRBN TBD (last 160 aa) to isolate size vs other issue
r_tbd = run_aidd_tool('protacfold', {
    "name": "ARV471_ERalpha_CRBN_TBD_test",
    "sequences": [
        {"protein": {"id": "A", "sequence": "SIKRSKKNSLALSLTADQMVSALLDAEPPILYSEYDPTRPFSEASMMGLLTNLADRELVHMINWAKRVPGFVDLTLHDQVHLLECAWLEILMIGLVWRSMEHPGKLLFAPNLLLDRNQGKCVEGMVEIFDMLLATSSRFRMMNLQGEEFVCLKSIILLNSGVYTFLSSTLKSLEEKDHIHRVLDKITDTLIHLMAKAGLTLQQQHQRLAQLLLILSHIRHMSNKGMEHLYSMKCKNVVPLSDLLLEMLDAHRLHAPTS"}},
        {"protein": {"id": "B", "sequence": tbd}},
        {"ligand":  {"id": "C", "smiles": canonical}}
    ],
    "modelSeeds": [42], "seed": 42,
    "diffusion_samples": 1,
    "output_format": "pdb",
    "use_msa_server": False,
    "dialect": "alphafold3", "version": 1
}, gpu=True)

print("rc:", r_tbd.get('rc'))
print("summary:", r_tbd.get('summary'))
