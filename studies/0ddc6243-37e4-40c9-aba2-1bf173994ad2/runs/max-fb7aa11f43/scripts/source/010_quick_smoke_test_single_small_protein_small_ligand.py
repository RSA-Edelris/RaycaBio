
# Quick smoke-test: single small protein + small ligand - does Boltz predict at all?
r_test = run_aidd_tool('boltz', {
    'sequences': [
        {
            'protein': {
                'id': 'A',
                'sequence': 'MTYKLILNGKTLKGETTTEAVDAATAEKVFKQYANDNGVDGEWTYDDATKTFTVTE',
                'msa': 'empty'
            }
        },
        {
            'ligand': {
                'id': 'B',
                'smiles': 'c1ccccc1'   # benzene, trivial
            }
        }
    ],
    'diffusion_samples': 1,
    'recycling_steps': 1,
    'sampling_steps': 10,   # minimal, just checking it runs
    'seed': 1,
    'output_format': 'mmcif',
    'use_msa_server': False,
    'no_kernels': True
})
print("rc:", r_test.get('rc'))
print("summary:", r_test.get('summary'))
print("confidence:", r_test.get('confidence'))
