
import shutil, os

# Move the failed run aside so the tool gets a clean output dir
if os.path.exists('protacfold_out'):
    shutil.move('protacfold_out', 'protacfold_out_attempt1_failed')
    print("moved old output dir aside")

result = run_aidd_tool('protacfold', {
    'name': 'gspt1_crbn_molecular_glue_ternary',
    'sequences': [
        {
            'protein': {
                'id': 'A',
                'sequence': 'GSGPIRLPIVDKYKDMGTVVLGKLESGSICKGQQLVMMPNKHNVEVLGILSDDVETDTVAPGENLKIRLKGIEEEEILPGFILCDPNNLCHSGRTFDAQIVIIEHKSIICPGYNAVLHIHTCIEEVEITALICLVDKKSGEKSKTRPRFVKQDQVCIARLRTAGTICLETFKDFPQMGRFTLRDEGKTIAIGKVLKLVP'
            }
        },
        {
            'protein': {
                'id': 'B',
                'sequence': 'GSMEAKKPNIINFDTSLPTSHTYLGADMEEFHGRTLHDDDSCQVIPVLPQVMMILIPGQTLPLQLFHPQEVSMVRNLIQKDRTFAVLAYSNVQEREAQFGTTAEIYAYREEQDFGIEIVKVKAIGRQRFKVLELRTQSDGIQQAKVQILPECVLPSTMSAVQLESLNKCQIFPSKPVSREDQCSYKWWQKYQKRKFHCANLTSWPRWLYSLYDAETLMDRIKKQLREWDENLKDDSLPSNPIDFSYRVAACLPIDDVLRIQLLKIGSAIQRLRCELDIMNKCTSLCCKQCQETEITTKNEIFSLSLCGPMAAYVNPHGYVHETLTVYKACNLNLIGRPSTEHSWFPGYAWTVAQCKICASHIGWKFTATKKDMSPQKFWGLTRSALLPTIPDTEDEISPDKVILCL'
            }
        },
        {
            'ligand': {
                'id': 'C',
                'smiles': 'Cc1ccc(NC(=O)NCc2ccc3C(=O)N(Cc3c2)[C@H]4CCC(=O)NC4=O)cc1Cl'
            }
        }
    ],
    'modelSeeds': [42],
    'diffusion_samples': 1,
    'recycling_steps': 3,
    'sampling_steps': 200,
    'output_format': 'mmcif',
    'use_msa_server': False,
    'dialect': 'alphafold3',
    'version': 1
})

print("rc:", result.get('rc'))
print("summary:", result.get('summary'))
print("confidence:", result.get('confidence'))
print("structures:", result.get('structures'))
