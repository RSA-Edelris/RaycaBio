
# Read the successful MM-GBSA calculation scripts from previous session
for fname in ['026_mm_gbsa_via_openmm_implicit_solvent_ff14sb_gaff2.py',
              '030_confirm_all_files_exist.py',
              '037_range.py']:
    path = os.path.join(ws, 'source', fname)
    if os.path.exists(path):
        print(f"\n{'='*60}")
        print(f"=== {fname} ===")
        print(open(path).read()[:3000])
