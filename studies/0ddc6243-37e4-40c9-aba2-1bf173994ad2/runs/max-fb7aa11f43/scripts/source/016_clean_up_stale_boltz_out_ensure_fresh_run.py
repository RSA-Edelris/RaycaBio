
import os, shutil

# Clean up stale boltz_out to ensure fresh run
shutil.rmtree('boltz_out', ignore_errors=True)

# Test GSPT1 alone at 199 residues
r_gspt1 = run_aidd_tool('boltz', {
    'sequences': [
        {'protein': {'id': 'A',
                     'sequence': 'GSGPIRLPIVDKYKDMGTVVLGKLESGSICKGQQLVMMPNKHNVEVLGILSDDVETDTVAPGENLKIRLKGIEEEEILPGFILCDPNNLCHSGRTFDAQIVIIEHKSIICPGYNAVLHIHTCIEEVEITALICLVDKKSGEKSKTRPRFVKQDQVCIARLRTAGTICLETFKDFPQMGRFTLRDEGKTIAIGKVLKLVP',
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
print("=== GSPT1 alone (199 aa) ===")
print("rc:", r_gspt1.get('rc'), " | summary:", r_gspt1.get('summary'))

# After the run, look for any log/events files that might hold the full traceback
for root, dirs, files in os.walk('boltz_out'):
    for f in files:
        full = os.path.join(root, f)
        print(f"  {full}  ({os.path.getsize(full)} b)")
