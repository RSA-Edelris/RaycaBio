
import os, glob, shutil

# Test A: 2 proteins only (no ligand)
r_proteins = run_aidd_tool('boltz', {
    'sequences': [
        {'protein': {'id': 'A',
                     'sequence': 'GSGPIRLPIVDKYKDMGTVVLGKLESGSICKGQQLVMMPNKHNVEVLGILSDDVETDTVAPGENLKIRLKGIEEEEILPGFILCDPNNLCHSGRTFDAQIVIIEHKSIICPGYNAVLHIHTCIEEVEITALICLVDKKSGEKSKTRPRFVKQDQVCIARLRTAGTICLETFKDFPQMGRFTLRDEGKTIAIGKVLKLVP',
                     'msa': 'empty'}},
        {'protein': {'id': 'B',
                     'sequence': 'GSMEAKKPNIINFDTSLPTSHTYLGADMEEFHGRTLHDDDSCQVIPVLPQVMMILIPGQTLPLQLFHPQEVSMVRNLIQKDRTFAVLAYSNVQEREAQFGTTAEIYAYREEQDFGIEIVKVKAIGRQRFKVLELRTQSDGIQQAKVQILPECVLPSTMSAVQLESLNKCQIFPSKPVSREDQCSYKWWQKYQKRKFHCANLTSWPRWLYSLYDAETLMDRIKKQLREWDENLKDDSLPSNPIDFSYRVAACLPIDDVLRIQLLKIGSAIQRLRCELDIMNKCTSLCCKQCQETEITTKNEIFSLSLCGPMAAYVNPHGYVHETLTVYKACNLNLIGRPSTEHSWFPGYAWTVAQCKICASHIGWKFTATKKDMSPQKFWGLTRSALLPTIPDTEDEISPDKVILCL',
                     'msa': 'empty'}}
    ],
    'diffusion_samples': 1,
    'recycling_steps': 1,
    'sampling_steps': 10,
    'seed': 42,
    'output_format': 'mmcif',
    'use_msa_server': False,
    'no_kernels': True
})
print("=== 2-protein (no ligand) ===")
print("rc:", r_proteins.get('rc'))
print("summary:", r_proteins.get('summary'))
