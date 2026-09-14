
# Sanity check with the schema's own example (short sequences, fast settings)
r_sanity = run_aidd_tool('protacfold', {
    "name": "ratb_min_ternary",
    "sequences": [
        {"protein": {"id": "A", "sequence": "SMEEPQSDPSVEPPLSQETFSDLWKLLPEN"}},
        {"protein": {"id": "B", "sequence": "GSMEAGRPRPVLRSVNSREPSQVIFCNRSP"}},
        {"ligand":  {"id": "C", "smiles": "CC(=O)Nc1ccc(O)cc1"}}
    ],
    "modelSeeds": [42], "seed": 42,
    "diffusion_samples": 1,
    "sampling_steps": 10,
    "recycling_steps": 1,
    "output_format": "mmcif",
    "use_msa_server": False,
    "dialect": "alphafold3", "version": 1
}, gpu=True)

print("rc:", r_sanity.get('rc'))
print("summary:", r_sanity.get('summary'))
if r_sanity.get('rc') == 0:
    print("confidence:", r_sanity.get('confidence'))
