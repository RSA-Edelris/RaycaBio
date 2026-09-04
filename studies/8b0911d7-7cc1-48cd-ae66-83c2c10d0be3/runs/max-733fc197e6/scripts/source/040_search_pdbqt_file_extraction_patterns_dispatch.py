
# Search for pdbqt or file extraction patterns in dispatch source
for keyword in ['pdbqt', 'tar', 'extract', 'files_written', 'ligand_out', 'fetch_file', 'copy_out']:
    idx = dsrc.find(keyword)
    if idx >= 0:
        print(f"--- found '{keyword}' at {idx} ---")
        print(dsrc[max(0,idx-100):idx+300])
        print()
