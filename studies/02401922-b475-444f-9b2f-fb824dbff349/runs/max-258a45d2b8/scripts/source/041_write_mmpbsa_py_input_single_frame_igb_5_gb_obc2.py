
# Write MMPBSA.py input (single-frame, igb=5 GB-OBC2, salt=0.15M for pH 7.4)
mmpbsa_in = """&general
  startframe=1, endframe=1, interval=1,
  keep_files=0, verbose=1,
/
&gb
  igb=5, saltcon=0.150,
/
"""
with open('mmpbsa.in','w') as f:
    f.write(mmpbsa_in)

# Run MMPBSA.py
r_mmgb = subprocess.run([
    'MMPBSA.py', '-O',
    '-i', 'mmpbsa.in',
    '-o', 'FINAL_RESULTS_MMGBSA.dat',
    '-cp', 'complex.prmtop',
    '-rp', 'receptor.prmtop',
    '-lp', 'ligand_amber.prmtop',
    '-y',  'complex.inpcrd'
], capture_output=True, text=True, cwd=WS)

print("MMPBSA.py rc:", r_mmgb.returncode)
print(r_mmgb.stdout[-2000:])
if r_mmgb.returncode != 0:
    print("STDERR:", r_mmgb.stderr[-1000:])
