
# Test CRBN alone (406 residues) - is this the failing size?
r_crbn = run_aidd_tool('boltz', {
    'sequences': [
        {'protein': {'id': 'A',
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
print("=== CRBN alone (406 aa) ===")
print("rc:", r_crbn.get('rc'), "summary:", r_crbn.get('summary'))
