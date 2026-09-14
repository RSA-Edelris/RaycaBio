
# Test: short proteins (sanity lengths) + ARV-471 — isolates whether the PROTAC molecule causes the crash
r_ligtest = run_aidd_tool('protacfold', {
    "name": "short_proteins_ARV471_ligtest",
    "sequences": [
        {"protein": {"id": "A", "sequence": "SMEEPQSDPSVEPPLSQETFSDLWKLLPEN"}},
        {"protein": {"id": "B", "sequence": "GSMEAGRPRPVLRSVNSREPSQVIFCNRSP"}},
        {"ligand":  {"id": "C", "smiles": canonical}}   # ARV-471, 54 atoms
    ],
    "modelSeeds": [42], "seed": 42,
    "diffusion_samples": 1,
    "sampling_steps": 10,
    "recycling_steps": 1,
    "output_format": "pdb",
    "use_msa_server": False,
    "dialect": "alphafold3", "version": 1
}, gpu=True)

print("rc:", r_ligtest.get('rc'))
print("summary:", r_ligtest.get('summary'))
