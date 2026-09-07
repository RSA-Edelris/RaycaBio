
import subprocess

# Check analysis tools for post-MD MM-GBSA
for t in ['gmx_MMPBSA', 'cpptraj', 'mmpbsa_py']:
    r = subprocess.run(['which', t], capture_output=True, text=True)
    print(f"  {t}: {r.stdout.strip() if r.returncode==0 else 'not found'}")

# cpptraj version
r = subprocess.run(['cpptraj', '--version'], capture_output=True, text=True)
print("\ncpptraj:", (r.stdout + r.stderr).splitlines()[0] if r.returncode==0 else 'error')

# Check if mdtraj can read xtc (for custom MM-GBSA)
import mdtraj as md
print(f"mdtraj {md.__version__}: xtc support = {'.xtc' in md.formats.registry.loaders}")

# Save job details
with open(f'{WD}/md_EDS01806218_ent2/job_info.txt', 'w') as fh:
    fh.write("Job ID: 6284357\nCluster: Isambard-AI_HPC\nRun ID: max-cf01a0650f\n"
             "System: 29253 atoms, 142-res CRBN pocket + EDS01806218_ent2, TIP3P\n"
             "Protocol: EM (10k steps) -> NPT eq 200 ps -> NPT prod 10 ns\n"
             "Force fields: ff14SB (protein) + GAFF2/AM1-BCC (ligand) + TIP3P\n"
             "T=300K, P=1 bar, V-rescale + Parrinello-Rahman\n")
print("\nJob info saved.")
