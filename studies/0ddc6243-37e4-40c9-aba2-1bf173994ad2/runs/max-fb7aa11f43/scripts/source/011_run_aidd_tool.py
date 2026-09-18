
r_min = run_aidd_tool('boltz', {
    'sequences': [
        {
            'protein': {
                'id': 'A',
                'sequence': 'GSGPIRLPIVDKYKDMGTVVLGKLESGSICKGQQLVMMPNKHNVEVLGILSDDVETDTVAPGENLKIRLKGIEEEEILPGFILCDPNNLCHSGRTFDAQIVIIEHKSIICPGYNAVLHIHTCIEEVEITALICLVDKKSGEKSKTRPRFVKQDQVCIARLRTAGTICLETFKDFPQMGRFTLRDEGKTIAIGKVLKLVP',
                'msa': 'empty'
            }
        },
        {
            'protein': {
                'id': 'B',
                'sequence': 'GSMEAKKPNIINFDTSLPTSHTYLGADMEEFHGRTLHDDDSCQVIPVLPQVMMILIPGQTLPLQLFHPQEVSMVRNLIQKDRTFAVLAYSNVQEREAQFGTTAEIYAYREEQDFGIEIVKVKAIGRQRFKVLELRTQSDGIQQAKVQILPECVLPSTMSAVQLESLNKCQIFPSKPVSREDQCSYKWWQKYQKRKFHCANLTSWPRWLYSLYDAETLMDRIKKQLREWDENLKDDSLPSNPIDFSYRVAACLPIDDVLRIQLLKIGSAIQRLRCELDIMNKCTSLCCKQCQETEITTKNEIFSLSLCGPMAAYVNPHGYVHETLTVYKACNLNLIGRPSTEHSWFPGYAWTVAQCKICASHIGWKFTATKKDMSPQKFWGLTRSALLPTIPDTEDEISPDKVILCL',
                'msa': 'empty'
            }
        },
        {
            'ligand': {
                'id': 'C',
                'smiles': 'Cc1ccc(NC(=O)NCc2ccc3C(=O)N(Cc3c2)[C@H]4CCC(=O)NC4=O)cc1Cl'
            }
        }
    ],
    'diffusion_samples': 1,
    'recycling_steps': 1,
    'sampling_steps': 10,   # minimal — just get it to run
    'seed': 42,
    'output_format': 'mmcif',
    'use_msa_server': False,
    'no_kernels': True
})
print("rc:", r_min.get('rc'))
print("summary:", r_min.get('summary'))
print("confidence:", r_min.get('confidence'))
print("structures:", r_min.get('structures'))
