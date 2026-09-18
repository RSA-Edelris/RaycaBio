
import shutil, os

# Clear output from previous protacfold attempt
if os.path.exists('protacfold_out'):
    shutil.move('protacfold_out', 'protacfold_out_attempt2_failed')

result2 = run_aidd_tool('boltz', {
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
    'recycling_steps': 3,
    'sampling_steps': 200,
    'seed': 42,
    'output_format': 'mmcif',
    'use_msa_server': False,
    'no_kernels': True
})

print("rc:", result2.get('rc'))
print("summary:", result2.get('summary'))
print("confidence:", result2.get('confidence'))
print("structures:", result2.get('structures'))
